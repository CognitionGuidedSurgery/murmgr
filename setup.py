from setuptools import setup

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
    install_requires=['cliff', 'click', 'path.py', 'colorama', 'pyyaml'],
    entry_points={
        'console_scripts': [
            'murmgr=murmgr:cli'
        ],
    },
    classifiers=(
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)", "Operating System :: Unix",
        "Operating System :: POSIX",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Utilities",
    )
)
