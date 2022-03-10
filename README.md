# Ostyganie-arduino
Oprogramowanie przeznaczone do współpracy z przyrządem do automatycznych pomiarów temperatury

ARDUINO:
Program pobiera dane z trzech czujników DS18B20 i wysyła je do komputera. Każdy czujnik DS18B20 posiada swój indywidualny numer, więc aby uźyć innych czujników trzeba zmienić dane w sekcji "Przypisanie adresów czujników".

INTERFEJS:
Obsługa:
  Wybrać port do połączenia z arduino z listy lub wpisać ręcznie, a następnie wybrać częstotliwość pomiarów. Po naciśnięciu "Połącz" pomiary powinny rozpocząć się automatycznie. Dane są zapisywane w oknie po prawej stronie, umożliwiającym również ich edycję i zapis. Opcja "Zamiana kropek na przecinki" pozwala uniknąć błędów z wyświetlaniem w arkuszach kalkulacyjnych.

INSTALACJA I ZALEŻNOŚCI
Do działania programu w werskji nieskompilowanej są wymagane:
- Python 3 wraz z modułami:
  - matplotlib
  - PySimpleGUI
  - tk (Tkinter)
  - PySerial
Wersja skompilowana zawiera w sobie program i wszystkie zależności, więc nie wymaga instalacji dodatkowego oprogramowania.

Znane błędy:
- Wykrywanie przez Windows Defender jako potencjalne zagrożenie
