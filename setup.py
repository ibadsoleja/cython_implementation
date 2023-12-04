#from setuptools import setup
from Cython.Build import cythonize
from setuptools import setup
import numpy
setup(
    name='Cythonized Scripts',
    ext_modules=cythonize(["adjusted_functions2.pyx", "pedro_main.pyx"]),
    include_dirs=[numpy.get_include()],
    zip_safe=False,
)