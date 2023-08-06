from setuptools import setup, find_packages

setup(
    name='dsmr-parser',
    description='Library to parse Dutch Smart Meter Requirements (DSMR)',
    author='Nigel Dokter',
    author_email='nigeldokter@gmail.com',
    url='https://github.com/ndokter/dsmr_parser',
    version='0.4',
    packages=find_packages(),
    install_requires=[
        'pyserial>=3,<4',
        'pyserial-asyncio<1',
        'pytz'
    ],
    entry_points={
        'console_scripts': ['dsmr_console=dsmr_parser.__main__:console']
    },
)
