from setuptools import setup, find_packages

setup(
    name='telstra-sms-sdk',
    version='0.0.2',
    keywords=('telstra', 'sms','sdk'),
    description='A 3rd party python sdk allow you to send sms easily.',
    license='MIT License',
    install_requires=['requests>=2.12.3'],

    author='Yang Liu',
    author_email='arkilis@gmail.com',

    packages=find_packages(),
    platforms='any',
)
