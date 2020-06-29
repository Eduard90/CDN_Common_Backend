from setuptools import setup, find_packages


setup(
    name='cdn_common',
    version='0.1',
    packages=find_packages(exclude=['tests*']),
    license='GPLv3',
    description='CDN Common (shared) package',
    long_description=open('README.md').read(),
    install_requires=['aiohttp', 'asyncio-nats-client[nkeys]', 'marshmallow', 'protobuf'],
    # url='',
    author='Eduard Kalashnikov',
    author_email='ytko90@gmail.com'
)
