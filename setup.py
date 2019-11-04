import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="5e-combat-simulator-jvasilakes",
    version="0.0.1",
    author="Jake Vasilakes",
    author_email="jvasilakes@gmail.com",
    description="A combat simulator for Dungeons and Dragons 5e",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages() + ["combat_simulator"],
    package_data={"combat_simulator": ["data/", "character_sheets/"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
