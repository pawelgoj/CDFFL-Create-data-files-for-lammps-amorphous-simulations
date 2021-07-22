from cord_rand import *
import tkinter as tk
import tkinter.font as font
from tkinter import ttk
from tkinter.filedialog import askopenfile

class LabelInApp(tk.Label):
    """Label in aplication CFWDFL"""

    def __init__(self, root: object, row: int, column: int,\
        columspan: int = 1, txt: str = "Tu wpisz text.") -> object:

        font1 = font.Font(size = 12)
        paddings = {'padx': 10, 'pady': 10}
        backgroundColor = {'bg': '#1E1E1E'}

        super().__init__()
        self = tk.Label(root, backgroundColor, text = txt, fg='white', font=font1, anchor='nw')
        self.grid(paddings, sticky='w', row=row, column=column, columnspan=columspan)

class ButtonInApp(tk.Button):
    """ Button in aplication CFWDFL"""

    def __init__(self, root: object, row: int, column: int,\
        columspan: int = 1, sticky='w', txt: str = "Tu wpisz text.",\
        functionApp: object = None) -> object:

        font1 = font.Font(size = 14)
        paddings = {'padx': 10, 'pady': 10}
        backgroundColorAndBorder = {'bg': '#1D375C', 'bd': 4}

        super().__init__()
        self = tk.Button(root, backgroundColorAndBorder, text = txt,\
            fg='white', font = font1, command = functionApp)
        self.grid(paddings, sticky=sticky, row=row, column=column, columnspan=columspan)


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
        self.config(backgroundColor)

        self.createWidgets()

    def createWidgets(self) -> None:
        #czcionki w  widżetach 
        font1 = font.Font(size = 18)
        font2 = font.Font(size = 14)
        fontmessageBox = font.Font(size = 12)

        paddings = {'padx': 10, 'pady': 10} 

        #kolor tła alikacji
        backgroundColor = {'bg': '#1E1E1E'}



        #Ramak w oknie aplikacji/pasek przewijania 
        
        self.scrollBar = ttk.Scrollbar(self, orient='vertical')\
            .grid(column=7, row=0, rowspa=8, sticky='ns')
        #yscrollcommand = scrollBar.set)\
        '''self.frame = tk.Canvas(self, backgroundColor, width=600, height=300)\
            .grid(column=0, row=0, columnspan=6, rowspan=8, sticky = 'NW')
        frame = self.frame
        self.scrollBar.config(command=canvas.yview)'''
    


           
        self.frame = tk.Frame(self, backgroundColor, width=600, height=300)
        self.frame.grid(column=0, row=0, columnspan=6, rowspan=8, sticky = 'NW')
        frame = self.frame
        
        

        #instrukcje
        self.instructions = LabelInApp(frame, 0, 0, 6,\
            txt="""Program tworzy foldery z danymi wejściowymi do lammpsa, na podstawie wzoru tlenkowego szkła. 
            """)


        #pierwszy rząd przycisków 
        self.label1 = LabelInApp(frame, 1, 0, 3, txt = "Znajdź katalog w którym "\
             "mają być zapisane dane:")
        self.button1 = ButtonInApp(frame, 1, 3, 3, txt = "Wskaż katalog")

        #drugi rząd przycisków
        self.label2 = LabelInApp(frame, 2, 0, 3, txt = "Twoja nazwa folderu:")
        self.input1 = tk.Entry(frame, width=20, font = font2).grid(paddings, sticky = 'w', row = 2, column = 3, columnspan=3)

        #trzeci rząd przycisków
        self.label3 = LabelInApp(frame, 3, 0, 3, txt = "Wpisz prefix dla podfolderów:")
        self.input2 = tk.Entry(frame, width=20, font = font2).grid(paddings, sticky = 'w', row = 3, column = 3, columnspan=3)

        #instrukcja dla wzoru szkła
        self.instructions2 = tk.Message(frame, width=800, font=fontmessageBox,
            text="Wprowadzony wzór szkła powinien być w postaci: \n" \
            "\n x Na2O ( 1 - x ) * ( 0.3 Fe2O3 0.7 P2O5 ) \n" \
            "\nPamiętaj o spacjach!\nDozwolone symbole matematyczne: +, -, *. \n" \
            "We wzorze znajdują się stosunki molowe.")

        self.instructions2.grid(paddings, row = 5, column = 3, sticky = 'w', columnspan=3)

        #czwarty rząd przycisków
        self.label4 = LabelInApp(frame, 4, 0, 3, txt = "Podaj wzór szkła:")
        self.inputGlassFormula = tk.Entry(frame, width=50, font = font1)
        self.inputGlassFormula.grid(paddings, sticky = 'w', row = 4, column = 3, columnspan=3)

        #Piąty rząd przycisków
        self.frame2 = tk.Frame(frame, backgroundColor,  width=600, height=25)
        self.frame2.grid(row=6, column=0, columnspan=6, rowspan=1, sticky = 'w')
        frame2 = self.frame2
        self.label5 = LabelInApp(frame2, 0, 0, txt = "Poczatkowa wartość x:")
        self.inputStartX = tk.Entry(frame2, width=10, font = font2)
        self.inputStartX.grid(paddings, row = 0, column = 1, sticky = 'w')
        self.label6 = LabelInApp(frame2, 0, 2, txt = "Wartość kroku:")
        self.inputStepX = tk.Entry(frame2, width=10, font = font2)
        self.inputStepX.grid(paddings, row = 0, column = 3, sticky = 'w')
        self.label7 = LabelInApp(frame2, 0, 4, txt = "ilość szkieł:")
        self.inputNumberOfSteps = tk.Entry(frame2, width=10, font = font2)
        self.inputNumberOfSteps.grid(paddings, row = 0, column = 5, sticky = 'w')

        #Komunikaty:
        self.frame3 = tk.Frame(frame, backgroundColor,  width=600, height=40)
        self.frame3.grid(row=7, column=0, columnspan=6, rowspan=1)
        frame3 = self.frame3
        self.instructions2 = tk.Message(frame3, backgroundColor, width=800, font=font2, fg = 'white',\
            text="testowy")
        self.instructions2.grid(paddings, row = 7, column = 2, columnspan=2)


        #ostatni rząd przycisków 
        self.StartButton = ButtonInApp(frame, 8, 0, 3, 'E', txt = "Start")
        self.quitButton = ButtonInApp(frame, 8, 3, 3, txt = "Zakończ", functionApp = self.quit)
        self.frame4 = tk.Frame(frame, backgroundColor,  width=600, height=40)
        self.frame4.grid(row=9, column=0, columnspan=6, rowspan=1)


application = AppliactionCFWDFL()
application.mainloop()


