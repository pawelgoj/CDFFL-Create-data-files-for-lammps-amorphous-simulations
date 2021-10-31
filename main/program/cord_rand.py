"""
@author: Pawel Goj
"""
import os
import re
from fractions import Fraction
from random import random
from typing import Optional 
from tkinter.ttk import Progressbar

try: 
    from program.config import Config
except:
    from main.program.config import Config

import json

PATH = Config.PATH_TO_JSON_FILE_WITH_MASSES

class App:
    def __init__(self):
        self.directory = ''

    def set_directory(self, directory):
        self.directory = directory

    def make_folders_with_data_for_lammps(self, name_of_folder: str, prefix_sub_folder: str, equation: str, many_glasses: bool,
        atoms_in_single_material: int, str_density_list: str, str_charges: str, init_x: float = 0, step_x: float = 0,
        quantity_of_materials: int = 1, progress_bar: Optional[Progressbar] = None, application_gui: Optional[type] = None,
        file_json: str = PATH + 'program/AtomMass.json'):

        nr_of_folders = quantity_of_materials

        if progress_bar != None and application_gui != None: 
            progress_bar['value'] = 20
            application_gui.update_idletasks()

        folder = Folder(self.directory, name_of_folder, prefix_sub_folder, nr_of_folders)

        folder.create_folders()

        subfolders_paths = folder.create_sub_folders()

        materials_list = MaterialsList(EquationOfMaterial, CompositionOfMaterial,
        many_glasses, equation, init_x, step_x, atoms_in_single_material,
        str_density_list, str_charges, quantity_of_materials, file = file_json)

        if progress_bar != None and application_gui != None: 
            progress_bar['value'] = 40
            application_gui.update_idletasks()

        charges = materials_list.get_charges()
        materials_list, atoms_masses = materials_list.get_materials_list_and_atom_masses_dict()

        filesForLammps = FilesForLammps(FileForLammps, subfolders_paths, prefix_sub_folder , materials_list, atoms_masses, charges)
        filesForLammps.make_files()

        if progress_bar != None and application_gui != None: 
            progress_bar['value'] = 70
            application_gui.update_idletasks()

        atoms_id = filesForLammps.get_atoms_id()
        directory = self.directory + '/' + name_of_folder

        file_with_atoms_id = FileWithAtomsId(directory, atoms_id)
        file_with_atoms_id.create_file()

        if progress_bar != None and application_gui != None: 
            progress_bar['value'] = 100
            application_gui.update_idletasks()


class FileWithAtomsId():
    def __init__(self, path: str, atoms_id: dict):
        self.path = path
        self.atoms_id = atoms_id

    def create_file(self):
        path = self.path + '/atoms_id.txt'
        with open(path, 'w') as file:
            for name, id in self.atoms_id.items():
                file.write(f'{name}: {id}\n')


class FilesForLammps:
    def __init__(self, File_for_lammps: type, subfolders_paths: list, prefix_sub_folder: str, materials_list: list,
         atoms_masses: dict, charges: dict):
        
        self.File_for_lammps = File_for_lammps
        self.prefix_sub_folder = prefix_sub_folder
        self.subfolders_paths = subfolders_paths
        self.materials_list = materials_list
        self.charges = charges
        self.atoms_masses = atoms_masses
        self.File_for_lammps = File_for_lammps

        atom_id = {}
        for id, atom in enumerate(self.charges.keys(), 1):
            atom_id.update({atom: id})

        self.atom_id = atom_id

    def make_files(self):
        i = 0
        for subfolder_path in self.subfolders_paths:
            name = self.prefix_sub_folder + f"{i+1}"
            
            material = self.materials_list[i]
            file = self.File_for_lammps(name, material, self.charges, self.atoms_masses, subfolder_path, self.atom_id)
            file.create_complete_file()
            i+= 1
    
    def get_atoms_id(self):
        return self.atom_id


class FileForLammps:
    def __init__(self, name: str, material: dict, charges: dict, atom_masses: dict, subfolder_path: str, atom_id: dict):
        self.path = f'{subfolder_path}\\{name}'
        self.name = name 

        if len(charges) != len(atom_masses):
            raise Exception('length of charges dict != length of atom masses dict')

        temporary_atom_masses = atom_masses.copy()
        temporary_charges = charges.copy()
        
        for atom in charges.keys():
            temporary_charges[atom] = {'id': atom_id[atom], 'charge': charges[atom]}
            temporary_atom_masses[atom] = {'id': atom_id[atom], 'mass': atom_masses[atom]}

        self.atom_id = atom_id

        self.charges = temporary_charges
        self.atom_masses = temporary_atom_masses

        self.length_of_simulation_box_edge = round(material['volume'] ** (1/3), 6)

        self.quantity = material['quantityOfAtoms']
        self.composition = material['composition'].copy()

    def crate_file_with_title(self):
        with open(f'{self.path}.txt', 'x') as file:
            file.write(f'#{self.name}\n\n')

    def write_quantity_of_atoms(self):
        with open(f'{self.path}.txt', 'a') as file:
            file.write(f'{self.quantity} atoms\n\n')
    
    def write_number_of_atom_types(self):
        number_of_atoms_types = len(self.composition)
        with open(f'{self.path}.txt', 'a') as file:
            file.write(f'{number_of_atoms_types} atom types\n\n')
 
    def write_system_coordinates(self):
        with open(f'{self.path}.txt', 'a') as file:
            file.write(f'0 {self.length_of_simulation_box_edge} xlo xhi\n')
            file.write(f'0 {self.length_of_simulation_box_edge} ylo yhi\n')
            file.write(f'0 {self.length_of_simulation_box_edge} zlo zhi\n\n')

    def write_masses_of_atoms(self):
        with open(f'{self.path}.txt', 'a') as file:
            file.write('Masses\n\n')
            for value in self.atom_masses.values():
                file.write(f"{value['id']} {value['mass']}\n")
            file.write('\n') 

    def write_table_with_atoms_positions(self):
        with open(f'{self.path}.txt', 'a') as file:
           
            file.write('Atoms\n\n')
            
            random_cord = lambda: round(random() * self.length_of_simulation_box_edge, 6)
            number = 0

            i = 1

            while i < self.quantity + 1:
                if number <= 0:
                    item = self.composition.popitem()
                    number = item[1]
                    atom = item[0]
                    id = self.charges[atom]['id']
                    charge = self.charges[atom]['charge']

                if number != 0:
                    x = random_cord()
                    y = random_cord()
                    z = random_cord()

                    file.write(f'{i} {id} {charge} {x} {y} {z}\n')

                elif i > 1:
                    i-=1

                i+=1
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
        many_glasses: bool, equation_of_material: str, initial_value_of_x: float, 
        step_value: float, quantity_of_atoms_in_single_material: int,
        glasses_densities: str, charges_of_atoms: str, quantity_of_materials: Optional[int] = None, file: str = PATH + 'program/AtomMass.json'): 

        self.EquationOfMaterial = EquationOfMaterial
        self.CompositionOfMaterial = CompositionOfMaterial

        self.equation_of_material = equation_of_material
        self.initial_value_of_x = initial_value_of_x
        self.step_value = step_value
        self.quantity_of_materials = quantity_of_materials
        self.quantity_of_atoms_in_single_material = quantity_of_atoms_in_single_material
        self.many_glasses = many_glasses

        if self.many_glasses == False:
            self.quantity_of_materials = 1
        elif self.quantity_of_materials == None:
            raise Exception('Not set quantity of materials!!!!!')

        self.glasses_densities = MaterialsList.convert_string_densities_to_list(glasses_densities)
        self.charges_of_atoms = MaterialsList.convert_string_charges_to_dict(charges_of_atoms)
        self.file = file

    #the two functionalities were combined on purpose
    def get_materials_list_and_atom_masses_dict(self) -> tuple:
        materials_list = []
        i = 0 
        for glassNr in range(self.quantity_of_materials):

            x_value = (glassNr * self.step_value) + self.initial_value_of_x
            equation_of_material = self.EquationOfMaterial(self.equation_of_material, self.many_glasses, x_value)
            proportions_of_atoms = equation_of_material.get_proportion_of_atoms()
            composition = self.CompositionOfMaterial(proportions_of_atoms, self.quantity_of_atoms_in_single_material)
            composition = composition.get_atoms_in_system() 
            if i == 0:
                atoms_masses = MaterialsList.read_atoms_masses_from_json_file(composition, self.file)

            mass_of_material = 0 
            quantity_of_all_atoms = 0
            for (key, quantity) in composition.items():
                atom_in_composition = key
                quantity_of_all_atoms += quantity
                mass_of_material = mass_of_material + \
                    (atoms_masses[atom_in_composition] * quantity ) / Constants.avogadro_constant

        
            volume = round(( mass_of_material / self.glasses_densities[i] ) * ((10 ** 8) ** 3), 4)
            materials_list.append({'composition': composition, 'quantityOfAtoms': quantity_of_all_atoms, 'volume': volume })
            i += 1
        return materials_list, atoms_masses
    
    def get_charges(self):
        return self.charges_of_atoms

    @staticmethod
    def convert_string_densities_to_list(glasses_densities: str) -> list:
        try:
            splitted = glasses_densities.split(',')
            splitted = [float(item) for item in splitted]
            return splitted
        except:
            raise Exception('Wrong syntax of density list string!')

    @staticmethod
    def convert_string_charges_to_dict(charges_of_atoms) -> dict:
        try:
            splitted = charges_of_atoms.split(',')
            splitted = {(item.split(':')[0]).strip(): float(item.split(':')[1]) for item in splitted}
            return splitted
        except:
            raise Exception('Wrong syntax of charges!')

    @staticmethod
    def read_atoms_masses_from_json_file(composition, file: str = PATH + 'program/AtomMass.json') -> dict:
        with open(file, 'r') as fileJ:
            json_file_content = json.load(fileJ)
        atom_masses_dict = {}
        for atom in composition.keys():
            atom_in_json = atom[0:2]
            atom_masses_dict.update({atom : json_file_content[atom_in_json]})
        return atom_masses_dict


class Folder: 
    def __init__(self, path: str ='', name: str = '', prefix: str = '', nr_of_folders: int = 0):
        '''Folder class creates directory for input simulations files'''
        if path == '' or name == '' or prefix == '' or nr_of_folders == 0:
            raise IncorectFilePath('No path to directory!!!')
        else:
            self.path = path
            self.name = name
            self.prefix = prefix
            self.nr_of_folders = nr_of_folders
        
    def create_folders(self) -> None:
        path = os.path.join(self.path, self.name)
        os.mkdir(path)
    
    def create_sub_folders(self) -> list:
        paths_list = []
        for i in range(1, self.nr_of_folders +1):
            file_name = self.prefix + str(i)
            path = os.path.join(self.path, self.name, file_name)
            paths_list.append(path)
            os.mkdir(path)
        return paths_list


class EquationOfMaterial: 

    def __init__(self, equation: str, many_glasses: bool = False, x_value: float = 0):
        self.equation = equation 
        self.many_glasses = many_glasses
        self.x_value = x_value

    def get_proportion_of_atoms(self) -> dict:
        proportions_of_oxides = self.get_proportions_of_oxides()
        proportions_of_atoms = EquationOfMaterial.calculate_proportions_of_atoms(proportions_of_oxides)
        return proportions_of_atoms

    def get_proportions_of_oxides(self) -> dict:

        if self.many_glasses:
            replaced = self.equation.replace("x", str(self.x_value))
        else: 
            replaced = self.equation

        math_part = re.split(r"[a-zA-Z]\S+", replaced)

        math_part_to_sort = math_part.copy()
        math_part_to_sort.sort(reverse=True, key = lambda item: len(item))
        for item in math_part_to_sort:
            if item != '':
                replaced = replaced.replace(str(item), ' ')
        del math_part_to_sort

        temp_list =[]
        for item in math_part: 
            item = item.replace(') (', ')@@(')
            item = item.split('@@')
            temp_list = temp_list + item

        math_part = []

        try:
            temp_list.remove('')
        except:
            pass

        for item in temp_list:
            if item.count('(') == item.count(')'):
                math_part.append(eval(item))
            else:
                math_part.append(item)
        
        temp_list = []
        factor_in_front_of_the_parenthesis = 0
        multiply = False
        for item in math_part:
            item = str(item)
            if -1 != item.find('('):
                temp_list.pop()
                multiply = True
            elif -1 != item.find(')'):
                multiply = False 
            
            if multiply:
                item = item.replace('(', '')
                item = item.replace(' ', '')
                temp_list.append(float(item) * factor_in_front_of_the_parenthesis)
            else:
                try:
                    factor_in_front_of_the_parenthesis = float(item)
                    temp_list.append(item)
                except:
                    continue

        math_part =  temp_list.copy()
        del temp_list
        text_part = replaced.split(' ')
        text_part = [item for item in text_part if item != '']  

        proportions_of_oxides = {}

        if len(text_part) == len(math_part):
            for i in range(len(text_part)):
                proportions_of_oxides.update({text_part[i]: round(float(math_part[i]), 6)})                
        else:
            raise NumberOfItemsOnTheListOfOxidesAndCoefficientsIncorrect('Number of items on the list of'\
                'oxides and coefficients incorrect')

        
    
        return proportions_of_oxides

    @classmethod
    def calculate_proportions_of_atoms(cls,  proportions_of_oxides: dict) -> dict:

        proportions_of_atoms = {}
        for key in proportions_of_oxides.keys():
            atom_dict = cls.calculate_atoms_from_oxide(key)
            dict = {}
            for key_atom_dict in atom_dict.keys():
                dict.update({key_atom_dict: [atom_dict[key_atom_dict][0] * proportions_of_oxides[key], *atom_dict[key_atom_dict][1:]]})
            atom_dict = dict.copy()
            del dict


            for key in atom_dict.keys():
                if key in proportions_of_atoms.keys():
                    if atom_dict[key][1] == 'Anion':
                        proportions_of_atoms[key][0] = proportions_of_atoms[key][0] + atom_dict[key][0]
                    else:
                        raise Exception(f'Atom {key} in two different oxidation states')
                else:
                    proportions_of_atoms[key] = atom_dict[key]
            
        proportions_of_atoms = cls.calculate_ratios(proportions_of_atoms)
        
        return proportions_of_atoms

    @classmethod
    def calculate_atoms_from_oxide(cls, oxide: str) -> dict:
        def check_cation_or_anion(position_in_oxideormula: int) -> str:
            if position_in_oxideormula == 0:
                return 'Cation'
            elif position_in_oxideormula == 1:
                return 'Anion'  
            else:
                raise Exception('You can use only simple compound oxide notation eg. Fe2O3 also SiC is correct')  

        
        math_part = re.split(r"[a-zA-Z]", oxide)
        text_part = re.split(r"[0-9]", oxide)

        math_part = cls.remove_empty_list_elements(math_part)
        text_part = cls.remove_empty_list_elements(text_part)


        if math_part != [] and len(math_part) == len(text_part) and len(math_part) > 1:
            oxide_dict = {}
            for i in range(len(text_part)):
                if check_cation_or_anion(i) == 'Cation': 
                    oxide_dict.update({text_part[i]: (cls.round_math_part(math_part[i]), check_cation_or_anion(i), text_part[i+1],\
                        Fraction(int(math_part[i+1]), int(math_part[i])))})
                elif check_cation_or_anion(i) == 'Anion':
                    oxide_dict.update({text_part[i]: (cls.round_math_part(math_part[i]), check_cation_or_anion(i))})
                else:
                    raise Exception('Wrong oxide notation!!!!')
        else:
            temp_dict = {}
            j = 0
            for item in text_part:
                i = 0
                for character in item:
                    if character.isupper() and i != 0:
                        before_character = item[:i]
                        after_character = item[i:]
                        if after_character != '' and math_part == []:
                            if temp_dict == {}:
                                temp_dict.update({before_character: (1, 'Cation', after_character, Fraction(1, 1))})
                                temp_dict.update({after_character: (1, 'Anion')})
                            else:
                                temp_dict = {}
                                temp_dict.update({before_character: (1, 'Cation', after_character, Fraction(1, 1))})
                                temp_dict.update({after_character: (1, 'Anion')})

                        elif len(math_part) == 1:
                            if len(text_part) == 1:
                                if temp_dict == {}:
                                    temp_dict.update({before_character: (1, 'Cation', after_character, Fraction(int(math_part[0]), 1))})
                                    temp_dict.update({after_character: (cls.round_math_part(math_part[0]), check_cation_or_anion(1))})
                                else:
                                    temp_dict = {}
                                    temp_dict.update({before_character: (1, 'Cation', after_character, Fraction(int(math_part[0]), 1))})
                                    temp_dict.update({after_character: (cls.round_math_part(math_part[0]), check_cation_or_anion(1))})
                        else: 
                            raise Exception('Wrong oxide name!')
                    i+=1 
            if temp_dict != {}: 
                oxide_dict = temp_dict.copy()
            else: 
                math_part.append(1)
                oxide_dict = {}
                for i in range(len(text_part)):
                    if check_cation_or_anion(i) == 'Cation': 
                        oxide_dict.update({text_part[i]: (cls.round_math_part(math_part[i]), check_cation_or_anion(i), text_part[i+1],\
                            Fraction(int(math_part[i+1]), int(math_part[i])))})
                    elif check_cation_or_anion(i) == 'Anion':
                        oxide_dict.update({text_part[i]: (cls.round_math_part(math_part[i]), check_cation_or_anion(i))})
                    else:
                        raise Exception('Wrong oxide notation!!!!')

            del temp_dict

        return oxide_dict

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
    def __init__(self, proportions_of_atoms: dict, number_of_atoms_in_system: int):
        self.proportions_of_atoms= proportions_of_atoms
        self.number_of_atoms_in_system = number_of_atoms_in_system

    def get_atoms_in_system(self) -> dict:
        atoms_in_system = {}       
        for key in self.proportions_of_atoms.keys():
            if self.proportions_of_atoms[key][1] == 'Cation':
                number = round(self.proportions_of_atoms[key][0] * self.number_of_atoms_in_system)
                anion = self.proportions_of_atoms[key][2]
                ratio = self.proportions_of_atoms[key][3]
                while number % ratio.denominator != 0:
                    number +=1
                
                atoms_in_system.update({key: number})
                if (anion in atoms_in_system.keys()):
                    atoms_in_system[anion] = int(ratio * number) + atoms_in_system[anion]
                else:
                    atoms_in_system[anion] = int(ratio * number)
        return atoms_in_system


class IncorectFilePath(Exception):
    pass


class NumberOfItemsOnTheListOfOxidesAndCoefficientsIncorrect(Exception):
    pass


class Constants: 
    avogadro_constant =  6.02214076 * (10 ** 23)