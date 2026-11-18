from setuptools import find_namespace_packages, setup


setup(
    name="grace-imagegen",
    version="0.1.0",
    description="Grace's raster painting: MOSS-Image sidecar client and the 'image' canvas action bridge",
    python_requires=">=3.10",
    package_dir={"": "src"},
    packages=find_namespace_packages(where="src"),
    install_requires=["grace-canvas>=0.2.0"],
    entry_points={"console_scripts": ["imagegen = imagegen.cli:main"]},
)
