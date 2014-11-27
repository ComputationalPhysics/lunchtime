from setuptools import setup
setup(
    name='lunchtime',
    version='1.3',
    author="Svenn-Arne Dragly",
    author_email="s@dragly.com",
    description="CompPhys Lunchtime",
    packages=['lunchtime'],
    entry_points = {
        'gui_scripts' : ['lunchtime = lunchtime.lunchtime:main']
    },
    data_files = [
        ('share/applications/', ['lunchtime.desktop'])
    ],
)
