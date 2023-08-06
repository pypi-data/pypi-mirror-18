import setuptools
import router_tools
import io, sys, os, codecs

setuptools.setup(
    name="router_tools",
    version=router_tools.__version__,
    url="https://github.com/renweibo/router_tools",
    license='MIT License',

    author="Ren Weibo",
    author_email="renweibo@gmail.com",

    description="A simple tool for router maintain.",
    long_description=open('README.md').read(),

    packages=setuptools.find_packages(),

    install_requires=[],

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    extras_require={
        'testing': ['pytest'],
    }
)
