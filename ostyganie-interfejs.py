#usr/bin/python3
#coding=utf8
"""Program odbiera dane z Arduino i tworzy na ich podstawie wykres - przeznaczony tylko do użycia z urządzeniem do ćwiczenia \"Ostyganie\
Użyto elementów z: https://github.com/PySimpleGUI/PySimpleGUI/blob/master/DemoPrograms%20old/Demo_Matplotlib_Animated.py"""

# IMPORT MODUŁÓW
import serial   # Komunikacja przez porty szeregowe
from time import sleep  # Oczekiwanie
from re import sub  # Usuwanie zbędnych znaków
import PySimpleGUI as psg   # GUI
from platform import system # sprawdzanie systemu operacyjnego - do prawidłowego zapisu
import matplotlib as mpl # Wykresy
import matplotlib.pyplot as plt # Też wykresy
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, FigureCanvasAgg
from matplotlib.figure import Figure

mpl.use('TkAgg')

# USTAWIENIA

baudrate_value = 115200 # Prędkość przesyłu danych

if system() == 'Windows':   # Domyślny port
    port = 'COM1'   # Port - Windows
elif system() == 'Linux':
    port = '/dev/ttyACM0'   # Port - Linux
else:
    port = 'Wpisz nazwę portu'
    
defaultTime = 5
    
# ZMIENNE GLOBALNE
connected = False   # Przechowywanie informacji o połączeniu



# LAYOUTY ------------------------------------------------------------------------------------------

# Wymiary
windowInfo = {'element_justification':'left', 'finalize':'True'}
inputTextSize = (25, 1)
labelSize = (25, 1)
labelSize2 = (10, 1)
multilineSize = (40, 14)
outputTextInfo = {'size':(8, 1), 'background_color':'black', 'text_color':'red', 'font':('Arial', 20), 'justification':'right'}
saveTextBoxSize = (19, 1)
plotCanvasInfo = {'background_color':'white'}
figSize = [2.0, 2.0]

programLayout = [  
    # Lewa kolumna
    [psg.Column([
        # Liczniki
        [psg.Column([   
            [psg.Text('Czas [HH:MM:SS]')],
            [psg.Text(**outputTextInfo, key = 'outputText0')]   ]),
        psg.Column([   
            [psg.Text('T0 [*C]')],
            [psg.Text(**outputTextInfo, key = 'outputText1')]   ]),
        psg.Column([   
            [psg.Text('T1 [*C]')],
            [psg.Text(**outputTextInfo, key = 'outputText2')]   ]),
        psg.Column([   
            [psg.Text('T2 [*C]')],
            [psg.Text(**outputTextInfo, key = 'outputText3')]   ])  ],
        
        # Wykresy    
        [psg.Canvas(key = 'plotCanvas0', **plotCanvasInfo),
        psg.Canvas(key = 'plotCanvas1', **plotCanvasInfo),
        psg.Canvas(key = 'plotCanvas2', **plotCanvasInfo)]
    ]),
        
        
        # Prawa kolumna
    psg.Column([   
        # Lista zebranych danych 
        [psg.Text('Pomiary', key='simText1')],
        [psg.Multiline(key = 'simMultiline', size=multilineSize, disabled = False, autoscroll = True)],
        
        # Pola do zapisywania
        [psg.Text('Nazwa pliku: ', size=labelSize2), psg.InputText(size = saveTextBoxSize, key = 'fileInputText')],
        [psg.Text('Folder: ', size=labelSize2), psg.InputText(key = 'dirInputText', size = saveTextBoxSize), psg.FolderBrowse('Szukaj', key = 'browseButton')],
        [psg.Checkbox('Zamiana kropek na przecinki', key = 'comaCheckBox')],
        [psg.Button('Zapisz', key = 'SaveButton')]
    ])  ],
    
    # Wybór portu
    [psg.Text('Port', labelSize), psg.InputText(default_text = port, key = 'portInputText', size = inputTextSize)],
    [psg.Text('Częstotliwość pomiaru [s]', labelSize), psg.InputText(default_text = defaultTime, key = 'timeInputText', size = inputTextSize)],
    [psg.Button('Połącz', key = 'connectButton'), psg.Button('Rozłącz', key = 'disconnectButton')]
    
]

# FUNKCJE

# Nawiązywanie połączenia
def connect(port):
    try:    # Próba połączenia
        global arduino, connected
        arduino = serial.Serial(port, baudrate = baudrate_value, timeout = 1)
        connected = True
        print('Połączono z Arduino')
        sleep(5)
        sendTime()  # Wysłanie danych o częstotliwości pomiaru
        
    except Exception as e:  # W przypadku gdy nie udało się nawiązać połączenia
                psg.popup('Błąd połączenia\n' + str(e))
                
# Wysyłanie danych o częstotliwości pomiaru
def sendTime():
    try:
        timeToSend = int(window['timeInputText'].Get())
        print(timeToSend)
        if int(timeToSend) > 0: # sprawdzenie czy wartość czasu jest większa od zera
            arduino.write(str(timeToSend).encode())
            print('Wysłano')
            sleep(0.5)
            arduino.flush()
            print('Oczekiwanie na odbiór')
            if arduino.inWaiting() != 0:
                print('odebrane dane')
                print(str(arduino.readline()))
        else:
            raise ValueError()  # Wyświetlenie błędu
            
    except Exception as e:  # Obsługa błędów
        psg.popup('Błąd, nie udało się wysłać\n' + (str(e)))
        del(e)
        
# Zapis danych z okna pomiaru w pliku
def saveFile():
    try:    # Zapis danych do pliku
        fileName = str(window['dirInputText'].Get()) + '/' + str(window['fileInputText'].Get())

        if system() == 'Windows':   # Zmiana slash na backslash na Windowsie
            fileName.replace('/', '\\')

        text = str(window['simMultiline'].Get())  # Odczyt danych z okna pomiaru

        if values['comaCheckBox'] == True:  # Zamiana kropek na przecinki
            with open(fileName, 'a') as f:  # Otwarcie pliku
                f.write(text.replace('.', ','))  # Zapis

        else:
            with open(fileName, 'a') as f:  # Otwarcie pliku
                f.write(text)  # Zapis

        psg.popup('Zapisano!\n' + fileName)  # Informacja o poprawnym zapisie
        del(fileName)
        
    except Exception as e:  # Obsługa błędów
        psg.popup('Błąd, nie udało się zapisać\n' + (str(e)))
        del(e)

def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top')
    return figure_canvas_agg
    
# PROGRAM

# Utworzenie okna
window = psg.Window('Pomiar temperatury', programLayout, **windowInfo)

# Wyświetlnenie początkowego tekstu w oknie pomiarów
window['simMultiline'].print('Czas [HH:MM:SS]; T0 [*C]; T1 [*C]; T2 [*C]')

# Utworzenie zmiennych dla wykresów
t0_values, t1_values, t2_values = [], [], []

# Utworzenie wykresów
canvas_elem0 = window.FindElement('plotCanvas0')
canvas0 = canvas_elem0.TKCanvas
fig0 = Figure(figsize = figSize, tight_layout = True)
ax0 = fig0.add_subplot()
fig_agg0 = draw_figure(canvas0, fig0)

canvas_elem1 = window.FindElement('plotCanvas1')
canvas1 = canvas_elem1.TKCanvas
fig1 = Figure(figsize = figSize, tight_layout = True)
ax1 = fig1.add_subplot()
fig_agg1 = draw_figure(canvas1, fig1)

canvas_elem2 = window.FindElement('plotCanvas2')
canvas2 = canvas_elem2.TKCanvas
fig2 = Figure(figsize = figSize, tight_layout = True)
ax2 = fig2.add_subplot()
fig_agg2 = draw_figure(canvas2, fig2)



# Pętla okna programu
while True:
        event, values = window.read(timeout=100)    # Odczyt wartości, limit czasu 100 ms
        
        # Przycisk zamykania okna
        if event == psg.WIN_CLOSED: 
            arduino.close() # Zamknięcie połączenia z Arduino
            break
            
        # Przycisk połączenia
        if event == 'connectButton':
            port = str(window['portInputText'].Get())
            connect(port)
        # Przycisk rozłączenia   
        elif event == 'disconnectButton':
            connected = False
            
        # Przycisk zapisywania
        elif event == 'SaveButton': 
            saveFile()
        
            arduino.close()
        
        else:
            try:
                if connected == True and arduino.inWaiting() != 0:  # Sprawdzenie połączenia i informacji o oczekujących danych
                    newValue = str(arduino.readline())  # Odczyt linii danych
                    newValue = sub('[^\d\.\;\ \:]', '', newValue)   # Usunięcie nieporządanych znaków
                    print(newValue)
                    try:
                        [time, temp0, temp1, temp2] = newValue.split('; ')  # Rozdzielenie danych do odpowiednich zmiennych
                    except Exception as e:
                        print('Błąd\n' + str(e))
                    
                    # Aktualizacja stanu wyświetlaczy
                    window['outputText0'].update(value = time)
                    window['outputText1'].update(value = temp0)
                    window['outputText2'].update(value = temp1)
                    window['outputText3'].update(value = temp2)
                    
                    # Aktualizacja zmiennych dla wykresów
                    t0_values.append(float(temp0))
                    t1_values.append(float(temp1))
                    t2_values.append(float(temp2))
                    
                    
                    # Dodanie nowej wartości do okna pomiarów
                    window['simMultiline'].print(newValue)
                    
                    # Rysowanie wykresów
                    ax0.cla()   # Wyczyszczenie
                    ax0.plot(t0_values) # Wykres
                    fig_agg0.draw() # Rysowanie
                    
                    ax1.cla()
                    ax1.plot(t1_values)
                    fig_agg1.draw()
                    
                    ax2.cla()
                    ax2.plot(t2_values)
                    fig_agg2.draw()
                    
            except Exception as e:  # Obsługa błędów
                print('Błąd\n' + str(e))
            
#Zamknięcie okna
window.close


        
    
