import allure

import pytest
from pytest_mock import mocker

import pandas as pd 
import numpy as np

import os
import os.path
import shutil

from fractions import Fraction

from main.program import cord_rand
from mocks import MockFactory

import pyautogui



class Preconditions:
    @pytest.fixture()
    def setup(self):
        self.file_path = 'D:/Praca/Programowanie/Skrypty-py/AppliactionCFWDFL_tworz_foldery_z_danymi_do_Lammpsa'\
                '/CFWDFL-Create-imput-files-for-lammps/Testy'
        try:
            shutil.rmtree(self.file_path)
        except:
            pass
        path = os.path.join(self.file_path)
        os.mkdir(path)
        yield self.file_path
        try:
            shutil.rmtree(self.file_path)
        except:
            pass

            
class TestsCompositionOfMaterial:
    @allure.title("Get atoms in system")    
    @allure.description_html("""
    <p>Get atoms in system</p>
    """)
    @pytest.mark.parametrize(
    'proportionsOfAtoms,numberOfAtomsInSystem,response',
    [
        ({'Na': [0.212766, 'Cation', 'O', Fraction(1, 2)],\
            'P': [0.148936, 'Cation', 'O', Fraction(5, 2)],\
            'Fe': [0.063830, 'Cation', 'O', Fraction(3, 2)],\
            'O': [0.574468, 'Anion']}, 1000, {'Na': 214, 'P': 150, 'Fe': 64, 'O': 578})
    ]
    )
    def test_get_atoms_in_system(self, proportionsOfAtoms, numberOfAtomsInSystem, response):
        #Given 
        compositionOfMaterial = cord_rand.CompositionOfMaterial(proportionsOfAtoms, numberOfAtomsInSystem)
        #When 
        atomsInSystem = compositionOfMaterial.get_atoms_in_system()
        #Then 
        assert atomsInSystem == response


class TestEquationOfMaterial:

    @allure.title("Get proportions of Oxides from equation")    
    @allure.description_html("""
    <p>Get proportions of Oxides from equation</p>
    """)
    @pytest.mark.parametrize(
    'data,manyGlasses,xValue,respose', 
    [
        ('x Na2O ( 1 - x ) ( 0.7 P2O5 0.3 Fe2O3 )', True, 0.5, {'Na2O': 0.5, 'P2O5': 0.35, 'Fe2O3': 0.15}),
        ('0.7 P2O5 0.3 Fe2O3 0.2 Na2O', False, 0.5, {'P2O5': 0.7, 'Fe2O3': 0.3, 'Na2O': 0.2}),
        ('x P2O5 ( 0.8 - x ) Fe2O3 0.2 Na2O', True, 0.5, {'P2O5': 0.5, 'Fe2O3': 0.3, 'Na2O': 0.2})
    ]
    )
    def test_get_proportions_of_oxides(self, data, manyGlasses, xValue, respose):
        #Given
        foo = cord_rand.EquationOfMaterial(data, manyGlasses, xValue)
        #When
        proportionsOfOxides = foo.get_proportions_of_oxides()

        #Then
        assert respose == proportionsOfOxides

    
    @allure.title("Calculate atoms from oxide")    
    @allure.description_html("""
    <p>Calculate atoms from oxide</p>
    """)
    @pytest.mark.parametrize('data,result',
    [
        ('Fe2O3',{'Fe': (2, 'Cation', 'O', Fraction(3, 2)), 'O': (3, 'Anion')}),
        ('Na2O',{'Na': (2, 'Cation', 'O', Fraction(1, 2)), 'O': (1, 'Anion')}),
        ('CaO',{'Ca': (1, 'Cation', 'O', Fraction(1, 1)), 'O': (1, 'Anion')}),
        ('CO',{'C': (1, 'Cation', 'O', Fraction(1, 1)), 'O': (1, 'Anion')}),
        ('CO2', {'C': (1, 'Cation', 'O', Fraction(2, 1)), 'O': (2, 'Anion')}),
        ('SiC', {'Si': (1, 'Cation', 'C', Fraction(1, 1)), 'C': (1, 'Anion')})
    ])
    def test_calculate_atoms_from_oxide(self, data, result):
        #Given
        oxide = data
        #When
        atomsDict = cord_rand.EquationOfMaterial.calculate_atoms_from_oxide(oxide)
        #Then
        assert atomsDict == result
    
    
    @allure.title("Calculate proportions of atoms")    
    @allure.description_html("""
    <p>Calculate proportions of atoms from proportion of oxides dictionary</p>
    """)
    @pytest.mark.parametrize(
        'data,result',
        [
        ({'P2O5': 0.5, 'Fe2O3': 0.3, 'Na2O': 0.1 , 'CaO': 0.05, 'SiO2': 0.05},\
        {'P': [0.180180, 'Cation', 'O', Fraction(5, 2)], 'Fe': [0.108108, 'Cation','O', Fraction(3, 2)],\
        'Na': [0.036036, 'Cation', 'O', Fraction(1, 2)], 'Ca': [0.009009, 'Cation', 'O', Fraction(1, 1)],\
        'Si': [0.009009, 'Cation', 'O', Fraction(2, 1)], 'O': [0.657658, 'Anion']})
        ]
    )
    def test_calculate_proportions_of_atoms(self, data, result):
        assert cord_rand.EquationOfMaterial.calculate_proportions_of_atoms(data) == result    
        
        
    @allure.title("Get proportions of atoms")    
    @allure.description_html("""
    <p>Get proportions of atoms</p>
    """)
    @pytest.mark.parametrize(
    'data,manyGlasses,xValue,respose', 
    [
        ('x Na2O ( 1 - x ) ( 0.7 P2O5 0.3 Fe2O3 )', True, 0.5, {'Na': [0.212766, 'Cation', 'O', Fraction(1, 2)],\
            'P': [0.148936, 'Cation', 'O', Fraction(5, 2)],\
            'Fe': [0.063830, 'Cation', 'O', Fraction(3, 2)],\
            'O': [0.574468, 'Anion']}),
        ('0.7 P2O5 0.3 Fe2O3 0.2 Na2O', False, 0.5, {'P': [0.200000, 'Cation', 'O', Fraction(5, 2)],\
            'Fe': [0.085714, 'Cation', 'O', Fraction(3, 2)],\
            'Na': [0.057143, 'Cation', 'O', Fraction(1, 2)],\
            'O': [0.657143, 'Anion']}),
        ('x P2O5 ( 0.8 - x ) Fe2O3 0.2 Na2O', True, 0.5, {'P': [0.178571, 'Cation', 'O', Fraction(5, 2)],\
            'Fe': [0.107143, 'Cation', 'O', Fraction(3, 2)],\
            'Na': [0.071429, 'Cation', 'O', Fraction(1, 2)],\
            'O': [0.642857, 'Anion']})
    ]
    )
    
    def test_get_proportions_of_atoms(self, data, manyGlasses, xValue ,respose):
        #Given
        foo = cord_rand.EquationOfMaterial(data, manyGlasses, xValue)
        #When
        proportionsOfAtoms = foo.get_proportion_of_atoms()

        #Then
        assert respose == proportionsOfAtoms


class TestsMaterialsList:

    @allure.title("Get atoms masses for json file")    
    @allure.description_html("""
    <p>Test of static method: MaterialsList.read_atoms_masses_from_json_file </p>
    """)
    @pytest.mark.parametrize(
    'composition,filePath,response',
    [
        ({'Na': 214, 'P': 150, 'Fe': 64, 'O': 578}, 'main/program/AtomMass.json',
        {'Na': 22.9898, 'P': 30.9738, 'Fe': 55.845, 'O': 15.9994}),
        ({'Na': 214, 'P': 150, 'FeIII': 64, 'O': 578}, 'main/program/AtomMass.json',
        {'Na': 22.9898, 'P': 30.9738, 'FeIII': 55.845, 'O': 15.9994})
    ]
    )
    def test_read_atoms_masses_from_json_file(self, composition, filePath, response):
        #Given #When 
        dictOfMasses = cord_rand.MaterialsList.read_atoms_masses_from_json_file(composition, filePath)
        assert dictOfMasses == response

    @allure.title("Get list of materials")    
    @allure.description_html("""
    <p>Test of method: MaterialsList.get_list_of_materials </p>
    """)
    @pytest.mark.parametrize(
        '''manyglasses,equationOfMaterial,initialValueOfX,
        stepValue,quantityOfMaterials,quantityOfAtomsInSingleMaterial,
        GlassesDensities,chargesOfAtoms,path,resultTuple,resultCharges''',
    [
        (True, 'x FeIII2O3 ( 1 - x ) P2O5', 0.2, 0.1, 3, 200, '2.5, 2.6, 2.7', 'FeIII: 3, P: 5, O: -2', 
        'main/program/AtomMass.json',
        ([ 
            {'composition': {'FeIII': 12, 'O': 138, 'P': 48}, 'quantityOfAtoms': 198, 'volume': 2899.1681},
            {'composition': {'FeIII': 20, 'O': 140, 'P': 44}, 'quantityOfAtoms': 204, 'volume': 3014.3020},
            {'composition': {'FeIII': 26, 'O': 139, 'P': 40}, 'quantityOfAtoms': 205, 'volume': 3022.6969}
        ], {'FeIII': 55.845, 'P': 30.9738, 'O': 15.9994}), {'FeIII': 3, 'P': 5, 'O': -2})
    ]
    )
    def test_get_list_of_materials(self, mocker, manyglasses, equationOfMaterial, initialValueOfX,
        stepValue, quantityOfMaterials, quantityOfAtomsInSingleMaterial, GlassesDensities, 
        chargesOfAtoms, path, resultTuple, resultCharges):

        #Given  
        mock = mocker.Mock(name="MockFactory")
        mock.get_EquationOfMaterial_class.side_effect = MockFactory.get_EquationOfMaterial_class
        mock.get_CompositionOfMaterial_class.side_effect = MockFactory.get_CompositionOfMaterial_class

        materialsList = cord_rand.MaterialsList(mock.get_EquationOfMaterial_class(), mock.get_CompositionOfMaterial_class(),
            manyglasses, equationOfMaterial, initialValueOfX,stepValue,
            quantityOfAtomsInSingleMaterial, GlassesDensities, chargesOfAtoms, quantityOfMaterials, path)

        #When
        result = materialsList.get_materials_list_and_atom_masses_dict()

        #Then
        assert result == resultTuple
        assert materialsList.chargesOfAtoms == resultCharges


@pytest.mark.usefixtures("setup")
class TestCreateFoldersAndSubFolders(Preconditions):

    #Decorator for allure 
    @allure.title("Create directory")
    @allure.description_html("""
    <p>Create the correct folder</p>
    """)
    def test_create_correct_folder(self, setup):
        path = setup
        #when
        folder = cord_rand.Folder(path, 'Dane', 'dane', 3)


        #then

        assert folder.path == path 

        return folder


    @allure.title("Create incorrect folder") 
    @allure.description_html("""
    <p>Create incorrect folder</p>
    """)
    def test_create_incorrect_folder(self, setup):
        #try
        with pytest.raises(cord_rand.IncorectFilePath):
            folder = cord_rand.Folder()


    @allure.title("Create directory") 
    @allure.description_html("""
    <p>Create directory</p>
    """)
    def test_create_directory(self, setup):
        #Given
        folder = TestCreateFoldersAndSubFolders.test_create_correct_folder(self, setup)
        path = setup


        #when
        folder.create_folders()


        #then
        assert os.path.isdir(path  + '/Dane')


    @allure.title("Create sub folders")    
    @allure.description_html("""
    <p>Create sub folders</p>
    """)   
    def test_create_sub_folders(self, setup):

        #Given
        folder = TestCreateFoldersAndSubFolders.test_create_correct_folder(self, setup)
        folder.create_folders()
        path = setup


        #when
        subFoldersList = folder.create_sub_folders()
        numberOfSubFolders = 3


        #then
        for i in range(1,numberOfSubFolders + 1):
            file = 'dane' + str(i)
            print(subFoldersList)
            assert os.path.isdir(path +'/Dane/' + file) and subFoldersList


@pytest.mark.usefixtures("setup")
class TestsCreateFileForLammps(Preconditions):

    data_for_tests = ('Test', {'composition': {'FeIII': 26, 'O': 139, 'P': 40}, 'quantityOfAtoms': 205, 'volume': 3022.6969},
        {'FeIII': 3, 'P': 5, 'O': -2}, {'FeIII': 55.845, 'P': 30.9738, 'O': 15.9994}, {'FeIII': 1, 'P': 2, 'O': 3})

    @allure.title("Crate file with title")
    @allure.description_html("""
    <p>Crate file with title</p>
    """)
    @pytest.mark.parametrize(
    'name, material, charges, atomMasses, atom_id',
    [
        data_for_tests
    ]
    )
    def test_crate_file_with_title(self, setup, name, material, charges, atomMasses,  atom_id):
        #Given 
        sub_folder_path = setup
        file_for_lammps = cord_rand.FileForLammps(name, material, charges, atomMasses, sub_folder_path,  atom_id)


        #When 
        file_for_lammps.crate_file_with_title()


        #Then
        path = sub_folder_path  + '/' + name + '.txt'

        assert os.path.isfile(path)


    @allure.title("Write quantity of atoms")
    @allure.description_html("""
    <p>Write quantity of atoms</p>
    """)
    @pytest.mark.parametrize(
    'name, material, charges, atomMasses, atom_id',
    [
        data_for_tests
    ]
    )
    def test_write_quantity_of_atoms(self, setup, name, material, charges, atomMasses, atom_id):

        #Given 
        TestsCreateFileForLammps.test_crate_file_with_title(self, setup, name, material, charges, atomMasses, atom_id)
        sub_folder_path = setup
        file_for_lammps = cord_rand.FileForLammps(name, material, charges, atomMasses, sub_folder_path, atom_id)


        #When 
        file_for_lammps.write_quantity_of_atoms()


        #Then
        path = sub_folder_path  + '/' + name + '.txt'
        with open(path, 'r' ) as file:
            text_in_file = file.read()

            assert '205 atoms' in text_in_file


    @allure.title("Write number of atom types")
    @allure.description_html("""
    <p>Write number of atom types</p>
    """)
    @pytest.mark.parametrize(
    'name, material, charges, atomMasses, atom_id',
    [
        data_for_tests
    ]
    )
    def test_write_number_of_atom_types(self, setup, name, material, charges, atomMasses, atom_id):
        #Given 
        TestsCreateFileForLammps.test_crate_file_with_title(self, setup, name, material, charges, atomMasses, atom_id)
        sub_folder_path = setup


        file_for_lammps = cord_rand.FileForLammps(name, material, charges, atomMasses, sub_folder_path, atom_id)
        #When 
        file_for_lammps.write_number_of_atom_types()


        #Then
        path = sub_folder_path  + '/' + name + '.txt'
        with open(path, 'r' ) as file:
            text_in_file = file.read()

            assert '3 atom types' in text_in_file


    @allure.title("Write system coordinates")
    @allure.description_html("""
    <p>Write system coordinates</p>
    """)
    @pytest.mark.parametrize(
    'name, material, charges, atomMasses, atom_id',
    [
        data_for_tests
    ]
    )
    def test_write_system_coordinates(self, setup, name, material, charges, atomMasses, atom_id):
        #Given 
        TestsCreateFileForLammps.test_crate_file_with_title(self, setup, name, material, charges, atomMasses, atom_id)
        sub_folder_path = setup
        file_for_lammps = cord_rand.FileForLammps(name, material, charges, atomMasses, sub_folder_path, atom_id)


        #When 
        file_for_lammps.write_system_coordinates()


        #Then
        path = sub_folder_path  + '/' + name + '.txt'
        with open(path, 'r' ) as file:
            text_in_file = file.read()

            assert '0 14.458776 xlo xhi\n0 14.458776 ylo yhi\n0 14.458776 zlo zhi' in text_in_file


    @allure.title("Write masses of atoms")
    @allure.description_html("""
    <p>Write masses of atoms</p>
    """)
    @pytest.mark.parametrize(
    'name, material, charges, atomMasses, atom_id',
    [
        data_for_tests
    ]
    )
    def test_write_masses_of_atoms(self, setup, name, material, charges, atomMasses, atom_id):

        #Given 
        TestsCreateFileForLammps.test_crate_file_with_title(self, setup, name, material, charges, atomMasses, atom_id)
        sub_folder_path = setup
        file_for_lammps = cord_rand.FileForLammps(name, material, charges, atomMasses, sub_folder_path, atom_id)


        #When 
        file_for_lammps.write_masses_of_atoms()


        #Then
        path = sub_folder_path  + '/' + name + '.txt'
        with open(path, 'r' ) as file:
            text_in_file = file.read()

            assert '1 55.845\n2 30.9738\n3 15.9994' in text_in_file


    @allure.title("Write table with atoms positions")
    @allure.description_html("""
    <p>Write table with atoms positions</p>
    """)
    @pytest.mark.parametrize(
    'name, material, charges, atomMasses, atom_id',
    [
        data_for_tests
    ]
    )
    def test_write_table_with_atoms_positions(self, setup, name, material, charges, atomMasses, atom_id):

        #Given 
        TestsCreateFileForLammps.test_crate_file_with_title(self, setup, name, material, charges, atomMasses, atom_id)
        sub_folder_path = setup
        file_for_lammps = cord_rand.FileForLammps(name, material, charges, atomMasses, sub_folder_path, atom_id)

        def get_correct_number_of_atom_types(charges, material):
            correct_values = []
            for key in charges.keys():               
                correct_values.append(material['composition'][key])

            return correct_values 


        #When 
        file_for_lammps.write_table_with_atoms_positions()


        #Then
        def cunt_atom_types_in_file(sub_folder_path, name):
            path = sub_folder_path  + '/' + name + '.txt'
            with open(path, 'r' ) as file:
                text_in_file = file.read()

            splitted = text_in_file.split('\n')
            splitted = splitted[4:-1]

            for item in splitted:
                item = item.split()
                try: 
                    top = np.array(item)
                    bottom = np.vstack((bottom, top))
                except:

                    bottom = np.array(item)

            df = pd.DataFrame(data=bottom)

            cunt = df.groupby([2]).count()
            cunt_in_file = []
            for key, value in charges.items():
                cunt_in_file.append(cunt.loc[str(value), 1])

            return cunt_in_file

        assert get_correct_number_of_atom_types(charges, material) == cunt_atom_types_in_file(sub_folder_path, name)

    @allure.title("Write table with atoms positions")
    @allure.description_html("""
    <p>Write table with atoms positions</p>
    """)
    @pytest.mark.parametrize(
    'name, material, charges, atomMasses, atom_id',
    [
        data_for_tests
    ]
    )
    def test_create_file_with_all_necessary_data(self, setup, name, material, charges, atomMasses, atom_id):
        #Given 
        sub_folder_path = setup
        file = cord_rand.FileForLammps(name, material, charges, atomMasses, sub_folder_path, atom_id)

        #When 
        file.create_complete_file()

        path = sub_folder_path  + '/' + name + '.txt'
        with open(path, 'r' ) as file:
            text_in_file = file.read()

        #Then 
        assert '205 atoms' in text_in_file and '3 atom types' in text_in_file\
            and '0 14.458776 xlo xhi\n0 14.458776 ylo yhi\n0 14.458776 zlo zhi' in text_in_file\
            and '1 55.845\n2 30.9738\n3 15.9994' in text_in_file


@pytest.mark.usefixtures("setup")
class TestsFilesForLammps(Preconditions):

    @allure.title("Create files with data for Lammps simulations in subfolders")
    @allure.description_html("""
    <p>Create files with data for Lammps simulations in subfolders</p>
    """)
    @pytest.mark.parametrize(
    "nameOfFolder,prefixOfSubFolder,nrOfSubFoldersFolders,materialsList, atomsMasses,charges",
        [('Dane', 'dane', 3,
        [ 
            {'composition': {'FeIII': 12, 'O': 138, 'P': 48}, 'quantityOfAtoms': 198, 'volume': 2899.1681},
            {'composition': {'FeIII': 20, 'O': 140, 'P': 44}, 'quantityOfAtoms': 204, 'volume': 3014.3020},
            {'composition': {'FeIII': 26, 'O': 139, 'P': 40}, 'quantityOfAtoms': 205, 'volume': 3022.6969}
        ], {'FeIII': 55.845, 'P': 30.9738, 'O': 15.9994}, {'FeIII': 3, 'P': 5, 'O': -2})
        ]

    )
    def test_make_files(self, setup, nameOfFolder, prefixOfSubFolder, nrOfSubFoldersFolders, materialsList, atomsMasses, charges):
        
        #Given
        path = setup
        folder = cord_rand.Folder(path, nameOfFolder, prefixOfSubFolder, nrOfSubFoldersFolders)
        folder.create_folders()
        subfoldersPaths = folder.create_sub_folders()

        #When 
        filesForLammps = cord_rand.FilesForLammps(cord_rand.FileForLammps, subfoldersPaths, prefixOfSubFolder, materialsList, atomsMasses, charges)
        filesForLammps.make_files()

        #Then
        for i in range(1,nrOfSubFoldersFolders + 1):
            subFolder = 'dane' + str(i)
            file = 'dane' + str(i)
            assert os.path.exists(path +'/Dane/' + subFolder + '/' + file + '.txt')
    
    
    @allure.title('Get atom names with id')
    @allure.description_html("""
        <p>Get atom names with id from object of class TestsFilesForLammps</p>
        """)
    @pytest.mark.parametrize(
    "nameOfFolder,prefixOfSubFolder,nrOfSubFoldersFolders,materialsList, atomsMasses,charges",
        [('Dane', 'dane', 3,
        [ 
            {'composition': {'FeIII': 12, 'O': 138, 'P': 48}, 'quantityOfAtoms': 198, 'volume': 2899.1681},
            {'composition': {'FeIII': 20, 'O': 140, 'P': 44}, 'quantityOfAtoms': 204, 'volume': 3014.3020},
            {'composition': {'FeIII': 26, 'O': 139, 'P': 40}, 'quantityOfAtoms': 205, 'volume': 3022.6969}
        ], {'FeIII': 55.845, 'P': 30.9738, 'O': 15.9994}, {'FeIII': 3, 'P': 5, 'O': -2})
        ]

    )
    def test_get_atoms_id(self, setup, nameOfFolder, prefixOfSubFolder, nrOfSubFoldersFolders, materialsList, atomsMasses, charges):

        #Given
        path = setup
        folder = cord_rand.Folder(path, nameOfFolder, prefixOfSubFolder, nrOfSubFoldersFolders)
        folder.create_folders()
        subfoldersPaths = folder.create_sub_folders()
        filesForLammps = cord_rand.FilesForLammps(cord_rand.FileForLammps, subfoldersPaths, prefixOfSubFolder, materialsList, atomsMasses, charges)

        #When 
        atoms_names_with_id = filesForLammps.get_atoms_id()

        #Then 
        assert atoms_names_with_id == {'FeIII': 1, 'P': 2, 'O': 3}


@pytest.mark.usefixtures("setup")
class TestFileWithAtomsId(Preconditions):

    @allure.title("Create file with atoms id")
    @allure.description_html("""
    <p>Test of method create_file for class FileWithAtomsId</p>
    """)
    @pytest.mark.parametrize(
        'atoms_id',
        [({'FeIII': 1, 'P': 2, 'O': 3})]
    )
    def test_create_file(self, setup, atoms_id):
        path = setup
        file = cord_rand.FileWithAtomsId(setup, atoms_id)
        file.create_file()

        path = path  + '/atoms_id.txt'
        with open(path, 'r' ) as file:
            text_in_file = file.read()

        assert 'FeIII: 1\nP: 2\nO: 3' in text_in_file


@pytest.mark.usefixtures("setup")
class TestsApp(Preconditions):
    @allure.title("Create folders with data for Lammps App test -integrate test")
    @allure.description_html("""
    <p>Create folders with data for Lammps App test, integration test</p>
    """)
    @pytest.mark.parametrize(
        'nameOfFolder,prefixSubFolder,equation, manyGlasses,atomsInSingleMaterial,'\
        'strDensityList, strCharges, initX, stepX, quantityOfMaterials, file_json_path',
        [('Test', 'Test', 'x Na2O (1 - x ) ( 0.3 Fe2O3 0.7 P2O5 )',
        True, 10000, '3, 2.7, 2.6, 2.5, 2.4', 'Fe: 3, P: 5, Na: 1, O: -2', 
        0, 0.1, 5, 'main/program/AtomMass.json')]
    )
    def test_make_folders_with_data_for_lammps(self, setup, nameOfFolder, prefixSubFolder, equation, manyGlasses,
        atomsInSingleMaterial, strDensityList, strCharges, initX, stepX, quantityOfMaterials, file_json_path):

        #Given
        app = cord_rand.App()
        app.set_directory(setup)

        #When
        app.make_folders_with_data_for_lammps(nameOfFolder, prefixSubFolder, equation, manyGlasses,
        atomsInSingleMaterial, strDensityList, strCharges, initX, stepX, quantityOfMaterials, file_json=file_json_path)

        #Then 
        assert os.path.isfile(setup + '/' + nameOfFolder + '/' + prefixSubFolder + '1' + '/' + prefixSubFolder + '1.txt')

        