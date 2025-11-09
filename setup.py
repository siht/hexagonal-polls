from setuptools import setup, find_packages

# Se lee la versión del pyproject.toml o se usa la versión hardcodeada 
# si no quieres depender de la lectura de archivos.
# Usaremos 1.3.0 directamente por simplicidad y fiabilidad.

setup(
    name='hexagonal-polls',
    version='1.5.1',
    description='Core domain contracts for the Hexagonal Polls application.',
    
    # 1. Indicamos a Setuptools que busque paquetes DENTRO de la carpeta 'src'.
    packages=find_packages(where='src'),
    
    # 2. Indicamos que el directorio raíz de los paquetes es 'src'.
    package_dir={'': 'src'},
    
    # Añadimos las dependencias para que se instalen junto con el paquete
    install_requires=[
        # Usamos la versión de Twisted que definiste en tu pyproject.toml
        'Twisted~=25.5.0', 
    ],
)
