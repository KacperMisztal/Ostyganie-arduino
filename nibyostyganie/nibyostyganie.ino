/* Program symulujący działanie termometrów do ćwiczenia ostyganie
 * Pozwala testować działąnie interfejsu bez konieczności podłączania czujników
 */
 
// ZMIENNE GLOBALNE
unsigned long delayTime = 1000L; // Częstotliwość pomiaru
unsigned int startTime; //czas działania programu

// PRZYGOTOWANIE
void setup() {
   // Rozpoczęcie komunikacji
  Serial.begin(115200);
  // Oczekiwanie na otrzymanie danych o czasie
  while(true){
    if(Serial.available()){
      delayTime = Serial.parseInt() * 1000;
      Serial.println(delayTime);
      break;
    }
  }

  // Zapisanie czasu rozpoczęcia
  startTime = millis(); 
}

// DODATKOWE FUNKCJE
//funkcja odpowiedzialna za pomiar czasu
String getFormattedTime(){
  unsigned long timeInMs = millis() - startTime;  //obliczenie aktualnego czasu w ms
  unsigned int timeS = timeInMs / 1000; // Sekundy
  unsigned int timeM = timeInMs / 60000;  // Minuty
  unsigned int timeH = timeInMs / 3600000;  // Godziny
  return String(timeH) + ":" + String(timeM % 60) + ":" + String(timeS % 60);
}

// PĘTLA GŁÓWNA
void loop() {
  unsigned int beginTime = millis();
  
  int nr0 = random(0, 30);
  int nr1 = random(0, 30);
  int nr2 = random(0, 30);

  // Wysłąnie danych
  Serial.println(getFormattedTime() + "; " + String(nr0) + "; " + String(nr1) + "; " + String(nr2));

  // odczekanie zadanego czasu - czas wykonania programu
  delay(delayTime - (millis() - beginTime));
  
}
