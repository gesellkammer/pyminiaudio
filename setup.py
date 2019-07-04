import os
import sys
import enum
import re
import textwrap
import unittest
from setuptools import setup

if sys.version_info < (3, 5):
    raise SystemExit("Miniaudio requires Python 3.5 or newer")

miniaudio_path = os.path.abspath(".")  # to make sure the compiler can find the required include files
PKG_VERSION = re.search(r'^__version__\s*=\s*"(.+)"', open("miniaudio.py", "rt").read(), re.MULTILINE).groups()[0]


def miniaudio_test_suite():
    testloader = unittest.TestLoader()
    testsuite = testloader.discover("tests", pattern="test*.py")
    return testsuite


if __name__ == "__main__":
    setup(
        name="miniaudio",
        version=PKG_VERSION,
        cffi_modules=["build_ffi_module.py:ffibuilder"],
        include_dirs=[miniaudio_path],
        zip_safe=False,
        include_package_data=False,
        py_modules=["miniaudio"],
        install_requires=["cffi>=1.3.0"],
        setup_requires=["cffi>=1.3.0"],
        tests_require=[],
        test_suite="setup.miniaudio_test_suite"
    )


def make_md_docs(modulename: str = "miniaudio", width: int = 100) -> str:
    import importlib
    import inspect
    module = importlib.import_module(modulename)
    documentable_classes = []
    documentable_enums = []
    documentable_functions = []
    for name, item in inspect.getmembers(module):
        if inspect.isclass(item) or inspect.isfunction(item):
            # consider only non-private classes and functions from the module itself
            if item.__module__ == modulename and not item.__name__.startswith('_'):
                if inspect.isclass(item):
                    if issubclass(item, enum.Enum):
                        documentable_enums.append((item.__name__, item))
                    else:
                        documentable_classes.append((item.__name__, item))
                elif inspect.isfunction(item):
                    documentable_functions.append((item.__name__, item))
    print("\n\n===================  GENERATED API DOCS  =================\n\n")
    for name, func in sorted(documentable_functions):
        doc = inspect.getdoc(func)
        if not doc:
            continue    # don't output if no docstring
        sig = str(inspect.signature(func))
        if sig.endswith("-> None"):
            sig = sig[:-7]
        print("*function*  ``{}  {}``\n".format(name, sig))
        for line in textwrap.wrap("> "+doc, width):
            print(line)
        print("\n")
    for name, enumk in sorted(documentable_enums):
        doc = inspect.getdoc(enumk)
        if not doc:
            continue    # don't output if no docstring
        print("*enum class*  ``{}``".format(name))
        print(" names:  ``{}``\n".format("`` ``".join(e.name for e in list(enumk))))
        for line in textwrap.wrap("> "+doc, width):
            print(line)
        print("\n")
    for name, klass in sorted(documentable_classes):
        doc = inspect.getdoc(klass)
        if not doc:
            continue    # don't output if no docstring
        sig = str(inspect.signature(klass.__init__))
        if sig.endswith("-> None"):
            sig = sig[:-7]
        print("*class*  ``{}``\n".format(name))
        print("``{}  {}``\n".format(name, sig))
        for line in textwrap.wrap("> "+doc, width):
            print(line)
        print("\n")
    print()
