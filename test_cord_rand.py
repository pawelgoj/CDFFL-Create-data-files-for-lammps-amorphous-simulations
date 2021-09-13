import allure
import pytest
import cord_rand
import os.path
import shutil
import os


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

        shutil.rmtree(self.file_path)


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
    @pytest.mark.parametrize(
    'data,manyGlasses,step,respose', 
    [
        ('x Na2O ( 1 - x ) ( 0.7 P2O5 0.3 Fe2O3 )', True, 0.5, {'Na2O': 0.5, 'P2O5': 0.35, 'Fe2O3': 0.15}),
        ('0.7 P2O5 0.3 Fe2O3 0.2 Na2O', False, 0.5, {'P2O5': 0.7, 'Fe2O3': 0.3, 'Na2O': 0.2}),
        ('x P2O5 ( 0.8 - x ) Fe2O3 0.2 Na2O', True, 0.5, {'P2O5': 0.5, 'Fe2O3': 0.3, 'Na2O': 0.2})
    ]
    )
    def test_get_proportions_of_oxides(self, data, manyGlasses, step, respose):
        #Given
        foo = cord_rand.Equation_of_material(data, manyGlasses, 1, step)
        #When
        proportionsOfOxides = foo.get_proportions_of_oxides(xValue = step)

        #Then
        assert respose == proportionsOfOxides

    @allure.title("Get atoms from oxide")    
    @allure.description_html("""
    <p>Get atoms from oxide</p>
    """)
    def test_get_atoms_from_oxide(self):
        #Given
        oxide = 'Fe2O3'
        #When
        atomsDict = cord_rand.Equation_of_material.get_atoms_from_oxide(oxide)
        #Then
        assert atomsDict == {'Fe': 2, 'O': 3}
    
    
    @pytest.mark.skip(reason="No yet this funcionality")
    @allure.title("Get proportions of atoms")    
    @allure.description_html("""
    <p>Get proportions of atoms from proportion of oxides dictionary</p>
    """)
    @pytest.mark.parametrize(
        'data,result',
        [
        ({'P2O5': 0.5, 'Fe2O3': 0.3, 'Na2O': 0.2},{'P': 0.178571, 'Fe': 0.107143, 'Na': 0.071429, 'O': 0.642857})
        ]
    )
    def test_get_proportions_of_atoms(self, data, result):
        assert cord_rand.Equation_of_material.get_proportions_of_atoms(data) == result


    @pytest.mark.skip(reason="No yet this funcionality")
    @allure.title("Create data for calculations")    
    @allure.description_html("""
    <p>Create data for calculations</p>
    """)
    def test_create_data_for_calculations(self, setup):
        #Given 
        pass  
