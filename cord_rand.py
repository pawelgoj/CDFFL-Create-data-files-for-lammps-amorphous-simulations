
import os
import re


class IncorectFilePath(Exception):
    pass

class NumberOfItemsOnTheListOfOxidesAndCoefficientsIncorrect(Exception):
    pass

class Folder: 
    def __init__(self, path: str ='', name: str = '', prefix: str = '', nrOfFolders: int = 0):
        '''Folder class creates directory for input simulations files'''
        if path == '' or name == '' or prefix == '' or nrOfFolders == 0:
            raise IncorectFilePath('Brak ścieżki do pliku!!!')
        else:
            self.path = path
            self.name = name
            self.prefix = prefix
            self.nrOfFolders = nrOfFolders
        
    def create_folders(self) -> None:
        path = os.path.join(self.path, self.name)
        os.mkdir(path)
    
    def create_sub_folders(self) -> None:
        for i in range(1, self.nrOfFolders +1):
            fileName = self.prefix + str(i)
            path = os.path.join(self.path, self.name, fileName)
            os.mkdir(path)

class File: 
    def __init__(self, path: str=''):
        pass

class Equation_of_material: 

    def __init__(self, equation: str, manyGlasses: bool = False, nrSteps: int = 1, step: float = 0):
        self.equation = equation 
        self.step = step
        self.nrSteps = nrSteps
        self.manyGlasses = manyGlasses
        
    def get_proportions_of_oxides(self, xValue : float = 0) -> dict:

        if self.manyGlasses:
            replaced = self.equation.replace("x", str(xValue))
        else: 
            replaced = self.equation

        mathPart = re.split(r"[a-zA-Z]\S+", replaced)

        mathPartToSort = mathPart.copy()
        mathPartToSort.sort(reverse=True, key = lambda item: len(item))
        for item in mathPartToSort:
            if item != '':
                replaced = replaced.replace(str(item), ' ')
        del mathPartToSort

        tempList =[]
        for item in mathPart: 
            item = item.replace(') (', ')@@(')
            item = item.split('@@')
            tempList = tempList + item

        mathPart = []

        try:
            tempList.remove('')
        except:
            pass

        for item in tempList:
            if item.count('(') == item.count(')'):
                mathPart.append(eval(item))
            else:
                mathPart.append(item)
        
        tempList = []
        factorInFrontOfTheParenthesis = 0
        multiply = False
        for item in mathPart:
            item = str(item)
            if -1 != item.find('('):
                tempList.pop()
                multiply = True
            elif -1 != item.find(')'):
                multiply = False 
            
            if multiply:
                print('tu')
                item = item.replace('(', '')
                item = item.replace(' ', '')
                tempList.append(float(item) * factorInFrontOfTheParenthesis)
                print(item)
            else:
                try:
                    factorInFrontOfTheParenthesis = float(item)
                    tempList.append(item)
                except:
                    continue

        mathPart =  tempList.copy()
        del tempList
        textPart = replaced.split(' ')
        textPart = [item for item in textPart if item != '']  

        proportionsOfOxides = {}

        if len(textPart) == len(mathPart):
            for i in range(len(textPart)):
                proportionsOfOxides.update({textPart[i]: round(float(mathPart[i]), 6)})                
        else:
            raise NumberOfItemsOnTheListOfOxidesAndCoefficientsIncorrect('Number of items on the list of'\
                'oxides and coefficients incorrect')
    
        return proportionsOfOxides

    @staticmethod
    def get_atoms_from_oxide(oxide: str) -> dict:

        mathPart = re.split(r"[a-zA-Z]", oxide)
        textPart = re.split(r"[0-9]", oxide)

        mathPart = [item for item in mathPart if item != '']
        textPart = [item for item in textPart if item != '']

        oxideDict = {textPart[i]: round(float(mathPart[i]), 6) for i  in range(len(textPart))}
        return oxideDict

    @classmethod
    def get_proportions_of_atoms(cls,  proportionsOfOxides: dict) -> dict:

        proportionsOfAtoms = {}
        for key, value in proportionsOfOxides:
            atomDict = cls.get_atoms_from_oxide(key)
            dict = {}
            for keyAtomDict, valueAtomDict in atomDict:
                dict.update({keyAtomDict: (valueAtomDict * value)})
            atomDict = dict.copy()
            del dict
            proportionsOfAtoms.update(atomDict)


            



