"""
    This module contains the unit test cases
"""
import unittest

from translator import englishtofrench, englishtogerman

class TestEnglishToFrench(unittest.TestCase):
    def test1(self):
        self.assertEqual(englishtofrench('Hello'), 'Bonjour') # test when 'Hello' is given as input the output is 'Bonjour'.
        self.assertEqual(englishtofrench(''), '')  # test when '' is given as input the output is ''.
        self.assertEqual(englishtofrench('Yes'), 'Oui')  # test when 'Yes' is given as input the output is 'Oui'.

class TestEnglishToGerman(unittest.TestCase): 
    def test1(self): 
        self.assertEqual(englishtogerman('Hello'), 'Hallo') # test when 'Hello' is given as input the output is 'Hallo'.
        self.assertEqual(englishtogerman(''), '')  # test when '' is given as input the output is ''.
        self.assertEqual(englishtogerman('Yes'), 'Ja')  # test when 'Yes' is given as input the output is 'Ja'.

unittest.main()