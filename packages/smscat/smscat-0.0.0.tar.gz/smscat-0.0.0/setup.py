from setuptools import setup


setup(
    name='smscat',
    version='0.0.0',
    author='Mark Smith',
    author_email='mark.smith@nexmo.com',
    packages=['smscat'],
    entry_points='''
        [console_scripts]
        sms=smscat:main
    ''',
)
