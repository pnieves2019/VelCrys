# VelCrys
VelCrys: Interactive web-based application to compute acoustic wave velocity in crystals and its magnetic corrections


Authors: P. Nieves, I. Korniienko, A. Fraile, J.M. Fernández-Díaz, R. Iglesias, D. Legut

-------------------------
WHAT IS VelCrys?
-------------------------

VelCrys is a web-based interactive tool, that allows to perform further post-processing of the elastic tensor in order to compute and plot the group velocity of the acoustic waves for any crystal symmetry. We also implemented the calculation of  effective magnetic corrections to the elastic tensor and corresponding fractional change in group velocity under a magnetic field.

-------------------------
ONLINE ACCESS
-------------------------

The application can be used online in the following link:

[http://www.md-esg.eu/velcrys/](http://www.md-esg.eu/velcrys/)

Note that this visualization tool can also be used offline by running it on your local computer, see details below.

--------------------------
OFFLINE AND DEVELOPER MODE
--------------------------

VelCrys can also be executed in your local computer. It requires to have ```Python3(>=3.6)```. For example, in Ubuntu Linux machine you can check the installed version of ```python3``` by opening a terminal and typing
```bash
python3 --version
```
In case you need to install python3 in your machine, you can type
```bash
sudo apt-get update
sudo apt-get install python3
```
Additionally, you need to install the following dependencies

```bash
dash(>=2.13.0)
plotly(>=5.17.0)
numpy(>=1.18.4)
```
you can easily install them with pip3
```bash
pip3 install dash
pip3 install plotly
pip3 install numpy
```
If you need to install pip3 on Ubuntu Linux, then type
```bash
sudo apt-get update
sudo apt-get install python3-pip
```
Once all depencencies are installed, download and extract the velcrys-master.zip file, go to the folder that contains the file ```velcrys.py``` and type
```bash
python3 velcrys.py
```
then visit http://127.0.0.1:8050/ in your web browser to use VelCrys.

**Compatibility issues**

On modern Linux, pip (pip3) may block global installs. A possible solution could be to use a virtual environment (venv):
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install <package_name>
```

Depending on the version of Dash, it may be needed to replace the last line in the velcrys.py file "app.run_server(debug=True)" with "app.run(debug=True)". 

------------------------------
DOCUMENTATION AND CITATION OF VelCrys
------------------------------

More details and examples of this application can be found in the published article:

P. Nieves, I. Korniienko, A. Fraile, J.M. Fernández-Díaz, R. Iglesias, D. Legut, VelCrys: Interactive web-based application to compute acoustic wave velocity in crystals and its magnetic corrections, SoftwareX 33 (2026) 102472.

[https://doi.org/10.1016/j.softx.2025.102472](https://doi.org/10.1016/j.softx.2025.102472) (Open access)

If you have used VelCrys, please cite it as

@article{NIEVES2026102472,\
author = {P. Nieves and I. Korniienko and A. Fraile and J.M. Fernández-Díaz and R. Iglesias and D. Legut},\
title = {VelCrys: Interactive web-based application to compute acoustic wave velocity in crystals and its magnetic corrections},\
journal = {SoftwareX},\
volume = {33},\
pages = {102472},\
year = {2026},\
doi = {https://doi.org/10.1016/j.softx.2025.102472} }

