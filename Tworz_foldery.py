import cord_rand 
import tkinter as tk
import tkinter.font as font
from tkinter import ttk
from tkinter import filedialog 




class LabelInApp(tk.Label):
    """Label in aplication CFWDFL"""

    def __init__(self, root: object, row: int, column: int,\
        columspan: int = 1, txt: str = "text in label"):

        font1 = font.Font(size = 12)
        paddings = {'padx': 10, 'pady': 10}
        backgroundColor = {'bg': '#1E1E1E'}

        super().__init__()
        self = tk.Label(root, backgroundColor, text = txt, fg='white', font=font1, anchor='nw')
        self.grid(paddings, sticky='w', row=row, column=column, columnspan=columspan)

class ButtonInApp(tk.Button):
    """ Button in aplication CFWDFL"""

    def __init__(self, root: object, row: int, column: int,\
        columspan: int = 1, sticky='w', txt: str = "text on button",\
        functionApp: object = None):

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

    def __init__(self):
        backgroundColor = {'bg': '#1E1E1E'}
        super().__init__()
        #Title of application
        self.title('CFWDFL-make imput files for LAMMPS')
        self.appname = 'CFWDFL'
        #ico
        self.iconbitmap('Bez nazwy.ico')
        self.resizable(width=True, height=True)
        self.windowingsystem = 'win32'
        self.config(backgroundColor)
        self.geometry("1050x600")
        self.createWidgets()

    def createWidgets(self) -> None:
        #czcionki w  widżetach 
        font1 = font.Font(size = 18)
        font2 = font.Font(size = 14)
        fontmessageBox = font.Font(size = 12)

        paddings = {'padx': 10, 'pady': 10} 

        #kolor tła alikacji
        backgroundColor = {'bg': '#1E1E1E'}

        #funkcja pobierając ścieżkę do folderu
        def get_folder_path():
            global folder_selected
            folder_selected = filedialog.askdirectory()

        #Funkcja wykonuje program
        def make_folders():
            print(folder_selected)



        #Ramak w oknie aplikacji/pasek przewijania 

        self.mainFrame = tk.Frame(self, backgroundColor)

        mainFrame = self.mainFrame
        mainFrame.pack(side='left', fill='both', expand=1)

        self.mainCanvas = tk.Canvas(mainFrame, backgroundColor, highlightthickness=0)
        mainCanvas = self.mainCanvas
        mainCanvas.pack(side='left', fill='both', expand=1)
        
        self.scrollBar = ttk.Scrollbar(mainFrame, orient='vertical', command=mainCanvas.yview)
        scrollBar = self.scrollBar
        scrollBar.pack(side='right', fill='y')

        mainCanvas.config(yscrollcommand=scrollBar.set)
        mainCanvas.bind('<Configure>', lambda e: mainCanvas.config(scrollregion = mainCanvas.bbox("all")))
        
        self.secondFrame = tk.Frame(mainCanvas, backgroundColor)
        secondFrame = self.secondFrame
        mainCanvas.create_window((0,0), window=secondFrame, anchor="nw")



        self.frame = tk.Frame(secondFrame, backgroundColor, width=600, height=300)
        self.frame.grid(column=0, row=0, columnspan=6, rowspan=8, sticky = 'NW')
        frame = self.frame
        
        #instrukcje
        self.instructions = LabelInApp(frame, 0, 0, 6,\
            txt="""The program creates folders with input to lammpsa, based on the glass oxide formula. 
            """)


        #pierwszy rząd przycisków 
        self.label1 = LabelInApp(frame, 1, 0, 3, txt = "Choose the directory "\
             "where the files are to be created:")
        self.button1 = ButtonInApp(frame, 1, 3, 3, txt = "Directory", functionApp =get_folder_path)

        #drugi rząd przycisków
        self.label2 = LabelInApp(frame, 2, 0, 3, txt = "Your name of folder:")
        self.input1 = tk.Entry(frame, width=20, font = font2).grid(paddings, sticky = 'w', row = 2, column = 3, columnspan=3)

        #trzeci rząd przycisków
        self.label3 = LabelInApp(frame, 3, 0, 3, txt = "Enter the prefix for subfolders:")
        self.input2 = tk.Entry(frame, width=20, font = font2).grid(paddings, sticky = 'w', row = 3, column = 3, columnspan=3)

        #instrukcja dla wzoru szkła
        self.instructions2 = tk.Message(frame, width=800, font=fontmessageBox,
            text="Wprowadzony wzór szkła powinien być w postaci: \n" \
            "\n x Na2O ( 1 - x ) * ( 0.3 Fe2O3 0.7 P2O5 ) \n" \
            "\nPamiętaj o spacjach!\nDozwolone symbole matematyczne: +, -, *. \n" \
            "We wzorze znajdują się stosunki molowe.")

        self.instructions2.grid(paddings, row = 5, column = 3, sticky = 'w', columnspan=3)

        #czwarty rząd przycisków
        self.label4 = LabelInApp(frame, 4, 0, 3, txt = "Enter the glass equation:")
        self.inputGlassFormula = tk.Entry(frame, width=50, font = font1)
        self.inputGlassFormula.grid(paddings, sticky = 'w', row = 4, column = 3, columnspan=3)

        #Piąty rząd przycisków
        self.frame2 = tk.Frame(frame, backgroundColor,  width=600, height=25)
        self.frame2.grid(row=6, column=0, columnspan=6, rowspan=1, sticky = 'w')
        frame2 = self.frame2

        self.label5 = LabelInApp(frame2, 0, 0, txt = "initial value of x:")
        self.inputStartX = tk.Entry(frame2, width=10, font = font2)
        self.inputStartX.grid(paddings, row = 0, column = 1, sticky = 'w')

        self.label6 = LabelInApp(frame2, 0, 2, txt = "step value:")
        self.inputStepX = tk.Entry(frame2, width=10, font = font2)
        self.inputStepX.grid(paddings, row = 0, column = 3, sticky = 'w')

        self.label7 = LabelInApp(frame2, 0, 4, txt = "quantity of materials:")
        self.inputNumberOfSteps = tk.Entry(frame2, width=10, font = font2)
        self.inputNumberOfSteps.grid(paddings, row = 0, column = 5, sticky = 'w')

        #Szusty rząd przycisków
        self.frame3 = tk.Frame(frame, backgroundColor,  width=600, height=25)
        self.frame3.grid(row=7, column=0, columnspan=6, rowspan=1, sticky = 'w')
        frame3 = self.frame3
        self.labelNumberOfAtoms = LabelInApp(frame3, 0, 0, txt = "quantity of atoms in single material:")
        self.inputNumberOfAtoms = tk.Entry(frame3, width=10, font = font2)
        self.inputNumberOfAtoms.grid(paddings, row = 0, column = 2, sticky = 'w')

        #Komunikaty:
        self.frame4 = tk.Frame(frame, backgroundColor,  width=600, height=40)
        self.frame4.grid(row=8, column=0, columnspan=6, rowspan=1)
        frame4 = self.frame4
        self.instructions2 = tk.Message(frame4, backgroundColor, width=800, font=font2,\
            fg = 'white',\
            text="testowy")
        self.instructions2.grid(paddings, row = 8, column = 2, columnspan=2)


        #ostatni rząd przycisków 
        self.StartButton = ButtonInApp(frame, 9, 0, 3, 'E', txt = "Start", functionApp = make_folders)
        self.quitButton = ButtonInApp(frame, 9, 3, 3, txt = "Exit", functionApp = self.quit)
        self.frame5 = tk.Frame(frame, backgroundColor,  width=600, height=40)
        self.frame5.grid(row=10, column=0, columnspan=6, rowspan=1)


application = AppliactionCFWDFL()
global folder_selected
folder_selected = ''
print(folder_selected)

application.mainloop()


