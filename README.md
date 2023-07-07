# About SELDOMpy

SELDOMpy is a Python package that generates dynamic models of cell signalling networks from experimental data. The SELDOMpy algorithm consists of the following steps:
- **Calculation of the adjacency matrix** of the network from the mutual information between all possible pairs of nodes.
- **Generation of an initial dynamic network model** from the adjacency matrix above.
- **Optimisation** of the value obtained from the simulation of the model.
- **Reduction** of the number of model arrow arcs using the Akaike criterion.
- **Simulation and saving** of the final model and graphs obtained from its simulation. 

SELDOMpy implements the algorithm from the R package [SELDOM](https://zenodo.org/record/250558).
The purpose of SELDOMpy is to create a more accessible and user-friendly tool than SELDOM. 
It works well with simple networks, but it is not as efficient as SELDOM in larger networks since it does not have such specific optimization tools.

SELDOMpy was created by **Luis Prado López**, <pradolopezluis@gmail.com>, under the supervision of [Alejandro F. Villaverde](http://afvillaverde.webs.uvigo.gal/), <afvillaverde@uvigo.gal> and [David Saque Henriques](https://www.iim.csic.es/es/personal/david-saque), <davidh@iim.csic.es>. 

## Installation and requirements
SELDOMpy requires Python 3. 
It also consists of .c files, so there are 2 installation possibilities:

a) If you are using a **64-bit Windows with Python 3.8**: You can install SELDOMpy directly using the following command: 

   `pip install SELDOMpy`

b) If you are using **other Python versions and operating systems**: You need to have a C compiler installed (such as Visual Studio) and follow the commands below:
  
  `pip install numpy`
  
  `python -m pip install pip==22.0.4`
  
  `pip install SELDOMpy`
  
  Once installed you can update pip to the latest version if you wish using `python -m pip install --upgrade pip`

## Getting started
The first thing is to install the package as indicated above depending on your terminal.
To be able to use SELDOMpy in your Python project you can import all its functions with the following command: 

`from SELDOMpy import *`

Once imported, you can perform the steps indicated in the first section following the PDF manual that includes the package.
 
## Results
The results of the final cell signaling network model are saved in a binary file (in the path indicated by the user). These results can be imported into Python if the user wishes and thus check the values of the model.
You can also plot the results obtained from the simulation of the final model together with the experimental measurements of the nodes to verify that the modeling was performed correctly using the _plot_results_ function. 

More information about SELDOMpy can be found in the [SELDOMpy manual](SELDOMpy/doc/SELDOMpy_manual.pdf)

## Disclaimer

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, version 3 of the License.
    
This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  
See the GNU General Public License for more details.
 
You should have received a copy of the GNU General Public License along with this program. If not, see <http://www.gnu.org/licenses/>.
