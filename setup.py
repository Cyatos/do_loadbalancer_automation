from setuptools import setup

setup(
    name='dolb_cli',
    version='1.0.0',
    py_modules=['loadbalancer'],
    install_requires=[
        'requests',
        'fire'],
    entry_points='''
        [console_scripts]
        dolb_cli=loadbalancer:main
    ''',
)
