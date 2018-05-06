import os
import unittest

from utils import extract

code_blocks = []


class testREADME(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open('README.md') as f:
            code_blocks.extend(extract(f, filter='python'))

    def setUp(self):
        os.makedirs('temp')
        os.chdir('temp')

    def tearDown(self):
        os.chdir('..')
        os.rmdir('temp')

    def test_Readme(self):
        for code_block in code_blocks:
            compile(code_block[0], 'random.py', mode='exec')
