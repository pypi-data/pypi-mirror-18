from setuptools import setup, find_packages
from Cython.Build import cythonize

__version__ = '0.53'


setup(
    name="eudplib",
    version=__version__,
    packages=find_packages(),
    package_data={
        '': ['*.dll', '*.lst', '*.pyd'],
    },
    setup_requires=["cffi>=1.0.0"],
    install_requires=["cffi>=1.0.0"],
    ext_modules=cythonize([
        "eudplib/core/allocator/*.pyx",
        "eudplib/utils/*.pyx",
    ]),

    # metadata for upload to PyPI
    author="Trgk",
    author_email="whyask37@naver.com",
    description="EUD Trigger generator",
    license="MIT license",
    keywords="starcraft rawtrigger eud",
    url="http://blog.naver.com/whyask37/",  # project home page, if any
)
