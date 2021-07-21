from cord_rand import *
import tkinter as tk
import tkinter.font as font
from tkinter.filedialog import askopenfile

class LabelInApp(tk.Label):
    """Label in aplication CFWDFL"""

    def __init__(self, root: object, row: int, column: int, columspan: int = 1, txt: str = "Tu wpisz text.") -> object:
        font1 = font.Font(size = 12)
        paddings = {'padx': 10, 'pady': 10}
        backgroundColor = {'bg': '#1E1E1E'}
        super().__init__()
        label = tk.Label(root, backgroundColor, text = txt, fg='white', font=font1)\
            .grid(paddings, sticky='w', row=row, column=column, columnspan=columspan)

class ButtonInApp(tk.Button):
    """ Button in aplication CFWDFL"""
    def __init__(self, root: object, row: int, column: int, columspan: int = 1, sticky='w', txt: str = "Tu wpisz text.", functionApp: object = None) -> object:
        font1 = font.Font(size = 14)
        paddings = {'padx': 10, 'pady': 10}
        backgroundColorAndBorder = {'bg': '#1D375C', 'bd': 4}

        super().__init__()
        self = tk.Button(root, backgroundColorAndBorder, text = txt, fg='white', font = font1, command = functionApp)\
            .grid(paddings, sticky=sticky, row=row, column=column, columnspan=columspan)


class AppliactionCFWDFL(tk.Tk):
    """Object is a aplication window
    """
    def __init__(self) -> object:
        backgroundColor = {'bg': '#1E1E1E'}
        super().__init__()
        #Title of application
        self.title('CFWDFL-make imput files from LAMMPS')
        self.appname = 'CFWDFL'
        #ico
        self.iconbitmap('Bez nazwy.ico')
        self.resizable(width=True, height=True)
        self.windowingsystem = 'win32'
        self.configure(backgroundColor)
        #self.tk_setPalette(backgroundm = 'red')
        self.createWidgets()

    def createWidgets(self) -> None:
        #czcionki w  widżetach 
        font1 = font.Font(size = 18)
        font2 = font.Font(size = 14)

        paddings = {'padx': 10, 'pady': 10} 

        #kolor tła alikacji
        backgroundColor = {'bg': '#1E1E1E'}

        #Ramak w oknie aplikacji 
        self.frame = tk.Frame(self, backgroundColor, width=600, height=300)\
            .grid(columnspan=6, rowspan=6)
        frame = self.frame

        #pierwszy rząd przycisków 
        self.label1 = LabelInApp(frame, 0, 0, 3, txt = "Znajdź katalog w którym "\
             "mają być zapisane dane:")
        self.button1 = ButtonInApp(frame, 0, 3, 3, txt = "Wskaż katalog")

        #drugi rząd przycisków
        self.label2 = LabelInApp(frame, 1, 0, 3, txt = "Twoja nazwa folderu:")
        self.input1 = tk.Entry(frame, width=20, font = font2).grid(paddings, sticky = 'w', row = 1, column = 3, columnspan=3)

        #trzeci rząd przycisków
        self.label3 = LabelInApp(frame, 2, 0, 3, txt = "Wpisz prefix dla podfolderów:")
        self.input2 = tk.Entry(frame, width=20, font = font2).grid(paddings, sticky = 'w', row = 2, column = 3, columnspan=3)

        #czwarty rząd przycisków
        self.label4 = LabelInApp(frame, 3, 0, 3, txt = "Podaj wzór szkła:")
        self.inputGlassFormula = tk.Entry(frame, width=50, font = font1)\
            .grid(paddings, sticky = 'w', row = 3, column = 3, columnspan=3)

        #Piąty rząd przycisków
        self.frame2 = tk.Frame(frame, backgroundColor,  width=600, height=25)\
            .grid(row=4, column=0, columnspan=6, rowspan=1)
        frame2 = self.frame2
        self.label5 = LabelInApp(frame2, 4, 0, txt = "Poczatkowa wartość x:")
        self.inputStartX = tk.Entry(frame2, width=10, font = font2).grid(paddings, row = 4, column = 1, sticky = 'w')
        self.label6 = LabelInApp(frame2, 4, 2, txt = "Poczatkowa wartość x:")
        self.inputStepX = tk.Entry(frame2, width=10, font = font2).grid(paddings, row = 4, column = 3, sticky = 'w')
        self.label7 = LabelInApp(frame2, 4, 4, txt = "Poczatkowa wartość x:")
        self.inputNumberOfSteps = tk.Entry(frame2, width=10, font = font2).grid(paddings, row = 4, column = 5, sticky = 'w')

        #Szusty rząd przycisków


        #ostatni rząd przycisków 
        self.StartButton = ButtonInApp(frame, 6, 0, 3, 'E', txt = "Start")
        self.quitButton = ButtonInApp(frame, 6, 3, 3, txt = "Zakończ", functionApp = self.quit)


application = AppliactionCFWDFL()
application.mainloop()


