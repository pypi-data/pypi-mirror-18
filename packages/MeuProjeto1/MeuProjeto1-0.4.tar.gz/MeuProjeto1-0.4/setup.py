from setuptools import setup, find_packages
with open('README.rst') as f:
    readme = f.read()
setup(name='MeuProjeto1',
      version='0.4',
      author='Jhonnatha de Andrade Monteiro',
      author_email='jhonnatha.am@gmail.com',
      license='MIT',
      description='Example package that calculate thermodynamic data',
      long_description=readme,
      packages=find_packages())