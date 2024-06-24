from setuptools import setup, find_packages

setup(
    name="dedged",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "cryptography",
        "questionary",
    ],
    entry_points={
        'console_scripts': [
            'dedged=Dedged:main',
        ],
    },
)
