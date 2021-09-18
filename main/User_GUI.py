import tkinter as tk
import tkinter.font as font
from tkinter import BaseWidget, Misc, ttk
from tkinter import filedialog 
from abc import ABC, abstractmethod


class Navigation:
    @staticmethod 
    def use_mouse_wheel(event):
        mainCanvas.yview_scroll(int(-1*(event.delta/120)), "units")

class WidgetInApp(ABC, BaseWidget):
    def add_mouse_wheel_interaction(self):
        self.bind('<MouseWheel>', Navigation.use_mouse_wheel)

class LabelInApp(tk.Label, WidgetInApp):
    """Label in aplication CFWDFL"""

    def __init__(self, root: Misc, row: int, column: int,\
        columspan: int = 1, txt: str = "text in label"):
        font1 = font.Font(size = 12)
        paddings = {'padx': 8, 'pady': 8}
        backgroundColor = {'bg': '#1E1E1E'}
        super().__init__(root, backgroundColor, text = txt, fg='white', font=font1, anchor='nw')
        self.grid(paddings, sticky='w', row=row, column=column, columnspan=columspan)
        self.add_mouse_wheel_interaction()
        
class ButtonInApp(tk.Button, WidgetInApp):
    """ Button in aplication CFWDFL"""

    def __init__(self, root: Misc, row: int, column: int,\
        columspan: int = 1, sticky='w', txt: str = "text on button",\
        functionApp = None):

        font1 = font.Font(size = 14)
        paddings = {'padx': 8, 'pady': 8}
        backgroundColorAndBorder = {'bg': '#403332', 'bd': 4}

        super().__init__(root, backgroundColorAndBorder, text = txt,\
            fg='white', font = font1, command = functionApp)
        self.grid(paddings, sticky=sticky, row=row, column=column, columnspan=columspan)
        self.add_mouse_wheel_interaction()

class EntryInApp(tk.Entry, WidgetInApp):
    def __init__(self, root: Misc, *args, **kwargs):
        super().__init__(root, *args, **kwargs)
        self.add_mouse_wheel_interaction()

class FrameInApp(tk.Frame, WidgetInApp):
    def __init__(self, root: Misc, *args, **kwargs):
        super().__init__(root, *args, **kwargs)
        self.add_mouse_wheel_interaction()

class LabelFrameInApp(tk.LabelFrame, WidgetInApp):
    def __init__(self, root: Misc, *args, **kwargs):
        super().__init__(root, *args, **kwargs)
        self.add_mouse_wheel_interaction()

class CheckbuttonInApp(tk.Checkbutton, WidgetInApp):
    def __init__(self, root: Misc, *args, **kwargs):
        font1 = font.Font(size = 14)
        attributes = {'padx': 8, 'pady': 8, 'bg': '#1E1E1E', 'selectcolor': '#1E1E1E',\
            'activebackground': '#1E1E1E', 'fg': 'white'}
        super().__init__(root, attributes, font = font1,  *args, **kwargs)
        self.add_mouse_wheel_interaction()

class MessageInApp(tk.Message, WidgetInApp):
    def __init__(self, root: Misc, *args, **kwargs):
        super().__init__(root, *args, **kwargs)
        self.add_mouse_wheel_interaction()

class AppliactionCFWDFL(tk.Tk):
    """Object is a aplication window
    """

    def __init__(self, backgroundColor: str = '#1E1E1E', regularFontSize: int = 12, headingFontSize: int = 14, \
        messageBoxFontSize: int = 12, paddings: dict = {'padx': 8, 'pady': 8}):
        self.backgroundColor = {'bg': backgroundColor}
        super().__init__()
        #Title of application
        self.title('CFWDFL-make imput files for LAMMPS')
        self.appname = 'CFWDFL'
        #ico
        self.iconbitmap("icon.ico")
        self.resizable(width=True, height=True)
        self.windowingsystem = 'win32'
        self.config(self.backgroundColor)
        self.geometry("1100x600")
        #fonts 
        self.regularFontSize = font.Font(size = regularFontSize)
        self.headingFontSize = font.Font(size = headingFontSize)
        self.messageBoxFontSize = font.Font(size = messageBoxFontSize)
        self.paddings = paddings
        self.createWidgets()


    def createWidgets(self) -> None:
        #czcionki w  widżetach (to można dać gdzie indizej)
        font1 = self.headingFontSize 
        font2 = self.regularFontSize
        fontmessageBox = self.messageBoxFontSize
        paddings = self.paddings 

        #kolor tła alikacji
        backgroundColor = self.backgroundColor


        '''Te funkcje trzeba jakoś wyodrębnić '''
        #funkcja pobierając ścieżkę do folderu
        def get_folder_path():
            global folder_selected
            folder_selected = filedialog.askdirectory()

        #Funkcja wykonuje program
        def make_folders():
            print(folder_selected)
        """******************************"""

        #Ramak w oknie aplikacji/pasek przewijania 
        self.mainFrame = tk.Frame(self)

        mainFrame = self.mainFrame
        mainFrame.pack(side='left', fill='both', expand=1)

        self.mainCanvas = tk.Canvas(mainFrame, backgroundColor , highlightthickness=0) #backgroundColor
        global mainCanvas
        mainCanvas = self.mainCanvas
        mainCanvas.pack(side='left', fill='both', expand=1)
        
        self.scrollBar = ttk.Scrollbar(mainFrame, orient='vertical', command=mainCanvas.yview)
        scrollBar = self.scrollBar
        scrollBar.pack(side='right', fill='y')

        mainCanvas.config(yscrollcommand=scrollBar.set)
        mainCanvas.bind('<Configure>', lambda e: mainCanvas.config(scrollregion = mainCanvas.bbox("all")))
        
        
        self.secondFrame = FrameInApp(mainCanvas, backgroundColor)
        secondFrame = self.secondFrame
        mainCanvas.create_window((0,0), window=secondFrame, anchor="nw")



        self.frame = FrameInApp(secondFrame, backgroundColor, width=600, height=300)
        self.frame.grid(column=0, row=0, columnspan=6, rowspan=11, sticky = 'NW')
        frame = self.frame
        #instrukcje
        self.instructions = LabelInApp(frame, 0, 0, 6,\
            txt="""The program creates folders with input to lammps, based on the glass oxide formula. 
            """)

        #pierwszy rząd przycisków 
        self.label1 = LabelInApp(frame, 1, 0, 3, txt = "Choose the directory "\
             "where files will they be created:")
        self.button1 = ButtonInApp(frame, 1, 3, 3, txt = "Directory", functionApp =get_folder_path)

        #drugi rząd przycisków
        self.label2 = LabelInApp(frame, 2, 0, 3, txt = "Name of folder:")
        self.input1 = EntryInApp(frame, width=20, font = font2).grid(paddings, sticky = 'w', row = 2, column = 3, columnspan=3)

        #trzeci rząd przycisków
        self.label3 = LabelInApp(frame, 3, 0, 3, txt = "Enter the prefix for subfolders:")
        self.input2 =  EntryInApp(frame, width=20, font = font2).grid(paddings, sticky = 'w', row = 3, column = 3, columnspan=3)

        oneGlass = tk.BooleanVar()
        self.checkIfOneGlass = CheckbuttonInApp(frame, text='Only one glass', variable = oneGlass, onvalue=True, offvalue=False)
        self.checkIfOneGlass.grid(paddings, row = 5, column = 0, sticky = 'w', columnspan=3)

        #instrukcja dla wzoru szkła
        self.instructions2 = MessageInApp(frame, width=800, font=fontmessageBox,
            text="Wprowadzony wzór szkła powinien być w postaci: \n" \
            "\n x Na2O ( 1 - x ) * ( 0.3 Fe2O3 0.7 P2O5 ) \n" \
            "\nPamiętaj o spacjach!\nDozwolone symbole matematyczne: +, -, *. \n" \
            "We wzorze znajdują się stosunki molowe.")

        self.instructions2.grid(paddings, row = 5, column = 3, sticky = 'w', columnspan=3)

        #czwarty rząd przycisków
        self.label4 = LabelInApp(frame, 4, 0, 3, txt = "Enter the glass equation:")
        self.inputGlassFormula =  EntryInApp(frame, width=50, font = font1)
        self.inputGlassFormula.grid(paddings, sticky = 'w', row = 4, column = 3, columnspan=3)

        #Piąty rząd przycisków
        self.labelFrame = LabelFrameInApp(frame, backgroundColor, width=600, height=25, text='If many glasses', font=font2, fg='white')
        self.labelFrame.grid(row=6, column=0, columnspan=6, rowspan=1, sticky = 'w')

        self.label5 = LabelInApp(self.labelFrame, 0, 0, txt = "initial value of x:")
        self.inputStartX =  EntryInApp(self.labelFrame, width=10, font = font2)
        self.inputStartX.grid(paddings, row = 0, column = 1, sticky = 'w')

        self.label6 = LabelInApp(self.labelFrame, 0, 2, txt = "step value:")
        self.inputStepX =  EntryInApp(self.labelFrame, width=10, font = font2)
        self.inputStepX.grid(paddings, row = 0, column = 3, sticky = 'w')

        self.label7 = LabelInApp(self.labelFrame, 0, 4, txt = "quantity of materials:")
        self.inputNumberOfSteps =  EntryInApp(self.labelFrame, width=10, font = font2)
        self.inputNumberOfSteps.grid(paddings, row = 0, column = 5, sticky = 'w')

        #Szusty rząd przycisków
        self.frame3 = FrameInApp(frame, backgroundColor,  width=600, height=25)
        self.frame3.grid(row=7, column=0, columnspan=6, rowspan=1, sticky = 'w')
        frame3 = self.frame3
        self.labelNumberOfAtoms = LabelInApp(frame3, 0, 0, txt = "quantity of atoms in single material:")
        self.inputNumberOfAtoms =  EntryInApp(frame3, width=10, font = font2)
        self.inputNumberOfAtoms.grid(paddings, row = 0, column = 2, sticky = 'w')

        self.frame4 = FrameInApp(frame, backgroundColor,  width=600, height=25)
        self.frame4.grid(row=8, column=0, columnspan=6, rowspan=1, sticky = 'w')
        self.labelDensityOfGlass = LabelInApp(self.frame4, 0, 0, txt = "list of density of glasses:")
        self.inputDensityOfGlass =  EntryInApp(self.frame4, width=50, font = font2)
        self.inputDensityOfGlass.grid(paddings, row = 0, column = 2, sticky = 'w')
        self.inputDensityOfGlass.insert(0, "eg. 3.14, 3.15")

        #Komunikaty:
        self.frame5 = FrameInApp(frame, backgroundColor,  width=600, height=40)
        self.frame5.grid(row=9, column=0, columnspan=6, rowspan=1)
        self.instructions2 = MessageInApp(self.frame5, backgroundColor, width=800, font=font2,\
            fg = 'white',\
            text="testowy")
        self.instructions2.grid(paddings, row = 9, column = 2, columnspan=2)


        #Last row of buttons 
        self.StartButton = ButtonInApp(frame, 10, 0, 3, 'E', txt = "Start", functionApp = make_folders)
        self.quitButton = ButtonInApp(frame, 10, 3, 3, txt = "Exit", functionApp = self.quit)
        self.frame6 = FrameInApp(frame, backgroundColor,  width=600, height=40)
        self.frame6.grid(row=11, column=0, columnspan=6, rowspan=1)


application = AppliactionCFWDFL()
global folder_selected
folder_selected = ''
print(folder_selected)

application.mainloop()


