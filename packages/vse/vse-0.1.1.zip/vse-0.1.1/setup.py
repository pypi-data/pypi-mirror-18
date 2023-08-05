from setuptools import setup

setup(name='vse',
      version='0.1.1',
      author='Marcin K. Paszkiewicz',
      author_email='mkpaszkiewicz@gmail.com',
      description='Configurable visual search engine based on the OpenCV',
      url='https://github.com/mkpaszkiewicz/vse',
      download_url='https://github.com/mkpaszkiewicz/vse/zipball/0.1.1',
      packages=['vse', 'bin'],
      keywords=['visual', 'search', 'engine', 'computer', 'vision'],
      install_requires=[
          'NumPy',
          'scipy',
      ]
      )
