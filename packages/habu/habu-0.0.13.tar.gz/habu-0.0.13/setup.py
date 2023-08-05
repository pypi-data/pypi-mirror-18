from setuptools import setup

with open('README.rst') as f:
    readme = f.read()

setup(
    name='habu',
    version='0.0.13',
    description='Ethical Hacking Utils',
    long_description=readme,
    author='Fabian Martinez Portantier',
    author_email='fportantier@securetia.com',
    url='https://gitlab.com/securetia/habu',
    license='GNU General Public License v3 (GPLv3)',
    install_requires=[
        'Click',
        'Requests',
    ],
    tests_require=[
        'pytest',
        'pytest-runner',
    ],
    packages=['habu'],
    include_package_data=True,
    entry_points='''
        [console_scripts]
        habu.ip=habu.cli.cmd_ip:cmd_ip
        habu.xor=habu.cli.cmd_xor:cmd_xor
        habu.contest=habu.cli.cmd_contest:cmd_contest
    ''',
    classifiers=[
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Topic :: Security",
        "Topic :: System :: Networking",
        "Programming Language :: Python :: 3.0",
        "Programming Language :: Python :: 3.6",
    ],
    keywords=['security'],
    zip_safe=False,
    test_suite='py.test',
)
