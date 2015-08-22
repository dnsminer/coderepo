from distutils.core import setup

setup(
    name='DNSMiner',
    version='0.5',
    packages=['bin', 'utils', 'utils.patterns', 'utils.databases', 'reporting', 'dm_modules'],
    url='www.DNSMiner.net',
    license='Apache License 2.0',
    author='Doug Leece',
    author_email='dleece@firstfiretech.ca',
    description='Teh various python programs and modules needed for DNS Miner'
)
