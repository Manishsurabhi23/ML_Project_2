'''
The setup.py file is an essential part of packaging and distributing python projects. It is used by setuptools
(or disutils in older Python versions) to define the configuration of your project, such as metadata, dependencies, and more 
'''

from setuptools import setup, find_packages
from typing import List


HYPEN_E_DOT = '-e .'

def get_requirements(file_path:str) -> List[str]:
    """Reads the requirements from a file and returns them as a list."""
    try:
        with open(file_path, 'r') as file:
            requirements = file.readlines()
            requirements = [req.replace('\n', '') for req in requirements]
            if HYPEN_E_DOT in requirements:
                requirements.remove(HYPEN_E_DOT)
    except FileNotFoundError:
        print("requirements.txt file not found")
    return requirements
    
setup(
    name='NetworkSecurity',
    version='0.0.1',
    author='Manish Surabhi',
    author_email='manishsurabhi23@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt')
)