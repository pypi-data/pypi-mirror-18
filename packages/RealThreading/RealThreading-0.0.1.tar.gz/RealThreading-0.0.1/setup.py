
try:
    from setuptools import setup,Extension
except ImportError:
    from distutils.core import setup,Extension

setup(
    name='RealThreading',
    version='0.0.1',
    packages=['rt'],
    url='',
    license='MIT',
    author='G.M',
    author_email='G.Mpydev@gmail.com',
    description="'A python's parallel processing module.",
    platforms='win32',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Natural Language :: English",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 3.5",
        "Topic :: Software Development :: Build Tools",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Hardware :: Symmetric Multi-processing",

    ],
    keywords=['threading', 'processing', 'parallel', 'multi-processing'],
    long_description=open('README.rst').read(),
    install_requires=['dill', 'pyil-converter'],
)
