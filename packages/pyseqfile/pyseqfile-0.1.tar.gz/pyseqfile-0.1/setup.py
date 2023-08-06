from setuptools import setup
from setuptools import Extension
from Cython.Build import cythonize
from distutils.command.sdist import sdist as _sdist

cmdclass = {}


class sdist(_sdist):

    def run(self):
        # Make sure the compiled Cython files in the distribution are
        # up-to-date
        from Cython.Build import cythonize
        cythonize(['pyseqfile/seqfile.pyx'])
        _sdist.run(self)
cmdclass['sdist'] = sdist

setup(
    name='pyseqfile',
    version='0.1',
    packages=[
        'pyseqfile'
    ],
    license='MIT',
    url='http://github.com/phelimb/remcdbg',
    description='Pyseqfile is a python wrapper on top of [seq_file](https://github.com/noporpoise/seq_file) which allow for reading multiple sequence file formats.',
    ext_modules=cythonize(
        [Extension("pyseqfile/seqfile", ["pyseqfile/seqfile.pyx"])]),
    install_requires=[
        'cython'],
    cmdclass=cmdclass

)
