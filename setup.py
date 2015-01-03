from distutils.core import setup

setup(
    name='murmgr',
    version='0.1',
    packages=[''],
    url='https://github.com/CognitionGuidedSurgery/murmgr',
    license='GPL v3',
    author='Alexander Weigl',
    author_email='uiduw@student.kit.edu',
    description='Management of MSML User Packages and Repositories',
    requires=['cliff', 'click', 'path.py', 'colorama'],
    entry_points='''
        [console_scripts]
        murmgr=murmgr:cli
    ''',
)
