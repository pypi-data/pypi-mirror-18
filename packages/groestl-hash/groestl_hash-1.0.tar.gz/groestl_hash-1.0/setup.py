from distutils.core import setup, Extension

groestl_hash_module = Extension('groestl_hash',
                               sources = ['groestlmodule.c',
                                          'groestl.c',
										  'sph/groestl.c',
										  'sph/sha2.c'],
                               include_dirs=['.', './sph','sha3'])


setup (name = 'groestl_hash',
       version = '1.0',
       description = 'Bindings for Groestl Used by MyriadCoin',
       ext_modules = [groestl_hash_module])
