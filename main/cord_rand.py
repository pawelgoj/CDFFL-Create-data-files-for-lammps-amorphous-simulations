import os
import re
import json
from fractions import Fraction
from random import random

#TODO implement App class
class App:
    def __init__(self):
        self.directory = ''


    def set_directory(self, directory):
        self.directory = directory


    def make_folders_with_data_for_lammps(self, nameOfFolder: str, prefixSubFolder: str, equation: str, manyGlasses: bool,
        atomsInSingleMaterial: int, strDensityList: str, strCharges: str, initX: float = 0, stepX: float = 0, quantityOfMaterials: int = 1):

        nrOfFolders = quantityOfMaterials
    
        folder = Folder(self.directory, nameOfFolder, prefixSubFolder, nrOfFolders)
        folder.create_folders()
        subfoldersPaths = folder.create_sub_folders()

        materialsList = MaterialsList(EquationOfMaterial, CompositionOfMaterial,
        manyGlasses, equation, initX, stepX, atomsInSingleMaterial,
        strDensityList, strCharges, quantityOfMaterials, file = 'AtomMass.json')

        charges = materialsList.get_charges()
        materialsList, atomsMasses = materialsList.get_materials_list_and_atom_masses_dict()

        filesForLammps = FilesForLammps(FileForLammps, subfoldersPaths, prefixSubFolder , materialsList, atomsMasses, charges)
        filesForLammps.make_files()



class FilesForLammps:
    def __init__(self, FileForLammps: type, subfoldersPaths: list, prefixSubFolder: str, materialsList: list, atomsMasses: dict, charges: dict):
        
        self.FileForLammps = FileForLammps
        self.prefixSubFolder = prefixSubFolder
        self.subfoldersPaths = subfoldersPaths
        self.materialsList = materialsList
        self.charges = charges
        self.atomsMasses = atomsMasses
        self.FileForLammps = FileForLammps

    def make_files(self):
        i = 0
        for subfolderPath in self.subfoldersPaths:
            name = self.prefixSubFolder + f"{i+1}"
            
            material = self.materialsList[i]
            file = self.FileForLammps(name, material, self.charges, self.atomsMasses, subfolderPath)
            file.create_complete_file()
            i+= 1


class FileForLammps:
    def __init__(self, name: str, material: dict, charges: dict, atomMasses: dict, subfolderPath: str):
        self.path = f'{subfolderPath}\\{name}'
        self.name = name 

        if len(charges) != len(atomMasses):
            raise Exception('length of charges dict != length of atom masses dict')

        temporary_atomMasses = atomMasses.copy()
        temporary_charges = charges.copy()
        for id, atom in enumerate(charges.keys(), 1):
            temporary_charges[atom] = {'id': id, 'charge': charges[atom]}
            temporary_atomMasses[atom] = {'id': id, 'mass': atomMasses[atom]}


        self.length_of_simulation_box_edge = round(material['volume'] ** (1/3), 6)
        self.charges = temporary_charges
        self.atomMasses = temporary_atomMasses
        self.quantity = material['quantityOfAtoms']
        self.composition = material['composition'].copy()

    def crate_file_with_title(self):
        with open(f'{self.path}.txt', 'x') as file:
            file.write(f'#{self.name}\n\n')

    def write_quantity_of_atoms(self):
        with open(f'{self.path}.txt', 'a') as file:
            file.write(f'{self.quantity} atoms\n\n')
    
    def write_number_of_atom_types(self):
        numberOfAtomsTypes = len(self.composition)
        with open(f'{self.path}.txt', 'a') as file:
            file.write(f'{numberOfAtomsTypes} atom types\n\n')
 
    def write_system_coordinates(self):
        with open(f'{self.path}.txt', 'a') as file:
            file.write(f'0 {self.length_of_simulation_box_edge} xlo xhi\n')
            file.write(f'0 {self.length_of_simulation_box_edge} ylo yhi\n')
            file.write(f'0 {self.length_of_simulation_box_edge} zlo zhi\n\n')

    def write_masses_of_atoms(self):
        with open(f'{self.path}.txt', 'a') as file:
            file.write('Masses\n\n')
            for value in self.atomMasses.values():
                file.write(f"{value['id']} {value['mass']}\n")
            file.write('\n') 

    def write_table_with_atoms_positions(self):
        with open(f'{self.path}.txt', 'a') as file:
           
            file.write('Atoms\n\n')
            
            random_cord = lambda: round(random() * self.length_of_simulation_box_edge, 6)
            number = 0
            for i in range(1, self.quantity+1):
                if number == 0:
                    item = self.composition.popitem()
                    number = item[1]
                    atom = item[0]
                    id = self.charges[atom]['id']
                    charge = self.charges[atom]['charge']

                x = random_cord()
                y = random_cord()
                z = random_cord()

                file.write(f'{i} {id} {charge} {x} {y} {z}\n')

                number-=1

    def create_complete_file(self):
        self.crate_file_with_title()
        self.write_quantity_of_atoms()
        self.write_number_of_atom_types()
        self.write_system_coordinates()
        self.write_masses_of_atoms()
        self.write_table_with_atoms_positions()


class MaterialsList:
    """
        In this class objects input data are process to obtain materials list. 
        one element in list contain important data: 
        atom types, quantity of given atom type, quantity of all atoms in system, volume of system.
        For better understanding find test: Get list of materials in test/test_cord_round.py
    """

    def __init__(self, EquationOfMaterial: type, CompositionOfMaterial: type,
        manyglasses: bool, equationOfMaterial: str, initialValueOfX: float, 
        stepValue: float, quantityOfAtomsInSingleMaterial: int,
        GlassesDensities: str, chargesOfAtoms: str, quantityOfMaterials: int = None, file: str = 'AtomMass.json'): 

        self.EquationOfMaterial = EquationOfMaterial
        self.CompositionOfMaterial = CompositionOfMaterial

        self.equationOfMaterial = equationOfMaterial
        self.initialValueOfX = initialValueOfX
        self.stepValue = stepValue
        self.quantityOfMaterials = quantityOfMaterials
        self.quantityOfAtomsInSingleMaterial = quantityOfAtomsInSingleMaterial
        self.manyglasses = manyglasses

        if self.manyglasses == False:
            self.quantityOfMaterials = 1

        self.GlassesDensities = MaterialsList.convert_string_densities_to_list(GlassesDensities)
        self.chargesOfAtoms = MaterialsList.convert_string_charges_to_dict(chargesOfAtoms)
        self.file = file

    #the two functionalities were combined on purpose
    def get_materials_list_and_atom_masses_dict(self) -> tuple:
        materialsList = []
        i = 0 
        for glassNr in range(self.quantityOfMaterials):

            xValue = (glassNr * self.stepValue) + self.initialValueOfX
            equationOfMaterial = self.EquationOfMaterial(self.equationOfMaterial, self.manyglasses, xValue)
            proportionsOfAtoms = equationOfMaterial.get_proportion_of_atoms()
            composition = self.CompositionOfMaterial(proportionsOfAtoms, self.quantityOfAtomsInSingleMaterial)
            composition = composition.get_atoms_in_system() 
            if i == 0:
                atomsMasses = MaterialsList.read_atoms_masses_from_json_file(composition, self.file)

            massOfMaterial = 0 
            quantityOfAllAtoms = 0
            for (key, quantity) in composition.items():
                atomInComposition = key
                quantityOfAllAtoms += quantity
                massOfMaterial = massOfMaterial + \
                    ( atomsMasses[atomInComposition] * quantity ) / Constants.AvogadroConstant

        
            volume = round(( massOfMaterial / self.GlassesDensities[i] ) * ((10 ** 8) ** 3), 4)
            materialsList.append({'composition': composition, 'quantityOfAtoms': quantityOfAllAtoms, 'volume': volume })
            i += 1

        return materialsList, atomsMasses
    
    def get_charges(self):
        return self.chargesOfAtoms

    @staticmethod
    def convert_string_densities_to_list(GlassesDensities: str) -> list:
        try:
            splitted = GlassesDensities.split(',')
            splitted = [float(item) for item in splitted]
            return splitted
        except:
            raise Exception('Wrong syntax of density list string!')

    @staticmethod
    def convert_string_charges_to_dict(chargesOfAtoms) -> dict:
        try:
            splitted = chargesOfAtoms.split(',')
            splitted = {(item.split(':')[0]).strip(): float(item.split(':')[1]) for item in splitted}
            return splitted
        except:
            raise Exception('Wrong syntax of charges!')

    @staticmethod
    def read_atoms_masses_from_json_file(composition, file: str = 'AtomMass.json') -> dict:
        with open(file, 'r') as fileJ:
            jsonFileContent = json.load(fileJ)
        atomMassesDict = {}
        for atom in composition.keys():
            atomInJson = atom[0:2]
            atomMassesDict.update({atom : jsonFileContent[atomInJson]})
        return atomMassesDict


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
    
    def create_sub_folders(self) -> list:
        pathsList = []
        for i in range(1, self.nrOfFolders +1):
            fileName = self.prefix + str(i)
            path = os.path.join(self.path, self.name, fileName)
            pathsList.append(path)
            os.mkdir(path)
        return pathsList


class EquationOfMaterial: 

    def __init__(self, equation: str, manyGlasses: bool = False, xValue: float = 0):
        self.equation = equation 
        self.manyGlasses = manyGlasses
        self.xValue = xValue

    def get_proportion_of_atoms(self) -> dict:
        proportionsOfOxides = self.get_proportions_of_oxides()
        proportionsOfAtoms = EquationOfMaterial.calculate_proportions_of_atoms(proportionsOfOxides)
        return proportionsOfAtoms

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
                print(item)
                print()
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

    @staticmethod
    def remove_empty_list_elements(list: list) -> list:
        return [item for item in list if item != '']

    @staticmethod
    def round_math_part(number) -> float:
        return round(float(number), 6)


class CompositionOfMaterial:
    def __init__(self, proportionsOfAtoms: dict, numberOfAtomsInSystem: int):
        self.proportionsOfAtoms= proportionsOfAtoms
        self.numberOfAtomsInSystem = numberOfAtomsInSystem
    def get_atoms_in_system(self) -> dict:
        atomsInSystem = {}       
        for key in self.proportionsOfAtoms.keys():
            if self.proportionsOfAtoms[key][1] == 'Cation':
                number = round(self.proportionsOfAtoms[key][0] * self.numberOfAtomsInSystem)
                anion = self.proportionsOfAtoms[key][2]
                ratio = self.proportionsOfAtoms[key][3]
                while number % ratio.denominator != 0:
                    number +=1
                
                atomsInSystem.update({key: number})
                if (anion in atomsInSystem.keys()):
                    atomsInSystem[anion] = int(ratio * number) + atomsInSystem[anion]
                else:
                    atomsInSystem[anion] = int(ratio * number)
        return atomsInSystem


class IncorectFilePath(Exception):
    pass


class NumberOfItemsOnTheListOfOxidesAndCoefficientsIncorrect(Exception):
    pass


class Constants: 
    AvogadroConstant =  6.02214076 * (10 ** 23)