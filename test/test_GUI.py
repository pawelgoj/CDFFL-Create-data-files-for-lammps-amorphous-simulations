"""
@author: Pawel Goj
"""
from appium import webdriver
from selenium.webdriver.common.keys import Keys
import allure
from allure_commons.types import AttachmentType
import pytest
from test_cord_rand import Preconditions
import os 
import base64


@pytest.mark.usefixtures("setup")
class TestUserGUI(Preconditions):

    @allure.title("User enter correct data into the form")
    @allure.description_html("""
    <p>User enter correct data into the form. Positive test case.</p>
    <p>Environment: Windows 10 Home 20H2</p>
    """)
    @allure.severity(allure.severity_level.NORMAL)
    #@pytest.mark.skip("Too long test!!!")
    def test_user_GU_positive_test_case(self, setup):

        driver = webdriver.Remote(
            command_executor='http://127.0.0.1:4723',
            desired_capabilities={
                "platformName": "Widows",
                "deviceName": "WindowsPC",
                "app": 'D:/Praca/Programowanie/Skrypty-py/AppliactionCFWDFL_tworz_foldery_z_danymi_do_Lammpsa/CFWDFL-Create-imput-files-for-lammps/program-exe-to-tests-on-windows/CDFFL/CDFFL.exe'
            })

        driver.implicitly_wait(0.1)
        driver.set_page_load_timeout(50000)

        button = driver.find_element_by_xpath('//Window[@Name="CDFFL"]/'\
            'Pane[@ClassName="TkChild"]/Pane[@ClassName="TkChild"]/Pane[@ClassName="TkChild"]/Pane[@ClassName="TkChild"]'\
                '/Pane[@ClassName="TkChild"]/Pane[@ClassName="TkChild"]/Button[@ClassName="Button"]')
        button.click()

        chose_directory = driver.find_element_by_xpath('//Window[@Name="Wybierz folder"]/Edit[@ClassName="Edit"][@Name="Folder:"]')
        chose_directory.click()
        path = setup.replace('/', '\\')
        chose_directory.send_keys(path)
        button_chose_directory = driver.find_element_by_xpath('//Window[@Name="Wybierz folder"]/Button[@Name="Wybierz folder"]')

        button_chose_directory.click() 


        driver.find_element_by_xpath('//Window[@Name="CDFFL"]\
            /TitleBar/Button[@Name="Maksymalizuj"]').click()

        input_directory = driver.find_element_by_xpath('//Window[@Name="CDFFL"]/'\
            'Pane[@ClassName="TkChild"]/Pane[@ClassName="TkChild"]/Pane[@ClassName="TkChild"]/Pane[@ClassName="TkChild"]'\
                '/Pane[@ClassName="TkChild"]/Pane[9]')
        input_directory.click()
        input_directory.send_keys('Test')

        input_sub_directory = driver.find_element_by_xpath('//Window[@Name="CDFFL"]/'\
            'Pane[@ClassName="TkChild"]/Pane[@ClassName="TkChild"]/Pane[@ClassName="TkChild"]/Pane[@ClassName="TkChild"]'\
                '/Pane[@ClassName="TkChild"]/Pane[8]')
        input_sub_directory.click()
        input_sub_directory.send_keys('Test')


        input_glass_equation = driver.find_element_by_xpath('//Window[@Name="CDFFL"]/'\
            'Pane[@ClassName="TkChild"]/Pane[@ClassName="TkChild"]/Pane[@ClassName="TkChild"]/Pane[@ClassName="TkChild"]'\
                '/Pane[@ClassName="TkChild"]/Pane[7]/Pane')
        input_glass_equation.click()
        input_glass_equation.send_keys('x Na2O (1 - x ) ( 0.3 Fe2O3 0.7 P2O5 )')


        input_initial_x = driver.find_element_by_xpath('//Window[@Name="CDFFL"]/'\
            'Pane[@ClassName="TkChild"]/Pane[@ClassName="TkChild"]/Pane[@ClassName="TkChild"]/Pane[@ClassName="TkChild"]'\
                '/Pane[@ClassName="TkChild"]/Pane[5]/Pane[3]')
        input_initial_x.click()
        input_initial_x.send_keys('0')

        input_step_x = driver.find_element_by_xpath('//Window[@Name="CDFFL"]/'\
            'Pane[@ClassName="TkChild"]/Pane[@ClassName="TkChild"]/Pane[@ClassName="TkChild"]/Pane[@ClassName="TkChild"]'\
                '/Pane[@ClassName="TkChild"]/Pane[5]/Pane[2]')
        input_step_x.click()
        input_step_x.send_keys('0.1')

        input_number_of_glasses = driver.find_element_by_xpath('//Window[@Name="CDFFL"]/'\
            'Pane[@ClassName="TkChild"]/Pane[@ClassName="TkChild"]/Pane[@ClassName="TkChild"]/Pane[@ClassName="TkChild"]'\
                '/Pane[@ClassName="TkChild"]/Pane[5]/Pane[1]')
        input_number_of_glasses.click()
        input_number_of_glasses.send_keys('5')

        input_number_atoms_in_glass = driver.find_element_by_xpath('//Window[@Name="CDFFL"]/'\
            'Pane[@ClassName="TkChild"]/Pane[@ClassName="TkChild"]/Pane[@ClassName="TkChild"]/Pane[@ClassName="TkChild"]'\
                '/Pane[@ClassName="TkChild"]/Pane[4]/Pane')
        input_number_atoms_in_glass.click()
        input_number_atoms_in_glass.send_keys('100000')

        input_density = driver.find_element_by_xpath('//Window[@Name="CDFFL"]/'\
            'Pane[@ClassName="TkChild"]/Pane[@ClassName="TkChild"]/Pane[@ClassName="TkChild"]/Pane[@ClassName="TkChild"]'\
                '/Pane[@ClassName="TkChild"]/Pane[3]/Pane[2]')
        input_density.click()

        for i in range(20):
            input_density.send_keys(Keys.BACKSPACE)
        input_density.send_keys('3, 2.7, 2.6, 2.5, 2.4')

        input_charges = driver.find_element_by_xpath('//Window[@Name="CDFFL"]/'\
            'Pane[@ClassName="TkChild"]/Pane[@ClassName="TkChild"]/Pane[@ClassName="TkChild"]/Pane[@ClassName="TkChild"]'\
                '/Pane[@ClassName="TkChild"]/Pane[3]/Pane[1]')
        input_charges.click()

        for i in range(20):
            input_charges.send_keys(Keys.BACKSPACE)

        input_charges.send_keys('Fe: 3, P: 5, Na: 1, O: -2')


        button = driver.find_element_by_xpath('//Window[@Name="CDFFL"]/'\
            'Pane[@ClassName="TkChild"]/Pane[@ClassName="TkChild"]/Pane[@ClassName="TkChild"]/Pane[@ClassName="TkChild"]'\
                '/Pane[@ClassName="TkChild"]/Button[2]')
        button.click()

        button = driver.find_element_by_xpath('//Window[@Name="Info"]/Button[@Name="OK"]')
        button.click()

        button = driver.find_element_by_xpath('//Window[@Name="CDFFL"]/'\
            'Pane[@ClassName="TkChild"]/Pane[@ClassName="TkChild"]/Pane[@ClassName="TkChild"]/Pane[@ClassName="TkChild"]'\
                '/Pane[@ClassName="TkChild"]/Button[1]')


        image = base64.decodebytes(bytes(driver.get_screenshot_as_base64(), "utf-8"))

        allure.attach(image, name="App_Window.png", attachment_type=AttachmentType.PNG)


        button.click()


        driver.quit()

        assert os.path.isfile(setup + '/Test/Test1/Test1.txt')


