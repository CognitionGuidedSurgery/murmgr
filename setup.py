from distutils.core import setup

setup(
    name='murmgr',
    version='1.0.0-beta',
    url='https://github.com/CognitionGuidedSurgery/murmgr',
    license='GPL v3',
    py_modules=['murmgr'],
    author='Alexander Weigl',
    author_email='uiduw@student.kit.edu',
    description='Management of MSML User Packages and Repositories',
    requires=['cliff', 'click', 'path.py', 'colorama'],
    entry_points='''
        [console_scripts]
        murmgr=murmgr:cli
    ''',
    classifiers=(
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)"
    )
)
