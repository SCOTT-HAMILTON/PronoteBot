from setuptools import setup, find_packages

setup(
    name='PronoteBot',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    py_modules = [ 'pronotebot', 'cli' ],

    install_requires=['selenium', 'pybase64', 'Click', 'pyautogui', 'wget'],

    entry_points='''
        [console_scripts]
        pronotebot=PronoteBot.cli:cli
    ''',

    # metadata to display on PyPI
    author='Scott Hamilton',
    author_email='sgn.hamilton+python@protonmail.com',
    description='Converts an excel timetable to a C++ header',
    keywords='timetable header conversion',
    url='https://github.com/SCOTT-HAMILTON/TimeTable2Header',
    project_urls={
        'Source Code': 'https://github.com/SCOTT-HAMILTON/TimeTable2Header',
    },
    classifiers=[
        'License :: OSI Approved :: Python Software Foundation License'
    ]
)
