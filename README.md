# Ostyganie-arduino
Oprogramowanie przeznaczone do współpracy z przyrządem do automatycznych pomiarów temperatury

ARDUINO:
Program pobiera dane z trzech czujników DS18B20 i wysyła je do komputera. Każdy czujnik DS18B20 posiada swój indywidualny numer, więc aby uźyć innych czujników trzeba zmienić dane w sekcji "Przypisanie adresów czujników".

INTERFEJS:
Obsługa:
  Wybrać port do połączenia z arduino z listy lub wpisać ręcznie, a następnie wybrać częstotliwość pomiarów. Po naciśnięciu "Połącz" pomiary powinny rozpocząć się automatycznie. Dane są zapisywane w oknie po prawej stronie, umożliwiającym również ich edycję i zapis. Opcja "Zamiana kropek na przecinki" pozwala uniknąć błędów z wyświetlaniem w arkuszach kalkulacyjnych.
