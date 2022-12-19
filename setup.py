from typing import List
from setuptools import find_packages, setup

def get_requirements()->List[str]:
    """
    This function will return list of requirements
    Returns:
        List[str]: requiremetns list
    """
    requirement_list:List[str]=[]
    # Code to read from requirements.txt file and append in requirement list.
    with open('requirements.txt', 'r') as file:
        line = file.readline()
        requirement_list.append(line)
    
    return requirement_list


setup(name='sonar',
      version='0.0.1',
      description='Python sonar mine and rock',
      author='Divyanshu Kesarwani',
      author_email='kingsapp14@gmail.com',
      url='https://www.python.org/sigs/distutils-sig/',
      packages=find_packages(),
      install_requires = get_requirements(),
     )