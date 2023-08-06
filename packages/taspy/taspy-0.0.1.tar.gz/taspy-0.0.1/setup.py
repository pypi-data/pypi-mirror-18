from setuptools import find_packages, setup


setup(
    name='taspy',
    version='0.0.1',
    license='GPL3',
    description='',
    # long_description=open('README.rst').read(),
    author='Philipp Schmitt',
    author_email='philipp@schmitt.co',
    url='https://github.com/pschmitt/taspy',
    packages=find_packages(),
    install_requires=['wireless'],
)
