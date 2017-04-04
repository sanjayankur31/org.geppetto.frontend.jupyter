import setuptools
from glob import glob

#This block copies resources to the server (/usr/local/share/jupyter/nbextensions/)
data_files = []
data_files.append(('share/jupyter/nbextensions/jupyter_geppetto', glob('src/jupyter_geppetto/*.js')))
data_files.append(('share/jupyter/nbextensions/jupyter_geppetto', glob('src/jupyter_geppetto/*.css')))

setuptools.setup(
    name="jupyter_geppetto",
    version="0.0.1",
    url="https://github.com/openworm/org.geppetto.frontend.jupyter",
    author="The Geppetto Development Team",
    author_email="info@geppetto.org",
    description="Geppetto extension for Jupyter notebook",
    license="MIT",
    long_description=open('README.rst').read(),
    packages=setuptools.find_packages('src'),
    package_dir={'': 'src'},
    data_files=data_files,
    include_package_data=True,
    install_requires=[
        'ipywidgets>=5.1.5, <6.0',
        'widgetsnbextension>=1.2.6, <2.0',
        'jupyter>=1.0.0'
    ],
)