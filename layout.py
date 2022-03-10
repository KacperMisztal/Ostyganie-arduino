# Layout dla interfejsu
import PySimpleGUI as psg
import manual

windowInfo = {'element_justification':'left', 'finalize':'True'}
inputTextSize = (25, 1)
labelSize = (25, 1)
labelSize2 = (10, 1)
multilineSize = (40, 14)
outputTextInfo = {'size':(8, 1), 'background_color':'black', 'text_color':'red', 'font':('Arial', 20), 'justification':'right'}
saveTextBoxSize = (19, 1)
plotCanvasInfo = {'background_color':'white'}
figSize = [3.5, 3.5]
defaultTime = 5

programLayout = [  
    # Lewa kolumna
    [psg.Column([
        # Liczniki i wykresy
        [psg.Column([
            [psg.Column([
                [psg.Text('Czas [HH:MM:SS]')],
                [psg.Text(**outputTextInfo, key = 'outputText0')]
            ]),
            psg.Column([
                    [psg.Text('T0 [*C]')],
                    [psg.Text(**outputTextInfo, key = 'outputText1')]
            ])],   
            [psg.Canvas(key = 'plotCanvas0', **plotCanvasInfo)]   ]),
        psg.Column([   
            [psg.Text('T1 [*C]')],
            [psg.Text(**outputTextInfo, key = 'outputText2')],
            [psg.Canvas(key = 'plotCanvas1', **plotCanvasInfo)]   ]),
        psg.Column([   
            [psg.Text('T2 [*C]')],
            [psg.Text(**outputTextInfo, key = 'outputText3')],
            [psg.Canvas(key = 'plotCanvas2', **plotCanvasInfo)]   ])  ],
    ])],
        
    [psg.Column([   
        # Lista zebranych danych 
        [psg.Text('Pomiary', key='simText1')],
        [psg.Multiline(key = 'simMultiline', size=multilineSize, disabled = False, autoscroll = True)]
    ]),
    
    # Wybór portu
    psg.Column([
        [psg.Text('Port', labelSize)],
        [psg.Combo(values=[], key='portList', size = labelSize), psg.Button('Odśwież', key='portRefreshButton')],
        [psg.Text('Częstotliwość pomiaru [s]', labelSize)], 
        [psg.InputText(default_text = defaultTime, key = 'timeInputText', size = inputTextSize)],
        [psg.Button('Połącz', key = 'connectButton'), psg.Button('Rozłącz', key = 'disconnectButton')],
        # Pola do zapisywania
        [psg.Text('Zapis', labelSize)],
        [psg.Text('Nazwa: ', size=labelSize2), psg.InputText(key = 'fileInputText', size = saveTextBoxSize), psg.FolderBrowse('Szukaj', key = 'browseButton')],
        [psg.Checkbox('Zamiana kropek na przecinki', key = 'comaCheckBox'), psg.Button('Zapisz', key = 'SaveButton')]
    ]),
    psg.Column([
        [psg.Text(manual.ostyganie_man)]
    ])  ]
]