# Layout dla interfejsu
import PySimpleGUI as psg

windowInfo = {'element_justification':'left', 'finalize':'True'}
inputTextSize = (25, 1)
labelSize = (25, 1)
labelSize2 = (10, 1)
multilineSize = (40, 8)
outputTextInfo = {'size':(8, 1), 'text_color':'white', 'font':('Arial', 18)}
saveTextBoxSize = (20, 1)
plotCanvasInfo = {'background_color':'white'}
figSize = [3.5, 3.5]
defaultTime = 5
columnInfo = {'vertical_alignment':'top'}

programLayout = [
    [psg.Text('Czas [hh:mm:ss] =', font=outputTextInfo['font'], text_color=outputTextInfo['text_color']), psg.Text(**outputTextInfo, key = 'outputText0')],  
    [psg.Column([
        # Liczniki i wykresy
        [psg.Column([
            [psg.Canvas(key = 'plotCanvas0', **plotCanvasInfo)],
            [psg.Text('T0 [°C] =', **outputTextInfo), psg.Text(**outputTextInfo, key = 'outputText1')]   ]),
        psg.Column([   
            [psg.Canvas(key = 'plotCanvas1', **plotCanvasInfo)],
            [psg.Text('T1 [°C] =', **outputTextInfo), psg.Text(**outputTextInfo, key = 'outputText2')]   ]),
        psg.Column([   
            [psg.Canvas(key = 'plotCanvas2', **plotCanvasInfo)],
            [psg.Text('T2 [°C] = ', **outputTextInfo), psg.Text(**outputTextInfo, key = 'outputText3')]   ])  ],
    ])],

    [psg.Column(**columnInfo, layout=[
        [psg.Column(**columnInfo, layout=[
                [psg.Text('Pomiary', key='simText1')],
                [psg.Multiline(key = 'simMultiline', size=multilineSize, disabled = False, autoscroll = True)]
            ]),
            # Pola do zapisywania
            psg.Column(**columnInfo, layout=[
                [psg.Text('Zapis', labelSize)],
                [psg.InputText(key = 'fileInputText', size = saveTextBoxSize),psg.FileSaveAs('Szukaj', default_extension='.csv', enable_events=True, key='saveAsButton')],
                [psg.Checkbox('Zamiana kropek na przecinki', key = 'comaCheckBox')],
                [psg.Button('Zapisz', key='saveButton')]
            ])
        ]
    ]),
    # Czas i wybór portu    
    psg.Column(**columnInfo, layout=[
        [psg.Column(**columnInfo, layout=[
            [psg.Text('Port', labelSize)],
            [psg.Combo(values=[], key='portList', size = labelSize)], 
            [psg.Button('Odśwież urządzenia', key='portRefreshButton', size=labelSize)],
            [psg.Text('Częstotliwość pomiaru [s]', labelSize)], 
            [psg.InputText(default_text = defaultTime, key = 'timeInputText', size = inputTextSize)],
            [psg.Button('Połącz', key = 'connectButton'), psg.Button('Rozłącz', key = 'disconnectButton')]
        ]),
        psg.Column(**columnInfo, layout=[
            [psg.Button('Pomoc', key='helpButton', size=(25,5))]
        ])
        ],        
    ])
    ]
]
