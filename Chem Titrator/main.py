import numpy as np
import math
import matplotlib.pyplot as plt
import PySimpleGUI as sg

sg.theme('LightBlue5')

def MainScreen():
    layout = [ [sg.Text('Please select a calculation type')],
               [sg.Button('Titration')],
               [sg.Button('Ideal Gas Law')],
               [sg.Button('Stoichiometry')] ]

    window = sg.Window('Main Page', layout)

    while True:
        event, values = window.read()
        print(event, values)
        if event == 'Titration':
            TitrationDataInput()
            break
        if event == 'Ideal Gas Law':
            IdealGasLawInitSelect()
            break
        if event == 'Stoichiometry':
            StoichiometryInput()
            break
        if event == sg.WIN_CLOSED:
            break

def TitrationDataInput():
    print(1)

    layout1 = [ [sg.Text('Acid can be weak or strong, base will always be strong.')],
                [sg.Text('The resulting graph will have an x-axis of (mL added of Strong Base) and y-axis of pH')],
                [sg.Text('Enter Acid Concentration (M):'), sg.Input(key='-AcidConc-'), sg.Radio('Weak Acid', '+AcidSelect+', default=False, key='-WeakAcid-'), sg.Radio('Strong Acid', '+AcidSelect+', default=True, key='-StrongAcid-'), sg.Button('Select')],
                [sg.Text('Enter Acid Volume (mL):'), sg.Input(key='-AcidVol-')],
                [sg.Text('Enter Base Concentration (M):'), sg.Input(key='-BaseConc-')],
                [sg.Text('Enter Base Volume (mL):'), sg.Input(key='-BaseVol-')],
                [sg.pin(sg.Text('Enter Acid KA:', visible=False, key='-AcidKAText-')), sg.pin(sg.Input(key='-AcidKA-', visible=False))],
                [sg.Button('Calculate')] ]
    layout = layout1
    strong = True
    window = sg.Window('Data Input', layout)


    while True:
        event, values = window.read()
        print(event, values)
        if event=='Select':
            if values['-WeakAcid-']==True:
                window['-AcidKAText-'].update(visible=True)
                window['-AcidKA-'].update(visible=True)
                strong = False
                print(8)
            elif values['-StrongAcid-']==True:
                window['-AcidKAText-'].update(visible=False)
                window['-AcidKA-'].update(visible=False)
                strong = True
                print(9)
        if event == 'Calculate':
            if strong == False:
                titrationData = [float(values['-AcidConc-']), float(values['-AcidVol-']), float(values['-BaseConc-']), float(values['-BaseVol-']), float(values['-AcidKA-'])]
                TitrateWeak(titrationData)
            else:
                titrationData = [float(values['-AcidConc-']), float(values['-AcidVol-']), float(values['-BaseConc-']), float(values['-BaseVol-'])]
                TitrateStrong(titrationData)

        if event == sg.WIN_CLOSED:
            break

def TitrateStrong(tiData):
    print(3)
    y = []
    x = []
    aConc, aVol, bConc, bVol = tiData
    bVolEq = (aConc * aVol)/bConc
    #Strong Acid Final Code
    x, y = [i for i in np.arange(0, bVolEq, 0.0625)]+[float(bVolEq)]+[i for i in np.arange(math.ceil(bVolEq)+0.0625, bVol+1, 0.0625)], [-math.log((((aConc * aVol) - (bConc * i)) / (aVol + i)), 10) for i in np.arange(0, bVolEq, 0.0625)]+[float(7)]+[14 + math.log((-((aConc * aVol) - (bConc * i))) / (aVol + i), 10) for i in np.arange(math.ceil(bVolEq)+0.0625, bVol+1, 0.0625)]

    plt.plot(x, y)
    plt.show()

    layout = [[sg.Text('Do not enter the equivalence point or the program will crash.')],
              [sg.Text('Equivalence point Point: ('+str(bVolEq)+', 7)')],
              [sg.Text('Enter x value(ml):'), sg.Input(key='_input'), sg.Button('Calculate')],
              [sg.Text('pH of selected x value: '), sg.Text(key='_output')]]

    window = sg.Window('Titrate Strong', layout)

    while True:
        event, values = window.read()
        print(event, values)
        if event == sg.WIN_CLOSED:
            break
        if event == 'Calculate':
            inp = float(values['_input'])
            if inp < bVolEq:
                m = (aConc * aVol) - (bConc * inp)
                pH = -math.log((m / (aVol + inp)), 10)
                window['_output'].update(pH)
            else:
                m = (aConc * aVol) - (bConc * inp)
                pH = 14 + math.log((-m) / (aVol + inp), 10)
                window['_output'].update(pH)

def TitrateWeak(tiData):
    print(4)
    y = []
    x = []
    aConc, aVol, bConc, bVol, K = tiData
    bVolEq = (aConc * aVol) / bConc
    initPH = -math.log(math.sqrt((K * aConc)), 10)
    halfEqPoint = (aConc * aVol) / (2 * bConc)
    eqPointPH = 14 + math.log(math.sqrt(((1 * 10 ** -14) / K) * ((aConc * aVol) / (aVol + bVolEq))), 10)
#weak acid dont touch
    x, y = [float(0)] + [i for i in np.arange(0.0625, halfEqPoint, 0.0625)] + [float(halfEqPoint)] + [i for i in np.arange(math.ceil(halfEqPoint) + 0.0625, bVolEq, 0.0625)] + [float(bVolEq)] + [i for i in np.arange(math.ceil(bVolEq) + 0.0625, bVol+1, 0.0625)], [float(initPH)]+[-math.log((((math.sqrt((((bConc*i)**2) + (2*(bConc*i)*K*(aVol+i)) + (K**2)*((aVol+i)**2) + (4*K*((aConc*aVol)-(bConc*i))*(aVol+i))))-(bConc*i)-(K*(aVol+i)))/(2*(aVol+i)))), 10) for i in np.arange(0.0625, halfEqPoint, 0.0625)]+[float(-math.log(K, 10))]+[-math.log((((math.sqrt((((bConc*i)**2) + (2*(bConc*i)*K*(aVol+i)) + (K**2)*((aVol+i)**2) + (4*K*((aConc*aVol)-(bConc*i))*(aVol+i))))-(bConc*i)-(K*(aVol+i)))/(2*(aVol+i)))), 10) for i in np.arange(math.ceil(halfEqPoint) + 0.0625, bVolEq, 0.0625)]+[float(eqPointPH)]+[14 + math.log((-((aConc * aVol) - (bConc * i))) / (aVol + i), 10) for i in np.arange(math.ceil(bVolEq) + 0.0625, bVol+1, 0.0625)]

    plt.plot(x, y)
    plt.show()
    print(x)
    print(y)

    layout = [[sg.Text('Do not enter the equivalence point or half equivalence point or the program will crash.')],
              [sg.Text('Equivalence point: (' + str(bVolEq) + ', '+str(eqPointPH)+')')],
              [sg.Text('Half equivalence point: (' + str(halfEqPoint) + ', ' +str(-math.log(K, 10))+')')],
              [sg.Text('Enter x value(ml):'), sg.Input(key='_input'), sg.Button('Calculate')],
              [sg.Text('pH of selected x value: '), sg.Text(key='_output')]]

    window = sg.Window('Titrate weak', layout)

    while True:
        event, values = window.read()
        print(event, values)
        if event == sg.WIN_CLOSED:
            break
        if event == 'Calculate':
            inp = float(values['_input'])
            if inp < bVolEq:
                mT = (aConc * aVol) - (bConc * inp)
                mB = (bConc * inp)
                V = aVol + inp
                sqrtTemp = (mB ** 2) + (2 * mB * K * V) + (K ** 2) * (V ** 2) + (4 * K * mT * V)
                numTemp = math.sqrt(sqrtTemp) - mB - (K * V)
                H = numTemp / (2 * V)
                pH = -math.log((H), 10)
                window['_output'].update(pH)
            else:
                m = (aConc * aVol) - (bConc * inp)
                pH = 14 + math.log((-m) / (aVol + inp), 10)
                window['_output'].update(pH)

def IdealGasLawInitSelect():
    print(2)

    layout = [ [sg.Text("Changing state calculations are when one or more states change by a known value, and the other properties have to be calculated using proportions.")],
               [sg.Text("Constant state calculations are when you know every property except one and that property has to be calculated.")],
               [sg.Radio('Changing', '+GasLawSelect+', default=True, key='-ChangingState-'), sg.Radio('Constant', '+GasLawSelect+', default=True, key='-ConstantState-')],
               [sg.Button('Select')]]

    window = sg.Window('', layout)
    while True:
        event, values = window.read()
        print(event, values)
        if event == sg.WIN_CLOSED:
            break
        elif event == 'Select':
            if values['-ChangingState-']:
                ChangingIdealGasLaw()
                break
            else:
                ConstantIdealGasLaw()
                break

def ChangingIdealGasLaw():
    print(5)

    layout = [ [sg.Text('Enter known variables, leave unknown as 0. Will not work if more than one input is left blank.')],
               [sg.Text('Pressure 1'), sg.Input(0, key='-Pressure1-'), sg.OptionMenu(values=['atm', 'torr', 'kPa', 'psi'], default_value='atm', key='-PRESMENU1-'), sg.Text('Pressure 2'), sg.Input(0, key='-Pressure2-'), sg.OptionMenu(values=['atm', 'torr', 'kPa', 'psi'], default_value='atm', key='-PRESMENU2-')],
               [sg.Text('Volume 1'), sg.Input(0, key='-Volume1-'), sg.OptionMenu(values=['L', 'mL'], default_value='L', key='-VOLMENU1-'), sg.Text('Volume 2'), sg.Input(0, key='-Volume2-'), sg.OptionMenu(values=['L', 'mL'], default_value='L', key='-VOLMENU2-')],
               [sg.Text('Moles 1'), sg.Input(0, key='-Moles1-'), sg.OptionMenu(values=['Mol'], default_value='Mol'), sg.Text('Moles 2'), sg.Input(0, key='-Moles2-'), sg.OptionMenu(values=['Mol'], default_value='Mol')],
               [sg.Text('Temperature 1'), sg.Input(0, key='-Temperature1-'), sg.OptionMenu(values=['K', 'C', 'F'], default_value='K', key='-TEMPMENU1-'), sg.Text('Temperature 2'), sg.Input(0, key='-Temperature2-'), sg.OptionMenu(values=['K', 'C', 'F'], default_value='K', key='-TEMPMENU2-')],
               [sg.Button('Calculate')],
               [sg.Text('Output'), sg.Text(key='-Output-')] ]

    window = sg.Window('Gas law change calc', layout)

    p = True
    v = True
    n = True
    t = True

    while True:
        event, values = window.read()
        print(event, values)
        if event == sg.WIN_CLOSED:

            break

        elif event == 'Calculate':

            p1 = float(values['-Pressure1-'])
            p2 = float(values['-Pressure2-'])
            v1 = float(values['-Volume1-'])
            v2 = float(values['-Volume2-'])

            t1 = float(values['-Temperature1-'])
            t2 = float(values['-Temperature2-'])

            if float(values['-Pressure1-']) != 0: #Does conversions for pressure
                if values['-PRESMENU1-'] == 'atm':
                    p1 = float(values['-Pressure1-'])/1.0
                elif values['-PRESMENU1-'] == 'torr':
                    p1 = float(values['-Pressure1-'])/760.0
                elif values['-PRESMENU1-'] == 'kPa':
                    p1 = float(values['-Pressure1-'])/101.325
                else:
                    p1 = float(values['-Pressure1-'])/14.7
            if float(values['-Pressure2-']) != 0: #Does conversions for pressure
                if values['-PRESMENU2-'] == 'atm':
                    p2 = float(values['-Pressure2-'])/1.0
                elif values['-PRESMENU2-'] == 'torr':
                    p2 = float(values['-Pressure2-'])/760.0
                elif values['-PRESMENU2-'] == 'kPa':
                    p2 = float(values['-Pressure2-'])/101.325
                else:
                    p2 = float(values['-Pressure2-'])/14.7

            if float(values['-Volume1-']) != 0:
                if values['-VOLMENU1-'] == 'L':
                    v = float(values['-Volume1-'])/1.0
                else:
                    v = float(values['-Volume1-'])/1000.0
            if float(values['-Volume2-']) != 0:
                if values['-VOLMENU2-'] == 'L':
                    v = float(values['-Volume2-'])/1.0
                else:
                    v = float(values['-Volume2-'])/1000.0

            n1 = float(values['-Moles1-'])
            n2 = float(values['-Moles2-'])

            if float(values['-Temperature1-']) != 0:
                if values['-TEMPMENU1-'] == 'K':
                    t1 = float(values['-Temperature1-'])/1.0
                elif values['-TEMPMENU1-'] == 'C':
                    t1 = float(values['-Temperature1-'])+273
                else:
                    t1 = (5/9)*float(values['-Temperature1-']) + 273
            if float(values['-Temperature2-']) != 0:
                if values['-TEMPMENU2-'] == 'K':
                    t2 = float(values['-Temperature2-'])/1.0
                elif values['-TEMPMENU2-'] == 'C':
                    t2 = float(values['-Temperature2-'])+273
                else:
                    t2 = (5/9)*float(values['-Temperature2-']) + 273

            if float(values['-Pressure1-']) == float(values['-Pressure2-']):
                p = False
                p1 = 1
                p2 = 1
            if float(values['-Volume1-']) == float(values['-Volume2-']):
                v = False
                v1 = 1
                v2 = 1
            if float(values['-Moles1-']) == float(values['-Moles2-']):
                n = False
                n1 = 1
                n2 = 1
            if float(values['-Temperature1-']) == float(values['-Temperature2-']):
                t = False
                t1 = 1
                t2 = 1

            if float(values['-Pressure1-']) == 0 and p:
                p1 = -1
            elif float(values['-Pressure2-']) == 0 and p:
                p2 = -1
            elif float(values['-Volume1-']) == 0 and v:
                v1 = -1
            elif float(values['-Volume2-']) == 0 and v:
                v2 = -1
            elif float(values['-Moles1-']) == 0 and n:
                n1 = -1
            elif float(values['-Moles2-']) == 0 and n:
                n2 = -1
            elif float(values['-Temperature1-']) == 0 and t:
                t1 = -1
            elif float(values['-Temperature2-']) == 0 and t:
                t2 = -1

            g1 = abs(p1 * v1 * n2 * t2)
            g2 = abs(p2 * v2 * n1 * t1)

            if p1 == -1 or v1 == -1 or n2 == -1 or t2 == -1: #Actually works dont touch, only important part
                window['-Output-'].update(g2/g1)
            elif p2 == -1 or v2 == -1 or n1 == -1 or t1 == -1:
                window['-Output-'].update(g1/g2)

def ConstantIdealGasLaw():
    print(11)

    layout = [ [sg.Text('Enter known variables, leave unknown as 0. Will not work if more than one input is left blank.')],
               [sg.Text('Pressure'), sg.Input(0, key='-Pressure-'), sg.OptionMenu(values=['atm', 'torr', 'kPa', 'psi'], default_value='atm', key='-PRESMENU-')],
               [sg.Text('Volume'), sg.Input(0, key='-Volume-'), sg.OptionMenu(values=['L', 'mL'], default_value='L', key='-VOLMENU-')],
               [sg.Text('Moles'), sg.Input(0, key='-Moles-')],
               [sg.Text('Temperature'), sg.Input(0, key='-Temperature-'), sg.OptionMenu(values=['K', 'C', 'F'], default_value='K', key='-TEMPMENU-')],
               [sg.Button('Calculate')],
               [sg.Text('Output'), sg.Text(key='-Output-')] ]

    window = sg.Window('Gas Law Calc Const', layout)
    x = 'a'
    p = 0
    v = 0
    n = 0
    t = 0
    r = 0.0820574

    while True:
        event, values = window.read()
        print(event, values)
        if event == sg.WIN_CLOSED:
            break
        elif event == 'Calculate':
            if float(values['-Pressure-']) != 0:
                if values['-PRESMENU-'] == 'atm':
                    p = float(values['-Pressure-'])/1.0
                elif values['-PRESMENU-'] == 'torr':
                    p = float(values['-Pressure-'])/760.0
                elif values['-PRESMENU-'] == 'kPa':
                    p = float(values['-Pressure-'])/101.325
                else:
                    p = float(values['-Pressure-'])/14.7
            else:
                x = 1
            if float(values['-Volume-']) != 0:
                if values['-VOLMENU-'] == 'L':
                    v = float(values['-Volume-'])/1.0
                else:
                    v = float(values['-Volume-'])/1000.0
            else:
                x = 2
            if float(values['-Moles-']) != 0:
                n = float(values['-Moles-'])/1.0
            else:
                x = 3
            if float(values['-Temperature-']) != 0:
                if values['-TEMPMENU-'] == 'K':
                    t = float(values['-Temperature-'])/1.0
                elif values['-TEMPMENU-'] == 'C':
                    t = float(values['-Temperature-'])+273
                else:
                    t = (5/9)*float(values['-Temperature-']) + 273
            else:
                x = 4

        if x == 1:
            window['-Output-'].update((n*r*t)/v)
        elif x == 2:
            window['-Output-'].update((n*r*t)/p)
        elif x == 3:
            window['-Output-'].update((p*v)/(r*t))
        elif x == 4:
            window['-Output-'].update((p*v)/(n*r))

def StoichiometryInput():
    print(3)

    layout = [ [sg.Text('Please confirm settings before clicking calculate')],
               [sg.Text('Input'), sg.Input(key='-input-'), sg.OptionMenu(values=['Mass', 'Molecules', 'Moles'], default_value='Mass', key='-inputselect-')],
               [sg.pin(sg.Text('Input Molar Mass of Substance', key='-1-')), sg.pin(sg.Input(key='-subAmm-'))],
               [sg.Text('Output'), sg.Text(key='-output-'), sg.OptionMenu(values=['Mass', 'Molecules', 'Moles'], default_value='Moles', key='-outputselect-')],
               [sg.Button('Confirm Settings')],
               [sg.Button('Calculate')] ]

    window = sg.Window('', layout)
    subA = 0
    subB = 0
    while True:
        event, values = window.read()
        print(event, values)
        if event == sg.WIN_CLOSED:
            break

        if event == 'Confirm Settings':
            if values['-inputselect-'] == 'Moles' and values['-outputselect-'] == 'Moles':
                window['-1-'].update('Input moles of above/moles of below in fraction form')
            else:
                window['-1-'].update('Input Molar Mass of Substance')

        if event == 'Calculate':
            if values['-inputselect-'] == 'Moles':
                subA = float(values['-input-'])
            elif values['-inputselect-'] == 'Mass':
                subA = float(values['-input-'])/float(values['-subAmm-'])
            elif values['-inputselect-'] == 'Molecules':
                subA = float(values['-input-'])/602200000000000000000000.0
            if values['-outputselect-'] == 'Moles':
                subB = subA/float(values['-subAmm-'])
            elif values['-outputselect-'] == 'Mass':
                subB = subA * float(values['-subAmm-'])
            elif values['-outputselect-'] == 'Molecules':
                subB = subA * 602200000000000000000000.0

            window['-output-'].update(subB)

MainScreen()