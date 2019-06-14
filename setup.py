from setuptools import setup

setup(
    name='novac-bot',
    version='2.0.0',
    packages=['Core', 'Market', 'Fleetup', 'Navigation', 'Miscellaneous'],
    url='https://github.com/no-vacancies/novac-bot',
    license='MIT',
    author='No Vacancies',
    author_email='',
    description='Discord bot providing various EVE Services for No Vacancies',
    install_requires = [
        'esipy',
        'cachecontrol',
        'pandas',
        'numpy',
        'requests',
        'discord',
        'diskcache',
        'lockfile'
    ]
)
