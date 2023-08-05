Setuptools Binary Targets
=========================

Distutils/Setuptools provides a fantastic cross platform framework for
building python packages, including binary extensions using your platforms
standard c/c++ compiler.

Why should it be limited only to use on python pyd extensions however,
there's nothing to stop it being used for compiling anything with said comiler,
such as executables and static libraries.

Well it turns out all the functionality is already there, it just isn't really
exposed to the end user very easily. This is easily rectified however::

    from setuptools import setup
    from ext_targets import build_ext, StaticLib, Executable


    setup(
        name='binaries!',  # This isn't actually used in the built targets
        cmdclass={'build_ext': build_ext},
        ext_modules=ext_modules = [
            StaticLib(
                name='saveforlater',
                sources=['lib.c', 'required.c'],
                include_dirs=['../include']
            ),
            Executable(
                name='my_program',
                sources=['source.c', 'extra.cpp'],
                libraries=['libsaveforlater']
                language='c++',
                include_dirs=['../include'],
                extra_compile_args=['-static'],
                extra_link_args=['-static']
            )
        ]
    )
