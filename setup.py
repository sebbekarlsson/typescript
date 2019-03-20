from setuptools import setup, find_packages


setup(
    name='typescript',
    version='1.0.0',
    install_requires=[
        'jinja2'
    ],
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'typescript = typescript.bin:run'
        ]
    }
)
