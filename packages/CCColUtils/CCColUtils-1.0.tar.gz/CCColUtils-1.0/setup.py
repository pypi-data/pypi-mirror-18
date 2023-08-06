from distutils.core import setup, Extension

cccolutils = Extension('cccolutils',
                       libraries = ['krb5', 'k5crypto', 'com_err'],
                       sources = ['cccolutils.c'])

setup (name='CCColUtils',
       version='1.0',
       description='Kerberos5 Credential Cache Collection Utilities',
       ext_modules=[cccolutils],
       author='Patrick Uiterwijk',
       author_email='puiterwijk@redhat.com',
       license='GPLv2+')
