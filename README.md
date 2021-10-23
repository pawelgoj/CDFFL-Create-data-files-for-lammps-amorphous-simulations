# CDFFL-Create-data-files-for-lammps-amorphous-simulations

## Description 
CDFFLthe application creates folders with files containing start data for Lammps (https://www.lammps.org/) simulations. In the starting data, the atoms are placed randomly in the simulation box. This can be useful when simulating glasses or amorphous materials. You just need to enter an oxide formula that specifies the composition of the materials you want to simulate. It is a very quick and convenient solution. You don't need to calculate the quantity of specyfic atoms for each material in series.


![Window of app CDFFL](image.png "Window of app CDFFL")
## Usage 
If you want to use exe file for windows download CDFFL.zip (find it in Releases) and unpack it.
Run program CDFFL.exe in unpacked folder. Complete the form and run application by `<Start>` button. Folders with data will appear in the previously chosen directory. Now you can add your starting data created by CDFFL to your Lammps script e.g.:

```
atom_style	charge
dimension 	3
boundary	p p p

read_data	your_starting_data.txt #your starting data
```
In file  ```atoms_id.txt``` created by CDFFL you have ids for atoms in the equation entered in the program. 

If you are going to use the python interpreter, copy the repository and run user_GUI.py in the main folder. E.g.:

``` 
python user_GUI.py
```
or
``` 
python -m user_GUI.py
```
**notice**
The program generates randomly distributed atoms, while the charge is not homogeneous in the systems. For example, two positively charged ions may appear side by side. Therefore, it is good to set a small time step at the beginning of the simulation.

## Technologies/Tools

1. Python 3.9 
2. tkinter 
3. Python Standard Library modules 

## Tests 
I use Test-driven development technique for develope this program. You can find unit and GUI tests in test folder on Test and Dev branch. 

**Tools:** 
1. **pytest**
2. **allure** - for create raport 
3. **appium** with **WinAppDriver** - for GUI test 
4. **numpy** and **pandas** - for data preparation
