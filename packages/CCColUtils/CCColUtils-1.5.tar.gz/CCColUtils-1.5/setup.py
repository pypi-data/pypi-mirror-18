from setuptools import setup, Extension

cccolutils = Extension('cccolutils',
                       libraries = ['krb5', 'k5crypto', 'com_err'],
                       sources = ['cccolutils.c'])

setup (name='CCColUtils',
       version='1.5',
       description='Kerberos5 Credential Cache Collection Utilities',
       ext_modules=[cccolutils],
       author='Patrick Uiterwijk',
       author_email='puiterwijk@redhat.com',
       license='GPLv2+',
       url='https://pagure.io/cccolutils',
       test_suite="tests",
       packages=[])
