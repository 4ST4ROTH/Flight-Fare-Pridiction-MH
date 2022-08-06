from setuptools import setup , find_packages
from typing import List

#Declaring variables for setup function:

PROJECT_NAME = 'Flight-fare-predictor'
VERSION = '0.0.1'
AUTHOR = 'Mohan Singh'
DESCRIPTION = 'The main goal is to predict the fares of the flights based on different factors available in the provided dataset.'

REQUIREMENT_FILE_NAME = 'requirements.txt'

HYPHEN_E_DOT = '-e .'

def get_requirements_list () -> List[str]:
    """Description: This function is going to return list of requirement
    mention in requirements.txt file
    return This function is going to return a list which contain name
    of libraries mentioned in requirements.txt file"""
    with open(REQUIREMENT_FILE_NAME) as requirement_file:
        requirements = requirement_file.readlines()
        requirement_list = [requirement_name.replace('\n',' ') for requirement_name in requirements]
        if HYPHEN_E_DOT in requirement_list:
            requirement_list.remove(HYPHEN_E_DOT)
        return requirement_list


setup(
    name = PROJECT_NAME,
    version = VERSION,
    author = AUTHOR,
    description = DESCRIPTION,
    packages =find_packages(),
    install_requirements = get_requirements_list()
)



