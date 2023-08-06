from setuptools import setup, find_packages

setup(
    name='telstra-sms-sdk',
    version='0.0.1',
    keywords=('telstra', 'sms','sdk'),
    description='A 3rd party python sdk allow you to send sms easily.',
    license='MIT License',
    install_requires=['click>=6.6', 'requests>=2.12.3'],

    author='Yang Liu',
    author_email='arkilis@gmail.com',

    packages=find_packages(),
    platforms='any',
)
