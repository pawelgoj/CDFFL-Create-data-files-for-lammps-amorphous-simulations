"""
@author: Pawel Goj
"""
from main.program import cord_rand

class MockFactory:
    @staticmethod
    def get_EquationOfMaterial_class():
        return cord_rand.EquationOfMaterial
    @staticmethod
    def get_CompositionOfMaterial_class():
        return cord_rand.CompositionOfMaterial

