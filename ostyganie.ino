// Kod bazuje na przykładach dołącznonych do bibiliotek OneWire i DallasTemperature
// Code based on examples included in OneWire and DallasTemperature libraries

//Autor : Kacper Misztal

// Biblioteki
#include <OneWire.h>
#include <DallasTemperature.h>

// Ustawienia
#define ONE_WIRE_BUS 10 //pin interfejsu OneWire
#define TEMPERATURE_PRECISION 12 //rozdzielczość czujnika [bit], min = 9, max = 12
long delayTime = 1000L;  //odstęp pomiędzy pomiarami
long baudrate = 115200;   //Szybkość kounikacji, bit/s

// Zmienne globalne
unsigned int startTime; //czas działania programu

// Przypisanie magistrali OneWire do odpowiedniego pinu
OneWire oneWire(ONE_WIRE_BUS);

// przekazanie danych OneWire do DallasTemperature
DallasTemperature sensors(&oneWire);

//Przypisanie adresów czujników
DeviceAddress tempSensor0 = { 0x28, 0xE5, 0x35, 0x9F, 0x0A, 0x00, 0x00, 0x9B };
DeviceAddress tempSensor1 = { 0x28, 0x9A, 0x6B, 0x9B, 0x0A, 0x00, 0x00, 0x1E };
DeviceAddress tempSensor2 = { 0x28, 0x2B, 0x40, 0x99, 0x0A, 0x00, 0x00, 0xA1 };

//funkcja odpowiedzialna za pomiar czasu
String getFormattedTime(){
  unsigned long timeInMs = millis() - startTime;  //obliczenie aktualnego czasu w ms
  unsigned int timeS = timeInMs / 1000;
  unsigned int timeM = timeInMs / 60000;
  unsigned int timeH = timeInMs / 3600000;
  return String(timeH) + ":" + String(timeM % 60) + ":" + String(timeS % 60);
}

void setup(void)
{
  // Komunikacja z komputerem
  Serial.begin(baudrate); //Rozpoczęcie komunikacji przez port szeregowy
  while(!Serial); //Oczekiwanie na połączenie

  // Oczekiwanie na otrzymanie danych o czasie
  while(true){
    if(Serial.available()){
      delayTime = Serial.parseInt() * 1000;
      Serial.println(delayTime);
      break;
  }
  
  }
  
  //zapisanie czasu
  startTime = millis(); 

  // rozpoczecie używania czjuników
  sensors.begin();

  // ustawienie zadanej wcześniej rozdzielczości
  sensors.setResolution(tempSensor0, TEMPERATURE_PRECISION);
  sensors.setResolution(tempSensor1, TEMPERATURE_PRECISION);
  sensors.setResolution(tempSensor2, TEMPERATURE_PRECISION);
}

//funkcja główna
void loop(void)
{
  // pomiar czasu wykonania programu
  unsigned long beginTime = millis();
  
  //wysłanie żądania do czujników
  sensors.requestTemperatures();

  // przesłanie wyników
  Serial.println(getFormattedTime() + "; " + String(sensors.getTempC(tempSensor0)) + "; " + String(sensors.getTempC(tempSensor1)) + "; " + String(sensors.getTempC(tempSensor2)));
  delay(delayTime - (millis() - beginTime));  // odczekanie zadanego czasu - czas wykonania programu
}
