import allure
import pytest
import cord_rand
import os.path
import shutil
import os
from fractions import Fraction


#Given
#prepare test enviroment
# 

class BaseTest:
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


@pytest.mark.usefixtures("setup")
class Testcord_rand(BaseTest):

    #Dekorator dla allure 
    @allure.title("Create directory")
    @allure.description_html("""
    <p>Create the correct folder</p>
    """)
    def test_create_correct_folder(self, setup):
        path = setup
        #when
        folder = cord_rand.Folder(path, 'Dane', 'dane', 5)
        #then
        assert folder.path ==\
            'D:/Praca/Programowanie/Skrypty-py/AppliactionCFWDFL_tworz_foldery_z_danymi_do_Lammpsa'\
            '/CFWDFL-Create-imput-files-for-lammps/Testy', "Test1"
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
        folder = Testcord_rand.test_create_correct_folder(self, setup)
        #when
        folder.create_folders()
        #then
        assert os.path.isdir('D:/Praca/Programowanie/Skrypty-py/AppliactionCFWDFL'\
            '_tworz_foldery_z_danymi_do_Lammpsa/CFWDFL-Create-imput-files-for-lammps/Testy/Dane'), "Test3"

    @allure.title("Create sub folders")    
    @allure.description_html("""
    <p>Create sub folders</p>
    """)   
    def test_create_sub_folders(self, setup):

        #Given
        folder = Testcord_rand.test_create_correct_folder(self, setup)
        folder.create_folders()
        #when
        folder.create_sub_folders()
        numberOfSubFolders = 5
        #then
        for i in range(1,numberOfSubFolders + 1):
            file = 'dane' + str(i)
            assert os.path.isdir('D:/Praca/Programowanie/Skrypty-py/AppliactionCFWDFL'\
            '_tworz_foldery_z_danymi_do_Lammpsa/CFWDFL-Create-imput-files-for-lammps/Testy/Dane/' + file), "Test4"


    @allure.title("Get proportions of Oxides from equation")    
    @allure.description_html("""
    <p>Get proportions of Oxides from equation</p>
    """)
    @pytest.mark.noautofixt
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
    @pytest.mark.noautofixt
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
    @pytest.mark.noautofixt
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
        assert cord_rand.EquationOfMaterial.calculate_proportions_of_atoms(data) == result    @allure.title("Get proportions of atoms")    


    
    @allure.description_html("""
    <p>Get proportions of atoms</p>
    """)
    @pytest.mark.noautofixt
    @pytest.mark.parametrize(
    'data,manyGlasses,xValue,respose', 
    [
        ('x Na2O ( 1 - x ) ( 0.7 P2O5 0.3 Fe2O3 )', True, 0.5, {'Na2O': 0.5, 'P2O5': 0.35, 'Fe2O3': 0.15}),
        ('0.7 P2O5 0.3 Fe2O3 0.2 Na2O', False, 0.5, {'P2O5': 0.7, 'Fe2O3': 0.3, 'Na2O': 0.2}),
        ('x P2O5 ( 0.8 - x ) Fe2O3 0.2 Na2O', True, 0.5, {'P2O5': 0.5, 'Fe2O3': 0.3, 'Na2O': 0.2})
    ]
    )
    def test_get_proportions_of_atoms(self, data, manyGlasses, xValue ,respose):
        #Given
        foo = cord_rand.EquationOfMaterial(data, manyGlasses, xValue)
        #When
        proportionsOfAtoms = foo.get_proportion_of_atoms()

        #Then
        assert respose == proportionsOfAtoms


    @pytest.mark.skip(reason="No yet this funcionality")
    @allure.title("Create data for calculations")    
    @allure.description_html("""
    <p>Create data for calculations</p>
    """)
    def test_create_data_for_calculations(self, setup):
        #Given 
        pass  
