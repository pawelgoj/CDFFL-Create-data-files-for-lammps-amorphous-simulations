
import os
import re
from fractions import Fraction


class IncorectFilePath(Exception):
    pass

class NumberOfItemsOnTheListOfOxidesAndCoefficientsIncorrect(Exception):
    pass

class constants:
    listOfAnions = ['F', 'O', 'Cl', 'Br', 'I', 'C', 'B']

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

class EquationOfMaterial: 

    def __init__(self, equation: str, manyGlasses: bool = False, xValue: float = 0):
        self.equation = equation 
        self.manyGlasses = manyGlasses
        self.xValue = xValue
        
    def get_proportions_of_oxides(self) -> dict:

        if self.manyGlasses:
            replaced = self.equation.replace("x", str(self.xValue))
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
    def remove_empty_list_elements(list: list) -> list:
        return [item for item in list if item != '']

    @staticmethod
    def round_math_part(number) -> float:
        return round(float(number), 6)
    
    @staticmethod
    def calculate_ratios(dictionary: dict) -> dict:
        
        for value in dictionary.values():
            try:
                sum = sum + value[0]
            except: 
                sum = value[0] 
        
        for key in dictionary.keys():
            dictionary[key][0] = EquationOfMaterial.round_math_part(dictionary[key][0] / sum)

        return dictionary

   
    @classmethod
    def calculate_atoms_from_oxide(cls, oxide: str) -> dict:
        def check_cation_or_anion(positionInOxideformula: int) -> str:
            if positionInOxideformula == 0:
                return 'Cation'
            elif positionInOxideformula == 1:
                return 'Anion'  
            else:
                raise Exception('You can use only simple compound oxide notation eg. Fe2O3 also SiC is correct')  

        
        mathPart = re.split(r"[a-zA-Z]", oxide)
        textPart = re.split(r"[0-9]", oxide)

        mathPart = cls.remove_empty_list_elements(mathPart)
        textPart = cls.remove_empty_list_elements(textPart)


        if mathPart != [] and len(mathPart) == len(textPart) and len(mathPart) > 1:
            oxideDict = {}
            for i in range(len(textPart)):
                if check_cation_or_anion(i) == 'Cation': 
                    oxideDict.update({textPart[i]: (cls.round_math_part(mathPart[i]), check_cation_or_anion(i), textPart[i+1],\
                        Fraction(int(mathPart[i+1]), int(mathPart[i])))})
                elif check_cation_or_anion(i) == 'Anion':
                    oxideDict.update({textPart[i]: (cls.round_math_part(mathPart[i]), check_cation_or_anion(i))})
                else:
                    raise Exception('Wrong oxide notation!!!!')
        else:
            tempDict = {}
            for item in textPart:
                i = 0
                for character in item:
                    if character.isupper() and i != 0:
                        beforeCharacter = item[:i]
                        afterCharacter = item[i:]
                        if afterCharacter != '' and mathPart == []:
                            tempDict.update({beforeCharacter: (1, 'Cation', afterCharacter, Fraction(1, 1))})
                            tempDict.update({afterCharacter: (1, 'Anion')})
                        elif len(mathPart) == 1:
                            tempDict.update({beforeCharacter: (1, 'Cation', afterCharacter, Fraction(int(mathPart[0]), 1))})
                            tempDict.update({afterCharacter: (cls.round_math_part(mathPart[0]), check_cation_or_anion(1))})
                        else: 
                            raise Exception('Wrong oxide name!')
                    i+=1 
            if tempDict != {}: 
                oxideDict = tempDict.copy()
            else: 
                mathPart.append(1)
                oxideDict = {}
                for i in range(len(textPart)):
                    if check_cation_or_anion(i) == 'Cation': 
                        oxideDict.update({textPart[i]: (cls.round_math_part(mathPart[i]), check_cation_or_anion(i), textPart[i+1],\
                            Fraction(int(mathPart[i+1]), int(mathPart[i])))})
                    elif check_cation_or_anion(i) == 'Anion':
                        oxideDict.update({textPart[i]: (cls.round_math_part(mathPart[i]), check_cation_or_anion(i))})
                    else:
                        raise Exception('Wrong oxide notation!!!!')

            del tempDict

        return oxideDict

    @classmethod
    def calculate_proportions_of_atoms(cls,  proportionsOfOxides: dict) -> dict:

        proportionsOfAtoms = {}
        for key in proportionsOfOxides.keys():
            atomDict = cls.calculate_atoms_from_oxide(key)
            dict = {}
            for keyAtomDict in atomDict.keys():
                dict.update({keyAtomDict: [atomDict[keyAtomDict][0] * proportionsOfOxides[key], *atomDict[keyAtomDict][1:]]})
            atomDict = dict.copy()
            del dict


            for key in atomDict.keys():
                if key in proportionsOfAtoms.keys():
                    if atomDict[key][1] == 'Anion':
                        proportionsOfAtoms[key][0] = proportionsOfAtoms[key][0] + atomDict[key][0]
                    else:
                        raise Exception(f'Atom {key} in two different oxidation states')
                else:
                    proportionsOfAtoms[key] = atomDict[key]
            
        
        proportionsOfAtoms = cls.calculate_ratios(proportionsOfAtoms)
        
        return proportionsOfAtoms


    def get_proportion_of_atoms(self) -> dict:
        proportionsOfOxides = self.get_proportions_of_oxides()
        proportionsOfAtoms = EquationOfMaterial.calculate_proportions_of_atoms(proportionsOfOxides)
        return proportionsOfAtoms
            
class CompositionOfMaterial:
    def __init__(self ):
        pass

