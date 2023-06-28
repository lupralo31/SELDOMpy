from setuptools import setup, find_packages

VERSION = '0.0.1.5'
DESCRIPTION = 'Package for modelling cellular signalling networks'
readme = open("README.md", "r")
# Configurando
setup(
    # el nombre debe coincidir con el nombre de la carpeta
    # 'modulomuysimple'
    name="SELDOMpy",
    version=VERSION,
    author="Luis Prado",
    author_email="<pradolopezluis@gmail.com>",
    description=DESCRIPTION,
    long_description=readme.read(),
    long_description_content_type='text/markdown',
    url='https://github.com/lupralo31/SELDOMpy',
    download_url='https://github.com/lupralo31/SELDOMpy',
    license='MIT',
    packages=find_packages(),
    install_requires=["numpy", "scikit-learn", "pandas", "mealpy", "matplotlib", "setuptools"],  # añade cualquier paquete adicional que debe ser
    # instalado junto con tu paquete. Ej: 'caer'

    keywords=['python', 'SELDOMpy'],
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    package_dir={'SELDOMpy': 'SELDOMpy'},
    package_data={"SELDOMpy": ['binaries/*.pyd']}
)