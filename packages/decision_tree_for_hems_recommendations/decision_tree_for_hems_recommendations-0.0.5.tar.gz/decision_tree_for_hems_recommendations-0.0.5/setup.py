from setuptools import setup, find_packages

setup(
    name="decision_tree_for_hems_recommendations",
    version="0.0.5",
    author="Shintaro Ikeda",
    author_email="ikenshirogivenup98@gmail.com",
    license="MIT",
    url="",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.11.2",
        "scipy>=0.18.1",
        "scikit-learn>=0.18.1",
        "pyowm>=2.5.0",
        "tenkishocho>=0.0.7",
    ],
)
