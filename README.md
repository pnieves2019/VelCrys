# VelCrys
VelCrys: Interactive web-based application to compute acoustic wave velocity in crystals and its magnetic corrections


Authors: P. Nieves, I. Korniienko, A. Fraile, J.M. Fernández, R. Iglesias, D. Legut

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

------------------------------
DOCUMENTATION
------------------------------

More details of this application can be found in preprint available in arXiv:

P. Nieves, I. Korniienko, A. Fraile, J.M. Fernández, R. Iglesias, D. Legut, VelCrys: Interactive web-based application to compute acoustic wave velocity in crystals and its magnetic corrections, arXiv:2405.14416

[https://arxiv.org/pdf/2405.14416](https://arxiv.org/pdf/2405.14416)




