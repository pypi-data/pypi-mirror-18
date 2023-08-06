from setuptools import setup, find_packages

setup(name='bibfix',
      version='0.2',
      description='Puts curly braces around acronyms in titles in '
                  'bibtex files.',
      author='Johannes Wienke',
      author_email='languitar@semipol.de',
      license='LGPLv3+',

      install_requires=[
          'bibtexparser>=0.6.1'
      ],

      entry_points={
          'console_scripts': [
              'bibfix = bibfix:main'
          ]
      },

      py_modules=['bibfix'],
      )
