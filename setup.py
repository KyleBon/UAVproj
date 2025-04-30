from setuptools import setup, find_packages

setup(
    name='uavsat',
    version='0.2.0',
    description='UAV SAT Path Validator using PySAT',
    author='Your Name',
    author_email='justin.williams1@students.cau.edu',
    packages=find_packages(),
    install_requires=[
        'python-sat[pblib,aiger]',
    ],
    entry_points={
        'console_scripts': [
            'uavsat=uavsat.core:main'
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
