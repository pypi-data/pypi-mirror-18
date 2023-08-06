from setuptools import setup

setup(
        name="pyOfx",
        version="0.1.4",
        author="Steven Rossiter",
        author_email="steve@flexsis.co.uk",
        description=("A wrapper around OrcFxAPI by Orcina "
                     "to add extra functionality."),
        license="MIT",
        keywords="orcaflex api wrapper subsea engineering",
        url="https://pythonhosted.org/pyOfx/",
        packages=['pyofx'],
        classifiers=[
            "Development Status :: 4 - Beta",
            "Environment :: Win32 (MS Windows)",
            "Topic :: Utilities",
            "Natural Language :: English",
            "License :: OSI Approved :: MIT License",
            "Operating System :: Microsoft :: Windows",
            "Programming Language :: Python :: 2.7",
            "Programming Language :: Python :: 3.4",
            "Topic :: Scientific/Engineering :: Physics"
        ],
)
