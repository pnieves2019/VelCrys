# -*- coding: utf-8 -*-

# Run this app with `python3 velcrys.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import os
import dash
#import dash_core_components as dcc
from dash import dcc
#import dash_html_components as html
from dash import html
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import mpmath
import cmath
from sympy import *
from dash.dependencies import Input, Output, State
from scipy.optimize import minimize


app = dash.Dash(__name__)

server = app.server

app.config.suppress_callback_exceptions = True

app.layout = html.Div(children=[
    html.H1(children='VelCrys: A tool to Compute Sound Velocity in Crystals'),
    html.Hr(),
    html.H5('P. Nieves, J.M. Fernández, R. Iglesias'),
    html.H6('Universidad de Oviedo, Spain'),
    html.H5('A. Fraile'),
    html.H6('Centro de Física de Materiales (CFM) CSIC-UPV/EHU, San Sebastián, Spain'),
    html.H5('I. Korniienko, D. Legut'),
    html.H6('IT4Innovations, VSB - Technical University of Ostrava, Czech Republic'),
    html.Hr(),

    html.H3("Introduction"),
    dcc.Markdown('''The propagation of elastic waves in anisotropic media, i.e. crystals, depends on the crystal symmetry and it is more complicated than in isotropic media. This interactive applet computes and plots the sound velocity (group velocity) of three kinds of seismic waves (qP, qS1, and qS2) for any crystal symmetry. It also includes the possibility to calculate the effective magnetic corrections to the elastic tensor and corresponding fractional change in sound velocity due to an external magnetic field (this option is currently supported only for Cubic I and Hexagonal I symmetries).'''),
    
    
    
    html.H3("Methodology"),
    dcc.Markdown('''The calculation of group velocity v for any crystal symmetry is performed by computing the analytical solution derived by Di Wang et al. [Geophysics 2023; 88 (4): C111–C121](https://doi.org/10.1190/geo2022-0566.1)'''),
    
    dcc.Markdown('$$v_l(C_{ij})= \\frac{\partial c}{ \partial n_l} = \\frac{\partial \omega} {\partial k_l},   l=x,y,z$$', mathjax=True),
   
    dcc.Markdown('''where $c=\omega/k$ is the phase velocity, and **n**=**k**/k is the unit vector of phase velocity direction (ray direction). The effective magnetic corrections to elastic tensor are obtained through the formulas derived by Rinaldi and Turilli [Phys. Rev. B, 31, 3051 (1985)](https://doi.org/10.1103/PhysRevB.31.3051)''', mathjax=True),
     
    dcc.Markdown('$$\Delta C_{ij} = \\frac{b^2α^2\chi}{M_s^2}$$', mathjax=True),
    
    dcc.Markdown('''where $b$ are magnetoelastic constants, $M_s$ is saturation magnetization, α is direction cosine of magnetization at equilibrium, and $\chi$ is the susceptibility tensor. Note that Rinaldi and Turilli expressions account for Simon effect but do not include higher order corrections like morphic and rotational-magnetostrictive effects.  The corresponding fractional change in group velocity due to magnetic effects is obtained by computing Di Wang et al. formulas using the elastic tensor including effective magnetic corrections, that leads to $v$, and elastic tensor without effective magnetic corrections which gives $v_0$, that is''', mathjax=True),

    dcc.Markdown('$$\\frac{v-v_0}{v_0}=\\frac{v(C_{ij}+\Delta C_{ij})-v(C_{ij})}{v(C_{ij})}$$', mathjax=True),
    
    dcc.Markdown('''This option is currently supported only for Cubic I (space group numbers 207-230), and Hexagonal I (space group numbers 177-194) symmetries.''', mathjax=True),


    html.Hr(),
    html.H3("Select the type of calculation:"),
    dcc.Dropdown(
                id='mode',
                options=[
                    {'label': 'Numerical evaluation of group velocity at a single wave vector k (all crystal symmetries)', 'value': 'numerical'},
                    {'label': '3D plot of group velocity (all crystal symmetries)', 'value': 'landscapec'},
                    {'label': 'Effective magnetic corrections to elastic tensor (Cubic I)', 'value': 'magnetic_cub'},
                    {'label': 'Effective magnetic corrections to elastic tensor (Hexagonal I)', 'value': 'magnetic_hex'},
                    {'label': '3D plot of fractional change in group velocity due to magnetic field (Cubic I)', 'value': 'magnetic_cub_field'},
                    {'label': '3D plot of fractional change in group velocity due to magnetic field (Hexagonal I)', 'value': 'magnetic_hex_field'},
                ],
                placeholder="Select the type of calculation"
             ),
           
    html.Div(id='mode_output'),




    html.Hr(),
    html.H3("Bibliography"),
    html.H6(" [1] Di Wang, Chao-Ying Bai, Xing-Wang Li, and Jing Hu, Analytic formula for the group velocity and its derivatives with respect to elastic moduli for a general anisotropic medium, Geophysics 2023; 88 (4): C111–C121. "),
    dcc.Markdown('''[https://doi.org/10.1190/geo2022-0566.1](https://doi.org/10.1190/geo2022-0566.1)'''),
    html.H6(" [2] S. Rinaldi and G. Turilli, Theory of linear magnetoelastic effects, Phys. Rev. B, 31, 3051 (1985). "),
    dcc.Markdown('''[https://doi.org/10.1103/PhysRevB.31.3051](https://doi.org/10.1103/PhysRevB.31.3051)'''),
    html.H3("Source files"),
    dcc.Markdown('''[https://github.com/pnieves2019/VelCrys](https://github.com/pnieves2019/VelCrys)'''),
    html.Hr(),


])

             


@app.callback(
    dash.dependencies.Output('mode_output', 'children'),
    [dash.dependencies.Input('mode', 'value'),
    ])



def update_landscape(mode):

  if mode == 'numerical': 
    
      return html.Div(children=[
            
            html.H4("Numerical evaluation of sound velocity (group velocity)"),
            html.H6("(Press Enter after changing any input to update the calculated values)"),
            dcc.Markdown(''' **Elastic tensor:**'''),
            html.Div(['C',html.Sub('11'),'(GPa)'" = ",
              dcc.Input(id='c11tric', value=200.125, type='number', debounce=True, step=0.001),
                      'C',html.Sub('12'),'(GPa)'" = ",
              dcc.Input(id='c12tric', value=150.456, type='number', debounce=True, step=0.001),
                      'C',html.Sub('13'),'(GPa)'" = ",
              dcc.Input(id='c13tric', value=150.456, type='number', debounce=True, step=0.001),             
                      'C',html.Sub('14'),'(GPa)'" = ",
              dcc.Input(id='c14tric', value=150.456, type='number', debounce=True, step=0.001),
                      'C',html.Sub('15'),'(GPa)'" = ",
              dcc.Input(id='c15tric', value=150.456, type='number', debounce=True, step=0.001),
                      'C',html.Sub('16'),'(GPa)'" = ",
              dcc.Input(id='c16tric', value=150.456, type='number', debounce=True, step=0.001),        
              ]),
            html.Div(['C',html.Sub('22'),'(GPa)'" = ",
              dcc.Input(id='c22tric', value=200.125, type='number', debounce=True, step=0.001),
                      'C',html.Sub('23'),'(GPa)'" = ",
              dcc.Input(id='c23tric', value=150.456, type='number', debounce=True, step=0.001),
                      'C',html.Sub('24'),'(GPa)'" = ",
              dcc.Input(id='c24tric', value=150.456, type='number', debounce=True, step=0.001),             
                      'C',html.Sub('25'),'(GPa)'" = ",
              dcc.Input(id='c25tric', value=150.456, type='number', debounce=True, step=0.001),
                      'C',html.Sub('26'),'(GPa)'" = ",
              dcc.Input(id='c26tric', value=150.456, type='number', debounce=True, step=0.001),        
              ]),  
            html.Div(['C',html.Sub('33'),'(GPa)'" = ",
              dcc.Input(id='c33tric', value=150.456, type='number', debounce=True, step=0.001),
                      'C',html.Sub('34'),'(GPa)'" = ",
              dcc.Input(id='c34tric', value=150.456, type='number', debounce=True, step=0.001),             
                      'C',html.Sub('35'),'(GPa)'" = ",
              dcc.Input(id='c35tric', value=150.456, type='number', debounce=True, step=0.001),
                      'C',html.Sub('36'),'(GPa)'" = ",
              dcc.Input(id='c36tric', value=150.456, type='number', debounce=True, step=0.001),        
              ]), 
              
            html.Div(['C',html.Sub('44'),'(GPa)'" = ",
              dcc.Input(id='c44tric', value=150.456, type='number', debounce=True, step=0.001),             
                      'C',html.Sub('45'),'(GPa)'" = ",
              dcc.Input(id='c45tric', value=150.456, type='number', debounce=True, step=0.001),
                      'C',html.Sub('46'),'(GPa)'" = ",
              dcc.Input(id='c46tric', value=150.456, type='number', debounce=True, step=0.001),        
              ]),  
              
            html.Div(['C',html.Sub('55'),'(GPa)'" = ",
              dcc.Input(id='c55tric', value=150.456, type='number', debounce=True, step=0.001),
                      'C',html.Sub('56'),'(GPa)'" = ",
              dcc.Input(id='c56tric', value=150.456, type='number', debounce=True, step=0.001),        
              ]), 
              
            html.Div(['C',html.Sub('66'),'(GPa)'" = ",
              dcc.Input(id='c66tric', value=150.456, type='number', debounce=True, step=0.001),                    
              ]), 
            dcc.Markdown(''' **Mass density:**'''),
            html.Div(['\u03C1','(kg/m',html.Sup("3"),')'" = ",
              dcc.Input(id='rhotric', value=10000.429, type='number', debounce=True, step=0.001)]),
            dcc.Markdown(''' **Wave vector k (phase velocity direction):**'''),
            html.Div(['k',html.Sub('x'),'(rad/m)'" = ",
              dcc.Input(id='kxtric', value=1.995774956, type='number', debounce=True, step=0.000000001)]),
            html.Div(['k',html.Sub('y'),'(rad/m)'" = ",
              dcc.Input(id='kytric', value=0.865988622, type='number', debounce=True, step=0.000000001)]),
            html.Div(['k',html.Sub('z'),'(rad/m)'" = ",
              dcc.Input(id='kztric', value=-1.310698633, type='number', debounce=True, step=0.000000001)]),
            dcc.Markdown(''' **Choose one of the 3 solutions (qP, qS1 and qS2) to compute:**'''),
            dcc.Dropdown(
                id='sol_num_tric',
                options=[
                    {'label': 'qP wave', 'value': 'sol_1'},
                    {'label': 'qS1 wave', 'value': 'sol_2'},
                    {'label': 'qS2 wave', 'value': 'sol_3'},
                ],
                value='sol_1'
            ),
            
            dcc.Loading(id="ls-loading-tric", children=[html.Table([
                html.Tr([html.Td(['Calculated value of group velocity:'])]),
                html.Tr([html.Td(['v', html.Sub('x'),'(m/s) = ']), html.Td(id='vxnumtric')]),
                html.Tr([html.Td(['v', html.Sub('y'),'(m/s) = ']), html.Td(id='vynumtric')]),
                html.Tr([html.Td(['v', html.Sub('z'),'(m/s) = ']), html.Td(id='vznumtric')]),
                html.Tr([html.Td(['|v|','(m/s) = ']), html.Td(id='v0numtric')]),
            ])], type="default",fullscreen=False,debug=False),
            
      ]) 


           
  elif mode == 'landscapec': 
    
      return html.Div(children=[
            
            html.H4("3D plot of sound velocity (group velocity)"),
            
            html.H4("Parameters of the simulation"),
            html.H6("(Press Enter after changing any input to update the figures)"),
            html.Hr(),


            
            dcc.Markdown(''' **Elastic tensor:**'''),
            html.Div(['C',html.Sub('11'),'(GPa)'" = ",
              dcc.Input(id='c11tric3d', value=200.125, type='number', debounce=True, step=0.001),
                      'C',html.Sub('12'),'(GPa)'" = ",
              dcc.Input(id='c12tric3d', value=150.456, type='number', debounce=True, step=0.001),
                      'C',html.Sub('13'),'(GPa)'" = ",
              dcc.Input(id='c13tric3d', value=150.456, type='number', debounce=True, step=0.001),             
                      'C',html.Sub('14'),'(GPa)'" = ",
              dcc.Input(id='c14tric3d', value=150.456, type='number', debounce=True, step=0.001),
                      'C',html.Sub('15'),'(GPa)'" = ",
              dcc.Input(id='c15tric3d', value=150.456, type='number', debounce=True, step=0.001),
                      'C',html.Sub('16'),'(GPa)'" = ",
              dcc.Input(id='c16tric3d', value=150.456, type='number', debounce=True, step=0.001),        
              ]),
            html.Div(['C',html.Sub('22'),'(GPa)'" = ",
              dcc.Input(id='c22tric3d', value=200.125, type='number', debounce=True, step=0.001),
                      'C',html.Sub('23'),'(GPa)'" = ",
              dcc.Input(id='c23tric3d', value=150.456, type='number', debounce=True, step=0.001),
                      'C',html.Sub('24'),'(GPa)'" = ",
              dcc.Input(id='c24tric3d', value=150.456, type='number', debounce=True, step=0.001),             
                      'C',html.Sub('25'),'(GPa)'" = ",
              dcc.Input(id='c25tric3d', value=150.456, type='number', debounce=True, step=0.001),
                      'C',html.Sub('26'),'(GPa)'" = ",
              dcc.Input(id='c26tric3d', value=150.456, type='number', debounce=True, step=0.001),        
              ]),  
            html.Div(['C',html.Sub('33'),'(GPa)'" = ",
              dcc.Input(id='c33tric3d', value=150.456, type='number', debounce=True, step=0.001),
                      'C',html.Sub('34'),'(GPa)'" = ",
              dcc.Input(id='c34tric3d', value=150.456, type='number', debounce=True, step=0.001),             
                      'C',html.Sub('35'),'(GPa)'" = ",
              dcc.Input(id='c35tric3d', value=150.456, type='number', debounce=True, step=0.001),
                      'C',html.Sub('36'),'(GPa)'" = ",
              dcc.Input(id='c36tric3d', value=150.456, type='number', debounce=True, step=0.001),        
              ]), 
              
            html.Div(['C',html.Sub('44'),'(GPa)'" = ",
              dcc.Input(id='c44tric3d', value=150.456, type='number', debounce=True, step=0.001),             
                      'C',html.Sub('45'),'(GPa)'" = ",
              dcc.Input(id='c45tric3d', value=150.456, type='number', debounce=True, step=0.001),
                      'C',html.Sub('46'),'(GPa)'" = ",
              dcc.Input(id='c46tric3d', value=150.456, type='number', debounce=True, step=0.001),        
              ]),  
              
            html.Div(['C',html.Sub('55'),'(GPa)'" = ",
              dcc.Input(id='c55tric3d', value=150.456, type='number', debounce=True, step=0.001),
                      'C',html.Sub('56'),'(GPa)'" = ",
              dcc.Input(id='c56tric3d', value=150.456, type='number', debounce=True, step=0.001),        
              ]), 
              
            html.Div(['C',html.Sub('66'),'(GPa)'" = ",
              dcc.Input(id='c66tric3d', value=150.456, type='number', debounce=True, step=0.001),                    
              ]),
            dcc.Markdown(''' **Mass density:**'''),
            html.Div(['\u03C1','(kg/m',html.Sup("3"),')'" = ",
              dcc.Input(id='rhotric3d', value=10000.429, type='number', debounce=True, step=0.001)]),
            dcc.Markdown(''' **Total number of wave vector k evaluated in the plot:**'''),
            html.Div(["N = ",
              dcc.Input(id='ntric3d', value=2000, type='number', debounce=True, step=1)]),
            dcc.Markdown(''' **Choose one of the 3 solutions (qP, qS1 and qS2) to plot:**'''),
            dcc.Dropdown(
                id='soltric3d',
                options=[
                    {'label': 'qP wave', 'value': 'sol_1'},
                    {'label': 'qS1 wave', 'value': 'sol_2'},
                    {'label': 'qS2 wave', 'value': 'sol_3'},
                ],
                value='sol_1'
            ),

            html.Div(id='output_tric_3d'),
            
            
            
            html.Hr(),
            html.H4("Simulation"),

            html.Hr(),
            dcc.Markdown(''' **Generated 3D figure to visualize sound velocity (group velocity):** '''),
            html.H6("The distance between a point on the surface and the origin (0,0,0) describes the magnitude of sound velocity |v(nx,ny,nz)| evaluated at the normalized wave vector n=(sinθ*cosφ, sinθ*sinφ, cosθ), where θ and φ are the polar and azimuthal angles, respectively. The color of the surface corresponds to the magnitude of sound velocity."),
            dcc.Markdown(''' **Warning:** The generation of the figure might take from several seconds to a few minutes to finish, depending on the specified total number of wave vector **k** evaluated in the plot (N).'''),


            
            dcc.Loading(id="ls-loading-tric-3d", children=[dcc.Graph(id='tric_3D')], type="default",fullscreen=False,debug=True),
            
            

            
            
      ])




  elif mode == 'magnetic_cub': 
    
      return html.Div(children=[
            
            html.H4("Effective magnetic corrections to elastic tensor"),
            html.H6("(Press Enter after changing any input to update the calculated values)"),
            dcc.Markdown(''' **Saturation Magnetization:**'''),
            html.Div(['μ',html.Sub("0"),'Ms (Tesla)'," = ",
              dcc.Input(id='msc', value=1.001, type='number', debounce=True, step=0.0001)]),
            dcc.Markdown(''' **Magnetocrystalline anisotropy at constant stress σ (includes magnetoelastic corrections):**'''),
            html.Div(['K',html.Sub("1"),html.Sup("σ"), "(MJ/m",html.Sup("3"),")"," = ",
              dcc.Input(id='k1c', value=0.000001, type='number', debounce=True, step=0.0000001)]),
            html.Div(['K',html.Sub("2"),html.Sup("σ"), "(MJ/m",html.Sup("3"),")"," = ",
              dcc.Input(id='k2c', value=0.000001, type='number', debounce=True, step=0.0000001)]),
            dcc.Markdown(''' **Anisotropic magnetoelastic constants:**'''),
            html.Div(['b',html.Sub("1"),"(MPa)"," = ",
              dcc.Input(id='b1c', value=5.3301, type='number', debounce=True, step=0.0000001)]),
            html.Div(['b',html.Sub("2"),"(MPa)"," = ",
              dcc.Input(id='b2c', value=-8.0781, type='number', debounce=True, step=0.0000001)]),
            dcc.Markdown(''' **External magnetic field:**'''),
            html.Div(['μ',html.Sub("0"),'H',html.Sub('x'),'(Tesla)'" = ",
              dcc.Input(id='hxc', value=1.995774956, type='number', debounce=True, step=0.000000001)]),
            html.Div(['μ',html.Sub("0"),'H',html.Sub('y'),'(Tesla)'" = ",
              dcc.Input(id='hyc', value=0.865988622, type='number', debounce=True, step=0.000000001)]),
            html.Div(['μ',html.Sub("0"),'H',html.Sub('z'),'(Tesla)'" = ",
              dcc.Input(id='hzc', value=-1.310698633, type='number', debounce=True, step=0.000000001)]),
            dcc.Markdown(''' **Independent elastic constants (without effective magnetic corrections):**'''),
            html.Div(['C',html.Sub('11'),'(GPa)'" = ",
              dcc.Input(id='c11c', value=200.12577, type='number', debounce=True, step=0.00001)]),
            html.Div(['C',html.Sub('12'),'(GPa)'" = ",
              dcc.Input(id='c12c', value=150.45677, type='number', debounce=True, step=0.00001)]),
            html.Div(['C',html.Sub('44'),'(GPa)'" = ",
              dcc.Input(id='c44c', value=100.27777, type='number', debounce=True, step=0.00001)]),
            dcc.Markdown(''' **Mass density:**'''),
            html.Div(['\u03C1','(kg/m',html.Sup("3"),')'" = ",
              dcc.Input(id='rhoc', value=10000.429, type='number', debounce=True, step=0.00001)]),
            dcc.Markdown(''' **Wave vector k (phase velocity direction):**'''),
            html.Div(['k',html.Sub('x'),'(rad/m)'" = ",
              dcc.Input(id='kxc', value=1.995774956, type='number', debounce=True, step=0.000000001)]),
            html.Div(['k',html.Sub('y'),'(rad/m)'" = ",
              dcc.Input(id='kyc', value=0.865988622, type='number', debounce=True, step=0.000000001)]),
            html.Div(['k',html.Sub('z'),'(rad/m)'" = ",
              dcc.Input(id='kzc', value=-1.310698633, type='number', debounce=True, step=0.000000001)]),
            dcc.Markdown(''' **Choose one of the 3 solutions (qP, qS1 and qS2) to plot:**'''),
            dcc.Dropdown(
                id='solc',
                options=[
                    {'label': 'qP wave', 'value': 'sol_1'},
                    {'label': 'qS1 wave', 'value': 'sol_2'},
                    {'label': 'qS2 wave', 'value': 'sol_3'},
                ],
                value='sol_1'
            ),

            html.Div(id='c'),

            
            dcc.Loading(id="ls-loading-mag-cub", children=[html.Table([
                html.Tr([html.Td(['Results'])]),
                html.Tr([html.Td(['Calculated equilibrium magnetization direction:'])]),
                html.Tr([html.Td(['α', html.Sub('x'), html.Sup('0'), ' = ']), html.Td(id='axc')]),
                html.Tr([html.Td(['α', html.Sub('y'), html.Sup('0'), ' = ']), html.Td(id='ayc')]),
                html.Tr([html.Td(['α', html.Sub('z'), html.Sup('0'), ' = ']), html.Td(id='azc')]),
                html.Tr([html.Td(['Calculated effective magnetic corrections to elastic tensor:'])]),
                html.Tr([html.Td(['\u0394C', html.Sub('11'),'(GPa) = ']), html.Td(id='dc11c')]),
                html.Tr([html.Td(['\u0394C', html.Sub('12'),'(GPa) = ']), html.Td(id='dc12c')]),
                html.Tr([html.Td(['\u0394C', html.Sub('13'),'(GPa) = ']), html.Td(id='dc13c')]),
                html.Tr([html.Td(['\u0394C', html.Sub('14'),'(GPa) = ']), html.Td(id='dc14c')]),
                html.Tr([html.Td(['\u0394C', html.Sub('15'),'(GPa) = ']), html.Td(id='dc15c')]),
                html.Tr([html.Td(['\u0394C', html.Sub('16'),'(GPa) = ']), html.Td(id='dc16c')]),
                html.Tr([html.Td(['\u0394C', html.Sub('22'),'(GPa) = ']), html.Td(id='dc22c')]),
                html.Tr([html.Td(['\u0394C', html.Sub('23'),'(GPa) = ']), html.Td(id='dc23c')]),
                html.Tr([html.Td(['\u0394C', html.Sub('24'),'(GPa) = ']), html.Td(id='dc24c')]),
                html.Tr([html.Td(['\u0394C', html.Sub('25'),'(GPa) = ']), html.Td(id='dc25c')]),
                html.Tr([html.Td(['\u0394C', html.Sub('26'),'(GPa) = ']), html.Td(id='dc26c')]),
                html.Tr([html.Td(['\u0394C', html.Sub('33'),'(GPa) = ']), html.Td(id='dc33c')]),
                html.Tr([html.Td(['\u0394C', html.Sub('34'),'(GPa) = ']), html.Td(id='dc34c')]),
                html.Tr([html.Td(['\u0394C', html.Sub('35'),'(GPa) = ']), html.Td(id='dc35c')]),
                html.Tr([html.Td(['\u0394C', html.Sub('36'),'(GPa) = ']), html.Td(id='dc36c')]),
                html.Tr([html.Td(['\u0394C', html.Sub('44'),'(GPa) = ']), html.Td(id='dc44c')]),
                html.Tr([html.Td(['\u0394C', html.Sub('45'),'(GPa) = ']), html.Td(id='dc45c')]),
                html.Tr([html.Td(['\u0394C', html.Sub('46'),'(GPa) = ']), html.Td(id='dc46c')]),
                html.Tr([html.Td(['\u0394C', html.Sub('55'),'(GPa) = ']), html.Td(id='dc55c')]),
                html.Tr([html.Td(['\u0394C', html.Sub('56'),'(GPa) = ']), html.Td(id='dc56c')]),
                html.Tr([html.Td(['\u0394C', html.Sub('66'),'(GPa) = ']), html.Td(id='dc66c')]),
                html.Tr([html.Td(['Sound velocity (group velocity) including effective magnetic corrections:'])]),
                html.Tr([html.Td(['v', html.Sub('x'),'(m/s) = ']), html.Td(id='vxc')]),
                html.Tr([html.Td(['v', html.Sub('y'),'(m/s) = ']), html.Td(id='vyc')]),
                html.Tr([html.Td(['v', html.Sub('z'),'(m/s) = ']), html.Td(id='vzc')]),
                html.Tr([html.Td(['|v|','(m/s) = ']), html.Td(id='vc')]),
                html.Tr([html.Td(['Sound velocity (group velocity) without effective magnetic corrections:'])]),
                html.Tr([html.Td(['v', html.Sub('0,x'),'(m/s) = ']), html.Td(id='v0xc')]),
                html.Tr([html.Td(['v', html.Sub('0,y'),'(m/s) = ']), html.Td(id='v0yc')]),
                html.Tr([html.Td(['v', html.Sub('0,z'),'(m/s) = ']), html.Td(id='v0zc')]),
                html.Tr([html.Td(['|v',html.Sub('0'),'|','(m/s) = ']), html.Td(id='v0c')]),
                html.Tr([html.Td(['Fractional change in sound velocity (group velocity):'])]),
                html.Tr([html.Td(['(v-v',html.Sub('0'),')/v',html.Sub('0'),' = ']), html.Td(id='vv0c')]),
            ])], type="default",fullscreen=False,debug=False),
      ])
      
  elif mode == 'magnetic_hex':
    
      return html.Div(children=[
            
            html.H4("Effective magnetic corrections to elastic tensor"),
            html.H6("(Press Enter after changing any input to update the calculated values)"),
            dcc.Markdown(''' **Saturation Magnetization:**'''),
            html.Div(['μ',html.Sub("0"),'Ms (Tesla)'," = ",
              dcc.Input(id='msh', value=1.001, type='number', debounce=True, step=0.0001)]),
            dcc.Markdown(''' **Magnetocrystalline anisotropy at constant stress σ (includes magnetoelastic corrections):**'''),
            html.Div(['K',html.Sub("1"),html.Sup("σ"), "(MJ/m",html.Sup("3"),")"," = ",
              dcc.Input(id='k1h', value=0.000001, type='number', debounce=True, step=0.0000001)]),
            html.Div(['K',html.Sub("2"),html.Sup("σ"), "(MJ/m",html.Sup("3"),")"," = ",
              dcc.Input(id='k2h', value=0.000001, type='number', debounce=True, step=0.0000001)]),
            dcc.Markdown(''' **Anisotropic magnetoelastic constants:**'''),
            html.Div(['b',html.Sub("21"),"(MPa)"," = ",
              dcc.Input(id='b21', value=5.3301, type='number', debounce=True, step=0.0000001)]),
            html.Div(['b',html.Sub("22"),"(MPa)"," = ",
              dcc.Input(id='b22', value=-8.0781, type='number', debounce=True, step=0.0000001)]),
            html.Div(['b',html.Sub("3"),"(MPa)"," = ",
              dcc.Input(id='b3', value=2.2201, type='number', debounce=True, step=0.0000001)]),
            html.Div(['b',html.Sub("4"),"(MPa)"," = ",
              dcc.Input(id='b4', value=-1.7771, type='number', debounce=True, step=0.0000001)]),
            dcc.Markdown(''' **External magnetic field:**'''),
            html.Div(['μ',html.Sub("0"),'H',html.Sub('x'),'(Tesla)'" = ",
              dcc.Input(id='hxh', value=1.995774956, type='number', debounce=True, step=0.000000001)]),
            html.Div(['μ',html.Sub("0"),'H',html.Sub('y'),'(Tesla)'" = ",
              dcc.Input(id='hyh', value=0.865988622, type='number', debounce=True, step=0.000000001)]),
            html.Div(['μ',html.Sub("0"),'H',html.Sub('z'),'(Tesla)'" = ",
              dcc.Input(id='hzh', value=-1.310698633, type='number', debounce=True, step=0.000000001)]),
            dcc.Markdown(''' **Independent elastic constants (without effective magnetic corrections):**'''),
            html.Div(['C',html.Sub('11'),'(GPa)'" = ",
              dcc.Input(id='c11h', value=200.12577, type='number', debounce=True, step=0.00001)]),
            html.Div(['C',html.Sub('12'),'(GPa)'" = ",
              dcc.Input(id='c12h', value=150.45677, type='number', debounce=True, step=0.00001)]),
            html.Div(['C',html.Sub('13'),'(GPa)'" = ",
              dcc.Input(id='c13h', value=150.45677, type='number', debounce=True, step=0.00001)]),
            html.Div(['C',html.Sub('33'),'(GPa)'" = ",
              dcc.Input(id='c33h', value=100.27777, type='number', debounce=True, step=0.00001)]),
            html.Div(['C',html.Sub('44'),'(GPa)'" = ",
              dcc.Input(id='c44h', value=100.27777, type='number', debounce=True, step=0.00001)]),
            dcc.Markdown(''' **Mass density:**'''),
            html.Div(['\u03C1','(kg/m',html.Sup("3"),')'" = ",
              dcc.Input(id='rhoh', value=10000.429, type='number', debounce=True, step=0.00001)]),
            dcc.Markdown(''' **Wave vector k (phase velocity direction):**'''),
            html.Div(['k',html.Sub('x'),'(rad/m)'" = ",
              dcc.Input(id='kxh', value=1.995774956, type='number', debounce=True, step=0.000000001)]),
            html.Div(['k',html.Sub('y'),'(rad/m)'" = ",
              dcc.Input(id='kyh', value=0.865988622, type='number', debounce=True, step=0.000000001)]),
            html.Div(['k',html.Sub('z'),'(rad/m)'" = ",
              dcc.Input(id='kzh', value=-1.310698633, type='number', debounce=True, step=0.000000001)]),
            dcc.Markdown(''' **Choose one of the 3 solutions (qP, qS1 and qS2) to plot:**'''),
            dcc.Dropdown(
                id='solh',
                options=[
                    {'label': 'qP wave', 'value': 'sol_1'},
                    {'label': 'qS1 wave', 'value': 'sol_2'},
                    {'label': 'qS2 wave', 'value': 'sol_3'},
                ],
                value='sol_1'
            ),

            html.Div(id='h'),

            
            dcc.Loading(id="ls-loading-mag-hex", children=[html.Table([
                html.Tr([html.Td(['Results'])]),
                html.Tr([html.Td(['Calculated equilibrium magnetization direction:'])]),
                html.Tr([html.Td(['α', html.Sub('x'), html.Sup('0'), ' = ']), html.Td(id='axh')]),
                html.Tr([html.Td(['α', html.Sub('y'), html.Sup('0'), ' = ']), html.Td(id='ayh')]),
                html.Tr([html.Td(['α', html.Sub('z'), html.Sup('0'), ' = ']), html.Td(id='azh')]),
                html.Tr([html.Td(['Calculated effective magnetic corrections to elastic tensor:'])]),
                html.Tr([html.Td(['\u0394C', html.Sub('11'),'(GPa) = ']), html.Td(id='dc11h')]),
                html.Tr([html.Td(['\u0394C', html.Sub('12'),'(GPa) = ']), html.Td(id='dc12h')]),
                html.Tr([html.Td(['\u0394C', html.Sub('13'),'(GPa) = ']), html.Td(id='dc13h')]),
                html.Tr([html.Td(['\u0394C', html.Sub('14'),'(GPa) = ']), html.Td(id='dc14h')]),
                html.Tr([html.Td(['\u0394C', html.Sub('15'),'(GPa) = ']), html.Td(id='dc15h')]),
                html.Tr([html.Td(['\u0394C', html.Sub('16'),'(GPa) = ']), html.Td(id='dc16h')]),
                html.Tr([html.Td(['\u0394C', html.Sub('22'),'(GPa) = ']), html.Td(id='dc22h')]),
                html.Tr([html.Td(['\u0394C', html.Sub('23'),'(GPa) = ']), html.Td(id='dc23h')]),
                html.Tr([html.Td(['\u0394C', html.Sub('24'),'(GPa) = ']), html.Td(id='dc24h')]),
                html.Tr([html.Td(['\u0394C', html.Sub('25'),'(GPa) = ']), html.Td(id='dc25h')]),
                html.Tr([html.Td(['\u0394C', html.Sub('26'),'(GPa) = ']), html.Td(id='dc26h')]),
                html.Tr([html.Td(['\u0394C', html.Sub('33'),'(GPa) = ']), html.Td(id='dc33h')]),
                html.Tr([html.Td(['\u0394C', html.Sub('34'),'(GPa) = ']), html.Td(id='dc34h')]),
                html.Tr([html.Td(['\u0394C', html.Sub('35'),'(GPa) = ']), html.Td(id='dc35h')]),
                html.Tr([html.Td(['\u0394C', html.Sub('36'),'(GPa) = ']), html.Td(id='dc36h')]),
                html.Tr([html.Td(['\u0394C', html.Sub('44'),'(GPa) = ']), html.Td(id='dc44h')]),
                html.Tr([html.Td(['\u0394C', html.Sub('45'),'(GPa) = ']), html.Td(id='dc45h')]),
                html.Tr([html.Td(['\u0394C', html.Sub('46'),'(GPa) = ']), html.Td(id='dc46h')]),
                html.Tr([html.Td(['\u0394C', html.Sub('55'),'(GPa) = ']), html.Td(id='dc55h')]),
                html.Tr([html.Td(['\u0394C', html.Sub('56'),'(GPa) = ']), html.Td(id='dc56h')]),
                html.Tr([html.Td(['\u0394C', html.Sub('66'),'(GPa) = ']), html.Td(id='dc66h')]),
                html.Tr([html.Td(['Sound velocity (group velocity) including effective magnetic corrections:'])]),
                html.Tr([html.Td(['v', html.Sub('x'),'(m/s) = ']), html.Td(id='vxh')]),
                html.Tr([html.Td(['v', html.Sub('y'),'(m/s) = ']), html.Td(id='vyh')]),
                html.Tr([html.Td(['v', html.Sub('z'),'(m/s) = ']), html.Td(id='vzh')]),
                html.Tr([html.Td(['|v|','(m/s) = ']), html.Td(id='vh')]),
                html.Tr([html.Td(['Sound velocity (group velocity) without effective magnetic corrections:'])]),
                html.Tr([html.Td(['v', html.Sub('0,x'),'(m/s) = ']), html.Td(id='v0xh')]),
                html.Tr([html.Td(['v', html.Sub('0,y'),'(m/s) = ']), html.Td(id='v0yh')]),
                html.Tr([html.Td(['v', html.Sub('0,z'),'(m/s) = ']), html.Td(id='v0zh')]),
                html.Tr([html.Td(['|v',html.Sub('0'),'|','(m/s) = ']), html.Td(id='v0h')]),
                html.Tr([html.Td(['Fractional change in sound velocity:'])]),
                html.Tr([html.Td(['(v-v',html.Sub('0'),')/v',html.Sub('0'),' = ']), html.Td(id='vv0h')]),
            ])], type="default",fullscreen=False,debug=False),
      ])


  elif mode == 'magnetic_cub_field': 
    
      return html.Div(children=[
            
            html.H4("Fractional change in sound velocity (group velocity) due to magnetic field (Cubic I)"),
            html.H6("(Press Enter after changing any input to update the calculated values)"),
            dcc.Markdown(''' **Saturation Magnetization:**'''),
            html.Div(['μ',html.Sub("0"),'Ms (Tesla)'," = ",
              dcc.Input(id='mscf', value=1.001, type='number', debounce=True, step=0.0001)]),
            dcc.Markdown(''' **Magnetocrystalline anisotropy at constant stress σ (includes magnetoelastic corrections):**'''),
            html.Div(['K',html.Sub("1"),html.Sup("σ"), "(MJ/m",html.Sup("3"),")"," = ",
              dcc.Input(id='k1cf', value=0.000001, type='number', debounce=True, step=0.0000001)]),
            html.Div(['K',html.Sub("2"),html.Sup("σ"), "(MJ/m",html.Sup("3"),")"," = ",
              dcc.Input(id='k2cf', value=0.000001, type='number', debounce=True, step=0.0000001)]),
            dcc.Markdown(''' **Anisotropic magnetoelastic constants:**'''),
            html.Div(['b',html.Sub("1"),"(MPa)"," = ",
              dcc.Input(id='b1cf', value=5.3301, type='number', debounce=True, step=0.0000001)]),
            html.Div(['b',html.Sub("2"),"(MPa)"," = ",
              dcc.Input(id='b2cf', value=-8.0781, type='number', debounce=True, step=0.0000001)]),
            dcc.Markdown(''' **External magnetic field:**'''),
            html.Div(['μ',html.Sub("0"),'H',html.Sub('x'),'(Tesla)'" = ",
              dcc.Input(id='hxcf', value=1.995774956, type='number', debounce=True, step=0.000000001)]),
            html.Div(['μ',html.Sub("0"),'H',html.Sub('y'),'(Tesla)'" = ",
              dcc.Input(id='hycf', value=0.865988622, type='number', debounce=True, step=0.000000001)]),
            html.Div(['μ',html.Sub("0"),'H',html.Sub('z'),'(Tesla)'" = ",
              dcc.Input(id='hzcf', value=-1.310698633, type='number', debounce=True, step=0.000000001)]),
            dcc.Markdown(''' **Independent elastic constants (without effective magnetic corrections):**'''),
            html.Div(['C',html.Sub('11'),'(GPa)'" = ",
              dcc.Input(id='c11cf', value=200.12577, type='number', debounce=True, step=0.00001)]),
            html.Div(['C',html.Sub('12'),'(GPa)'" = ",
              dcc.Input(id='c12cf', value=150.45677, type='number', debounce=True, step=0.00001)]),
            html.Div(['C',html.Sub('44'),'(GPa)'" = ",
              dcc.Input(id='c44cf', value=100.27777, type='number', debounce=True, step=0.00001)]),
            dcc.Markdown(''' **Mass density:**'''),
            html.Div(['\u03C1','(kg/m',html.Sup("3"),')'" = ",
              dcc.Input(id='rhocf', value=10000.429, type='number', debounce=True, step=0.00001)]),
              dcc.Markdown(''' **Total number of wave vector k evaluated in the plot:**'''),
            html.Div(["N = ",
              dcc.Input(id='ncf', value=2000, type='number', debounce=True, step=1)]),
              dcc.Markdown(''' **Scale factor:**'''),
            html.Div(["Scale factor = ",
              dcc.Input(id='scalecf', value=1.0, type='number', debounce=True)]),
            dcc.Markdown(''' **Choose one of the 3 solutions (qP, qS1 and qS2) to plot:**'''),
            dcc.Dropdown(
                id='solcf',
                options=[
                    {'label': 'qP wave', 'value': 'sol_1'},
                    {'label': 'qS1 wave', 'value': 'sol_2'},
                    {'label': 'qS2 wave', 'value': 'sol_3'},
                ],
                value='sol_1'
            ),

            html.Div(id='cf'),
            
            
            
            html.Hr(),
            html.H4("Simulation"),

            html.Hr(),
            dcc.Markdown(''' **Generated 3D figure to visualize sound velocity (group velocity):** '''),
            html.H6("The distance between a point on the surface and the origin (0,0,0) describes the magnitude the fractional change in sound velocity substracted to the unit sphere: 1-s*((v(nx,ny,nz)-v0(nx,ny,nz))/v0(nx,ny,nz)), where v and v0 are sound velocity with and without effective magnetic corrections respectively and s is the scale factor, evaluated at the normalized wave vector n=(sinθ*cosφ, sinθ*sinφ, cosθ), where θ and φ are the polar and azimuthal angles, respectively. The color of the surface corresponds to the magnitude of the fractional change in sound velocity (v(nx,ny,nz)-v0(nx,ny,nz))/v0(nx,ny,nz)."),
            dcc.Markdown(''' **Warning:** The generation of the figure might take from several seconds to a few minutes to finish, depending on the specified total number of wave vector **k** evaluated in the plot (N).'''),


            
            dcc.Loading(id="ls-loading-cub-3df", children=[dcc.Graph(id='output_cf')], type="default",fullscreen=False,debug=True),
            
            
      ])



  elif mode == 'magnetic_hex_field': 
    
      return html.Div(children=[
            
            html.H4("Fractional change in sound velocity (group velocity) due to magnetic field (Hexagonal I)"),
            html.H6("(Press Enter after changing any input to update the calculated values)"),
            dcc.Markdown(''' **Saturation Magnetization:**'''),
            html.Div(['μ',html.Sub("0"),'Ms (Tesla)'," = ",
              dcc.Input(id='mshf', value=1.001, type='number', debounce=True, step=0.0001)]),
            dcc.Markdown(''' **Magnetocrystalline anisotropy at constant stress σ (includes magnetoelastic corrections):**'''),
            html.Div(['K',html.Sub("1"),html.Sup("σ"), "(MJ/m",html.Sup("3"),")"," = ",
              dcc.Input(id='k1hf', value=0.000001, type='number', debounce=True, step=0.0000001)]),
            html.Div(['K',html.Sub("2"),html.Sup("σ"), "(MJ/m",html.Sup("3"),")"," = ",
              dcc.Input(id='k2hf', value=0.000001, type='number', debounce=True, step=0.0000001)]),
            dcc.Markdown(''' **Anisotropic magnetoelastic constants:**'''),
            html.Div(['b',html.Sub("21"),"(MPa)"," = ",
              dcc.Input(id='b21hf', value=5.3301, type='number', debounce=True, step=0.0000001)]),
            html.Div(['b',html.Sub("22"),"(MPa)"," = ",
              dcc.Input(id='b22hf', value=-8.0781, type='number', debounce=True, step=0.0000001)]),
            html.Div(['b',html.Sub("3"),"(MPa)"," = ",
              dcc.Input(id='b3hf', value=5.3301, type='number', debounce=True, step=0.0000001)]),
            html.Div(['b',html.Sub("4"),"(MPa)"," = ",
              dcc.Input(id='b4hf', value=-8.0781, type='number', debounce=True, step=0.0000001)]),
            dcc.Markdown(''' **External magnetic field:**'''),
            html.Div(['μ',html.Sub("0"),'H',html.Sub('x'),'(Tesla)'" = ",
              dcc.Input(id='hxhf', value=1.995774956, type='number', debounce=True, step=0.000000001)]),
            html.Div(['μ',html.Sub("0"),'H',html.Sub('y'),'(Tesla)'" = ",
              dcc.Input(id='hyhf', value=0.865988622, type='number', debounce=True, step=0.000000001)]),
            html.Div(['μ',html.Sub("0"),'H',html.Sub('z'),'(Tesla)'" = ",
              dcc.Input(id='hzhf', value=-1.310698633, type='number', debounce=True, step=0.000000001)]),
            dcc.Markdown(''' **Independent elastic constants (without effective magnetic corrections):**'''),
            html.Div(['C',html.Sub('11'),'(GPa)'" = ",
              dcc.Input(id='c11hf', value=200.12577, type='number', debounce=True, step=0.00001)]),
            html.Div(['C',html.Sub('12'),'(GPa)'" = ",
              dcc.Input(id='c12hf', value=150.45677, type='number', debounce=True, step=0.00001)]),
            html.Div(['C',html.Sub('13'),'(GPa)'" = ",
              dcc.Input(id='c13hf', value=150.45677, type='number', debounce=True, step=0.00001)]),
            html.Div(['C',html.Sub('33'),'(GPa)'" = ",
              dcc.Input(id='c33hf', value=150.45677, type='number', debounce=True, step=0.00001)]),
            html.Div(['C',html.Sub('44'),'(GPa)'" = ",
              dcc.Input(id='c44hf', value=100.27777, type='number', debounce=True, step=0.00001)]),
            dcc.Markdown(''' **Mass density:**'''),
            html.Div(['\u03C1','(Kg/m',html.Sup("3"),')'" = ",
              dcc.Input(id='rhohf', value=10000.429, type='number', debounce=True, step=0.001)]),
              dcc.Markdown(''' **Total number of wave vector k evaluated in the plot:**'''),
            html.Div(["N = ",
              dcc.Input(id='nhf', value=2000, type='number', debounce=True, step=1)]),
              dcc.Markdown(''' **Scale factor:**'''),
            html.Div(["Scale factor = ",
              dcc.Input(id='scalehf', value=1.0, type='number', debounce=True)]),
            dcc.Markdown(''' **Choose one of the 3 solutions (qP, qS1 and qS2) to plot:**'''),
            dcc.Dropdown(
                id='solhf',
                options=[
                    {'label': 'qP wave', 'value': 'sol_1'},
                    {'label': 'qS1 wave', 'value': 'sol_2'},
                    {'label': 'qS2 wave', 'value': 'sol_3'},
                ],
                value='sol_1'
            ),

            html.Div(id='hf'),
            
            
            
            html.Hr(),
            html.H4("Simulation"),

            html.Hr(),
            dcc.Markdown(''' **Generated 3D figure to visualize sound velocity (group velocity):** '''),
            html.H6("The distance between a point on the surface and the origin (0,0,0) describes the magnitude the fractional change in sound velocity substracted to the unit sphere: 1-s*((v(nx,ny,nz)-v0(nx,ny,nz))/v0(nx,ny,nz)), where v and v0 are sound velocity with and without effective magnetic corrections respectively and s is the scale factor, evaluated at the normalized wave vector n=(sinθ*cosφ, sinθ*sinφ, cosθ), where θ and φ are the polar and azimuthal angles, respectively. The color of the surface corresponds to the magnitude of the fractional change in sound velocity (v(nx,ny,nz)-v0(nx,ny,nz))/v0(nx,ny,nz)."),
            dcc.Markdown(''' **Warning:** The generation of the figure might take from several seconds to a few minutes to finish, depending on the specified total number of wave vector **k** evaluated in the plot (N).'''),


            
            dcc.Loading(id="ls-loading-hex-3df", children=[dcc.Graph(id='output_hf')], type="default",fullscreen=False,debug=True),
            
            
      ])            




##############Magnetic correction Cubic 

@app.callback(
    [Output('dc11c', 'children'),
     Output('dc12c', 'children'),
     Output('dc13c', 'children'),
     Output('dc14c', 'children'),
     Output('dc15c', 'children'),
     Output('dc16c', 'children'),
     Output('dc22c', 'children'),
     Output('dc23c', 'children'),
     Output('dc24c', 'children'),
     Output('dc25c', 'children'),
     Output('dc26c', 'children'),
     Output('dc33c', 'children'),
     Output('dc34c', 'children'),
     Output('dc35c', 'children'),
     Output('dc36c', 'children'),
     Output('dc44c', 'children'),
     Output('dc45c', 'children'),
     Output('dc46c', 'children'),
     Output('dc55c', 'children'),
     Output('dc56c', 'children'),
     Output('dc66c', 'children'),
     Output('axc', 'children'),
     Output('ayc', 'children'),
     Output('azc', 'children'),
     Output('vxc', 'children'),
     Output('vyc', 'children'),
     Output('vzc', 'children'),
     Output('vc', 'children'),
     Output('v0xc', 'children'),
     Output('v0yc', 'children'),
     Output('v0zc', 'children'),
     Output('v0c', 'children'),
     Output('vv0c', 'children'),
    ],
    [Input(component_id='msc', component_property='value'),
     Input(component_id='k1c', component_property='value'),
     Input(component_id='k2c', component_property='value'),
     Input(component_id='b1c', component_property='value'),
     Input(component_id='b2c', component_property='value'),
     Input(component_id='hxc', component_property='value'),
     Input(component_id='hyc', component_property='value'),
     Input(component_id='hzc', component_property='value'),
     Input(component_id='c11c', component_property='value'),
     Input(component_id='c12c', component_property='value'),
     Input(component_id='c44c', component_property='value'),
     Input(component_id='kxc', component_property='value'),
     Input(component_id='kyc', component_property='value'),
     Input(component_id='kzc', component_property='value'),
     Input(component_id='rhoc', component_property='value'),
     Input(component_id='solc', component_property='value'),
    ],

)


def update_magnetic(ms,kk1,kk2,bb1,bb2,hx,hy,hz,cc11,cc12,cc44,kx,ky,kz,rho,sol):

    delta=0.0*10.0**(-5)
    mu0 = 4.0*np.pi*10.0**(-7)
    ms = ms/mu0
    k1 = kk1*10.0**6  #J/m^3
    k2 = kk2*10.0**6  #J/m^3
    b1 = bb1*10.0**6  # Pa
    b2 = bb2*10.0**6  # Pa
  #  dk1 = ((b1**2)/(c11 - c12)) - ((b2**2)/(2.0*c44))
  #  k1eff = (k1 + dk1)
    
    hx=hx+delta
    hy=hy+delta
    hz=hz+delta
    
    a = [hx,hy,hz,ms,k1,k2]  
  
    x0 = minimize(enecub,np.array([0.2,0.3]),args=(a),method='Nelder-Mead',options={'maxiter': 1000, 'maxfev': 1000, 'disp': True, 'xatol': 0.0000001})

    xx=float(x0.x[0])
    yy=float(x0.x[1])
    
    ett0=ett(xx,yy,hx,hy,hz,ms,k1,k2)
    epp0=epp(xx,yy,hx,hy,hz,ms,k1,k2)
    
    chizz= (ms**2*np.sin(xx)**2)/ett0
    chiyz= -(ms**2*np.sin(xx)*np.cos(xx)*np.sin(yy))/(ett0)
    chixz= -(ms**2*np.sin(xx)*np.cos(xx)*np.cos(yy))/(ett0)
    chiyy= ms**2*(((np.cos(xx)**2*np.sin(yy)**2)/ett0) + ((np.sin(xx)**2*np.cos(yy)**2)/epp0))
    chixx= ms**2*(((np.cos(xx)**2*np.cos(yy)**2)/ett0) + ((np.sin(xx)**2*np.sin(yy)**2)/epp0))
    chixy= -ms**2*(((np.cos(xx)**2*np.cos(yy)*np.sin(yy))/ett0) - ((np.sin(xx)**2*np.cos(yy)*np.sin(yy))/epp0))
    
    
    ax= np.sin(xx)*np.cos(yy)
    ay= np.sin(xx)*np.sin(yy)
    az= np.cos(xx)
    
    dc11= -(b1/ms)**2*(4.0*chixx*ax**2)*10.0**(-9)  #GPa
    dc12= -(b1/ms)**2*(4.0*chixy*ax*ay)*10.0**(-9)
    dc22= -(b1/ms)**2*(4.0*chiyy*ay**2)*10.0**(-9)
    dc33= -(b1/ms)**2*(4.0*chizz*az**2)*10.0**(-9)
    dc44= -(b2/ms)**2*(chizz*ay**2 + 2.0*chiyz*ay*az + chiyy*az**2)*10.0**(-9)
    dc55= -(b2/ms)**2*(chixx*az**2 + chizz*ax**2 + 2.0*chixz*ax*az)*10.0**(-9)
    dc66= -(b2/ms)**2*(chixx*ay**2 + chiyy*ax**2 + 2.0*chixy*ax*ay)*10.0**(-9)
    dc13= -(b1/ms)**2*(4.0*chixz*ax*az)*10.0**(-9)
    dc23= -(b1/ms)**2*(4.0*chiyz*ay*az)*10.0**(-9)
    dc14= -((2.0*b1*b2)/(ms**2))*(chixy*ax*az + chixz*ax*ay)*10.0**(-9)
    dc15= -((2.0*b1*b2)/(ms**2))*(chixx*ax*az + chixz*ax*ax)*10.0**(-9)
    dc16= -((2.0*b1*b2)/(ms**2))*(chixx*ax*ay + chixy*ax*ax)*10.0**(-9)
    dc24= -((2.0*b1*b2)/(ms**2))*(chiyy*ay*az + chiyz*ay*ay)*10.0**(-9)
    dc25= -((2.0*b1*b2)/(ms**2))*(chixy*ay*az + chiyz*ax*ay)*10.0**(-9)
    dc26= -((2.0*b1*b2)/(ms**2))*(chixy*ay*ay + chiyy*ax*ay)*10.0**(-9)
    dc34= -((2.0*b1*b2)/(ms**2))*(chiyz*az*az + chizz*az*ay)*10.0**(-9)
    dc35= -((2.0*b1*b2)/(ms**2))*(chixz*az*az + chizz*ax*az)*10.0**(-9)
    dc36= -((2.0*b1*b2)/(ms**2))*(chixz*ay*az + chiyz*ax*az)*10.0**(-9)
    dc45= -(b2/ms)**2*(chixy*az**2 + chixz*ay*az + chiyz*ax*az + chizz*ax*ay)*10.0**(-9)
    dc46= -(b2/ms)**2*(chixy*ay*az + chixz*ay*ay + chiyy*ax*az + chiyz*ax*ay)*10.0**(-9)
    dc56= -(b2/ms)**2*(chixx*ay*az + chixy*ax*az + chixz*ax*ay + chiyz*ax*ax)*10.0**(-9)
    
    a11=(cc11*10**9/rho)+(dc11*10**9/rho)
    a12=(cc12*10**9/rho)+(dc12*10**9/rho)
    a13=(cc12*10**9/rho)+(dc13*10**9/rho)
    a14=(0.0*10**9/rho)+(dc14*10**9/rho)
    a15=(0.0*10**9/rho)+(dc15*10**9/rho)
    a16=(0.0*10**9/rho)+(dc16*10**9/rho)
    a22=(cc11*10**9/rho)+(dc22*10**9/rho)
    a23=(cc12*10**9/rho)+(dc23*10**9/rho)
    a24=(0.0*10**9/rho)+(dc24*10**9/rho)
    a25=(0.0*10**9/rho)+(dc25*10**9/rho)
    a26=(0.0*10**9/rho)+(dc26*10**9/rho)
    a33=(cc11*10**9/rho)+(dc33*10**9/rho)
    a34=(0.0*10**9/rho)+(dc34*10**9/rho)
    a35=(0.0*10**9/rho)+(dc35*10**9/rho)
    a36=(0.0*10**9/rho)+(dc36*10**9/rho)
    a44=(cc44*10**9/rho)+(dc44*10**9/rho)
    a45=(0.0*10**9/rho)+(dc45*10**9/rho)
    a46=(0.0*10**9/rho)+(dc46*10**9/rho)
    a55=(cc44*10**9/rho)+(dc55*10**9/rho)
    a56=(0.0*10**9/rho)+(dc56*10**9/rho)
    a66=(cc44*10**9/rho)+(dc66*10**9/rho)
    
    a011=cc11*10**9/rho
    a012=cc12*10**9/rho
    a013=cc12*10**9/rho
    a014=0.0*10**9/rho
    a015=0.0*10**9/rho
    a016=0.0*10**9/rho
    a022=cc11*10**9/rho
    a023=cc12*10**9/rho
    a024=0.0*10**9/rho
    a025=0.0*10**9/rho
    a026=0.0*10**9/rho
    a033=cc11*10**9/rho
    a034=0.0*10**9/rho
    a035=0.0*10**9/rho
    a036=0.0*10**9/rho
    a044=cc44*10**9/rho
    a045=0.0*10**9/rho
    a046=0.0*10**9/rho
    a055=cc44*10**9/rho
    a056=0.0*10**9/rho
    a066=cc44*10**9/rho
    
    kk=np.sqrt(kx**2+ky**2+kz*2)
    kkx=kx/kk
    kky=ky/kk
    kkz=kz/kk
    
    
    vvx,vvy,vvz = vel(a11,a12,a13,a14,a15,a16,a22,a23,a24,a25,a26,a33,a34,a35,a36,a44,a45,a46,a55,a56,a66,kkx,kky,kkz,sol)
        
    vvvx,vvvy,vvvz = vel(a011,a012,a013,a014,a015,a016,a022,a023,a024,a025,a026,a033,a034,a035,a036,a044,a045,a046,a055,a056,a066,kkx,kky,kkz,sol)
    
    vx0=vvx
    vy0=vvy
    vz0=vvz
    v0=np.sqrt(vx0**2+vy0**2+vz0**2)
        
    vx00=vvvx
    vy00=vvvy
    vz00=vvvz
    v00=np.sqrt(vx00**2+vy00**2+vz00**2)
        
    v000=(v0-v00)/v00

  
    return dc11,dc12,dc13,dc14,dc15,dc16,dc22,dc23,dc24,dc25,dc26,dc33,dc34,dc35,dc36,dc44,dc45,dc46,dc55,dc56,dc66,ax,ay,az,vx0,vy0,vz0,v0,vx00,vy00,vz00,v00,v000

def enecub(x,a):

  hx0=a[0]
  hy0=a[1]
  hz0=a[2]
  Ms0=a[3]
  k1eff0=a[4]
  k2eff0=a[5]
  theta=x[0]
  phi=x[1]
  
  return k1eff0*(((np.sin(theta)*np.cos(phi))**2)*(np.sin(theta)*np.sin(phi))**2 + ((np.sin(theta)*np.cos(phi))**2)*np.cos(theta)**2 + (np.sin(theta)*np.sin(phi))**2*np.cos(theta)**2) + k2eff0*((np.sin(theta)*np.cos(phi))**2)*(np.sin(theta)*np.sin(phi))**2*np.cos(theta)**2 - Ms0*(np.sin(theta)*np.cos(phi)*hx0 + np.sin(theta)*np.sin(phi)*hy0 + np.cos(theta)*hz0)



def ett(x,y,hhx,hhy,hhz,ms,kk1eff,kk2eff):
  
  ff0 = -0.5*ms*(-hhz*np.cos(x) - hhx*np.cos(y)*np.sin(x) - hhy*np.sin(x)*np.sin(y))
  ff1 = kk1eff*(2.0*np.cos(x)**4*np.cos(y)**2 - 12.0*np.cos(x)**2*np.cos(y)**2*np.sin(x)**2 + 2.0*np.cos(y)**2*np.sin(x)**4 + 2.0*np.cos(x)**4*np.sin(y)**2 - 12.0*np.cos(x)**2*np.sin(x)**2*np.sin(y)**2 + 12.0*np.cos(x)**2*np.cos(y)**2*np.sin(x)**2*np.sin(y)**2 + 2.0*np.sin(x)**4*np.sin(y)**2 - 4.0*np.cos(y)**2*np.sin(x)**4*np.sin(y)**2)
  ff2 = kk2eff*(12.0*np.cos(x)**4*np.cos(y)**2*np.sin(x)**2*np.sin(y)**2 - 22.0*np.cos(x)**2*np.cos(y)**2*np.sin(x)**4*np.sin(y)**2 + 2.0*np.cos(y)**2*np.sin(x)**6*np.sin(y)**2)
     

  
  ff=ff0+ff1+ff2 
     
  return ff
     
  
def epp(x,y,hhx,hhy,hhz,ms,kk1eff,kk2eff):
  ff0 = -0.5*ms*(-hhx*np.cos(y)*np.sin(x) - hhy*np.sin(x)*np.sin(y)) 
  
  ff1=kk1eff*(2.0*np.cos(y)**4*np.sin(x)**4 - 12.0*np.cos(y)**2*np.sin(x)**4*np.sin(y)**2 + 2.0*np.sin(x)**4*np.sin(y)**4)
  
  ff2=kk2eff*(2.0*np.cos(x)**2*np.cos(y)**4*np.sin(x)**4 - 12.0*np.cos(x)**2*np.cos(y)**2*np.sin(x)**4*np.sin(y)**2 + 2.0*np.cos(x)**2*np.sin(x)**4*np.sin(y)**4)

  ff=ff0+ff1+ff2  
     
  return ff




##############Magnetic correction hex 

@app.callback(
    [Output('dc11h', 'children'),
     Output('dc12h', 'children'),
     Output('dc13h', 'children'),
     Output('dc14h', 'children'),
     Output('dc15h', 'children'),
     Output('dc16h', 'children'),
     Output('dc22h', 'children'),
     Output('dc23h', 'children'),
     Output('dc24h', 'children'),
     Output('dc25h', 'children'),
     Output('dc26h', 'children'),
     Output('dc33h', 'children'),
     Output('dc34h', 'children'),
     Output('dc35h', 'children'),
     Output('dc36h', 'children'),
     Output('dc44h', 'children'),
     Output('dc45h', 'children'),
     Output('dc46h', 'children'),
     Output('dc55h', 'children'),
     Output('dc56h', 'children'),
     Output('dc66h', 'children'),
     Output('axh', 'children'),
     Output('ayh', 'children'),
     Output('azh', 'children'),
     Output('vxh', 'children'),
     Output('vyh', 'children'),
     Output('vzh', 'children'),
     Output('vh', 'children'),
     Output('v0xh', 'children'),
     Output('v0yh', 'children'),
     Output('v0zh', 'children'),
     Output('v0h', 'children'),
     Output('vv0h', 'children'),
    ],
    [Input(component_id='msh', component_property='value'),
     Input(component_id='k1h', component_property='value'),
     Input(component_id='k2h', component_property='value'),
     Input(component_id='b21', component_property='value'),
     Input(component_id='b22', component_property='value'),
     Input(component_id='b3', component_property='value'),
     Input(component_id='b4', component_property='value'),
     Input(component_id='hxh', component_property='value'),
     Input(component_id='hyh', component_property='value'),
     Input(component_id='hzh', component_property='value'),
     Input(component_id='c11h', component_property='value'),
     Input(component_id='c12h', component_property='value'),
     Input(component_id='c13h', component_property='value'),
     Input(component_id='c33h', component_property='value'),
     Input(component_id='c44h', component_property='value'),
     Input(component_id='kxh', component_property='value'),
     Input(component_id='kyh', component_property='value'),
     Input(component_id='kzh', component_property='value'),
     Input(component_id='rhoh', component_property='value'),
     Input(component_id='solh', component_property='value'),
    ],

)


def update_magnetic_hex(ms,kk1,kk2,bb21,bb22,bb3,bb4,hx,hy,hz,cc11,cc12,cc13,cc33,cc44,kx,ky,kz,rho,sol):

    delta=0.0*10.0**(-5)
    mu0 = 4.0*np.pi*10.0**(-7)
    ms = ms/mu0
    k1 = kk1*10.0**6  #J/m^3
    k2 = kk2*10.0**6  #J/m^3
    b21 = bb21*10.0**6  # Pa
    b22 = bb22*10.0**6  # Pa
    b3 = bb3*10.0**6  # Pa
    b4 = bb4*10.0**6  # Pa
    
    hx=hx+delta
    hy=hy+delta
    hz=hz+delta
    
    a = [hx,hy,hz,ms,k1,k2]  
  
    x0 = minimize(enehex,np.array([0.2,0.3]),args=(a),method='Nelder-Mead',options={'maxiter': 1000, 'maxfev': 1000, 'disp': True, 'xatol': 0.0000001})

    xx=float(x0.x[0])
    yy=float(x0.x[1])
    
    ett0=etth(xx,yy,hx,hy,hz,ms,k1,k2)
    epp0=epph(xx,yy,hx,hy,hz,ms,k1,k2)
    
    chizz= (ms**2*np.sin(xx)**2)/ett0
    chiyz= -(ms**2*np.sin(xx)*np.cos(xx)*np.sin(yy))/(ett0)
    chixz= -(ms**2*np.sin(xx)*np.cos(xx)*np.cos(yy))/(ett0)
    chiyy= ms**2*(((np.cos(xx)**2*np.sin(yy)**2)/ett0) + ((np.sin(xx)**2*np.cos(yy)**2)/epp0))
    chixx= ms**2*(((np.cos(xx)**2*np.cos(yy)**2)/ett0) + ((np.sin(xx)**2*np.sin(yy)**2)/epp0))
    chixy= -ms**2*(((np.cos(xx)**2*np.cos(yy)*np.sin(yy))/ett0) - ((np.sin(xx)**2*np.cos(yy)*np.sin(yy))/epp0))
    
    
    ax= np.sin(xx)*np.cos(yy)
    ay= np.sin(xx)*np.sin(yy)
    az= np.cos(xx)
    
    dc11= (1.0/ms)**2*(-b3**2*(chixx*ax**2+chiyy*ay**2-chixy*ax*ay)+2.0*b21*b3*az*(chiyz*ay-chixz*ax)-chizz*4.0*b21**2*az**2)*10.0**(-9)  #GPa
    dc22= (1.0/ms)**2*(-b3**2*(chixx*ax**2+chiyy*ay**2-chixy*ax*ay)-2.0*b21*b3*az*(chiyz*ay-chixz*ax)-chizz*4.0*b21**2*az**2)*10.0**(-9)  
    dc33= -(b22/ms)**2*(4.0*chizz*az**2)*10.0**(-9) 
    dc44= -(b4/ms)**2*(chizz*ay**2 + chiyz*ay*az + chiyy*az**2)*10.0**(-9)
    dc55= -(b4/ms)**2*(chixx*az**2 + chizz*ax**2 + chixz*ax*az)*10.0**(-9)
    dc66= -(b3/ms)**2*(chixx*ay**2 + chiyy*ax**2 + chixy*ax*ay)*10.0**(-9)
    dc12= (1.0/ms)**2*(b3**2*(chixx*ax**2+chiyy*ay**2-chixy*ax*ay)-4.0*b21**2*az**2*chizz)*10.0**(-9)
    dc13= (1.0/ms)**2*(-b22*b3*(chixz*ax*az-chiyz*ay*az)-4.0*chizz*b21*b22*az**2)*10.0**(-9)
    dc14= -(1.0/ms)**2*(0.5*b4)*(b3*(-2.0*chiyy*ay*az+chixy*ax*az+chixz*ax*ay-chiyz*ay**2)+b21*(4.0*chizz*ay*az+2.0*chiyz*az**2))*10.0**(-9)
    dc15= -(1.0/ms)**2*(0.5*b4)*(b3*(2.0*chixx*ax*az-chixy*ay*az-chiyz*ax*ay+chixz*ax**2)+b21*(4.0*chizz*ax*az+2.0*chixz*az**2))*10.0**(-9)
    dc16= -(1.0/ms)**2*(0.5*b3)*(2.0*b3*ax*ay*(chixx-chiyy)+b3*chixy*(ax**2-ay**2)+2.0*b21*az*(ay*chixz+ax*chiyz))*10.0**(-9)
    dc23= (1.0/ms)**2*(b3*b22*az*(ax*chixz-ay*chiyz)-4.0*b21*b22*az**2*chizz)*10.0**(-9)
    dc24= -(1.0/ms)**2*(0.5*b4)*(b3*(2.0*chiyy*ay*az-chixy*ax*az-chixz*ax*ay+chiyz*ay**2)+b21*(4.0*chizz*ay*az+2.0*chiyz*az**2))*10.0**(-9)
    dc25= -(1.0/ms)**2*(0.5*b4)*(b3*(-2.0*chixx*ax*az+chixy*ay*az-chixz*ax**2+chiyz*ax*ay)+b21*(4.0*chizz*ax*az+2.0*chixz*az**2))*10.0**(-9)
    dc26= -(1.0/ms)**2*(0.5*b4)*(b3*(-2.0*chixx*ay*ax+2.0*chiyy*ax*ay+chixy*ay*ay-chixy*ax**2)+b21*(2.0*chixz*ay*az+2.0*chiyz*az*ax))*10.0**(-9)
    dc34= -((b22*b4)/(ms**2))*az*(2.0*chizz*ay + az*chiyz)*10.0**(-9)
    dc35= -((b22*b4)/(ms**2))*az*(2.0*chizz*ax + az*chixz)*10.0**(-9)
    dc36= -((b22*b3)/(ms**2))*az*(chixz*ay + ax*chiyz)*10.0**(-9)
    dc45= -0.5*(b4/ms)**2*(chixy*az**2 + chixz*ay*az + chiyz*ax*az + 2.0*chizz*ax*ay)*10.0**(-9)
    dc46= -0.5*(1.0/ms)**2*b3*b4*(chixy*ay*az + chixz*ay*ay + 2.0*chiyy*ax*az + chiyz*ax*ay)*10.0**(-9)
    dc56= -0.5*(1.0/ms)**2*b3*b4*(2.0*chixx*ay*az + chixy*ax*az + chixz*ax*ay + chiyz*ax*ax)*10.0**(-9)
    
    
    a11=(cc11*10**9/rho)+(dc11*10**9/rho)
    a12=(cc12*10**9/rho)+(dc12*10**9/rho)
    a13=(cc13*10**9/rho)+(dc13*10**9/rho)
    a14=(0.0*10**9/rho)+(dc14*10**9/rho)
    a15=(0.0*10**9/rho)+(dc15*10**9/rho)
    a16=(0.0*10**9/rho)+(dc16*10**9/rho)
    a22=(cc11*10**9/rho)+(dc22*10**9/rho)
    a23=(cc13*10**9/rho)+(dc23*10**9/rho)
    a24=(0.0*10**9/rho)+(dc24*10**9/rho)
    a25=(0.0*10**9/rho)+(dc25*10**9/rho)
    a26=(0.0*10**9/rho)+(dc26*10**9/rho)
    a33=(cc33*10**9/rho)+(dc33*10**9/rho)
    a34=(0.0*10**9/rho)+(dc34*10**9/rho)
    a35=(0.0*10**9/rho)+(dc35*10**9/rho)
    a36=(0.0*10**9/rho)+(dc36*10**9/rho)
    a44=(cc44*10**9/rho)+(dc44*10**9/rho)
    a45=(0.0*10**9/rho)+(dc45*10**9/rho)
    a46=(0.0*10**9/rho)+(dc46*10**9/rho)
    a55=(cc44*10**9/rho)+(dc55*10**9/rho)
    a56=(0.0*10**9/rho)+(dc56*10**9/rho)
    a66=(0.5*(cc11-cc12)*10**9/rho)+(dc66*10**9/rho)
    
    a011=(cc11*10**9/rho)
    a012=(cc12*10**9/rho)
    a013=(cc13*10**9/rho)
    a014=(0.0*10**9/rho)
    a015=(0.0*10**9/rho)
    a016=(0.0*10**9/rho)
    a022=(cc11*10**9/rho)
    a023=(cc13*10**9/rho)
    a024=(0.0*10**9/rho)
    a025=(0.0*10**9/rho)
    a026=(0.0*10**9/rho)
    a033=(cc33*10**9/rho)
    a034=(0.0*10**9/rho)
    a035=(0.0*10**9/rho)
    a036=(0.0*10**9/rho)
    a044=(cc44*10**9/rho)
    a045=(0.0*10**9/rho)
    a046=(0.0*10**9/rho)
    a055=(cc44*10**9/rho)
    a056=(0.0*10**9/rho)
    a066=(0.5*(cc11-cc12)*10**9/rho)
    
    kk=np.sqrt(kx**2+ky**2+kz*2)
    kkx=kx/kk
    kky=ky/kk
    kkz=kz/kk
    
    
    vvx,vvy,vvz = vel(a11,a12,a13,a14,a15,a16,a22,a23,a24,a25,a26,a33,a34,a35,a36,a44,a45,a46,a55,a56,a66,kkx,kky,kkz,sol)
        
    vvvx,vvvy,vvvz = vel(a011,a012,a013,a014,a015,a016,a022,a023,a024,a025,a026,a033,a034,a035,a036,a044,a045,a046,a055,a056,a066,kkx,kky,kkz,sol)
    
    vx0=vvx
    vy0=vvy
    vz0=vvz
    v0=np.sqrt(vx0**2+vy0**2+vz0**2)
        
    vx00=vvvx
    vy00=vvvy
    vz00=vvvz
    v00=np.sqrt(vx00**2+vy00**2+vz00**2)
        
    v000=(v0-v00)/v00


  
    return dc11,dc12,dc13,dc14,dc15,dc16,dc22,dc23,dc24,dc25,dc26,dc33,dc34,dc35,dc36,dc44,dc45,dc46,dc55,dc56,dc66,ax,ay,az,vx0,vy0,vz0,v0,vx00,vy00,vz00,v00,v000

def enehex(x,a):

  hx0=a[0]
  hy0=a[1]
  hz0=a[2]
  Ms0=a[3]
  k1eff0=a[4]
  k2eff0=a[5]
  theta=x[0]
  phi=x[1]
  
  return k1eff0*(1-np.cos(theta)**2) + k2eff0**(1-np.cos(theta)**2)**2 - Ms0*(np.sin(theta)*np.cos(phi)*hx0 + np.sin(theta)*np.sin(phi)*hy0 + np.cos(theta)*hz0)



def etth(x,y,hhx,hhy,hhz,ms,kk1eff,kk2eff):
  
  ff0 = -0.5*ms*(-hhz*np.cos(x) - hhx*np.cos(y)*np.sin(x) - hhy*np.sin(x)*np.sin(y))
  ff1 = 2.0*kk1eff*(np.cos(x)**2 - np.sin(x)**2)
  ff2 = kk2eff*(4.0*np.cos(x)**2*(1.0 - np.cos(x)*2) + 8.0*np.cos(x)**2*np.sin(x)**2 - 4.0*(1.0 - np.cos(x)**2)*np.sin(x)**2)
     

  
  ff=ff0+ff1+ff2 
     
  return ff
     
  
def epph(x,y,hhx,hhy,hhz,ms,kk1eff,kk2eff):
  ff0 = -0.5*ms*(-hhx*np.cos(y)*np.sin(x) - hhy*np.sin(x)*np.sin(y)) 
  
  ff1=0.0
  
  ff2=0.0

  ff=ff0+ff1+ff2  
     
  return ff



##############wang numerical

@app.callback(
    [Output('vxnumtric', 'children'),
     Output('vynumtric', 'children'),
     Output('vznumtric', 'children'),
     Output('v0numtric', 'children'),
    ],
    [Input(component_id='c11tric', component_property='value'),
     Input(component_id='c12tric', component_property='value'),
     Input(component_id='c13tric', component_property='value'),
     Input(component_id='c14tric', component_property='value'),
     Input(component_id='c15tric', component_property='value'),
     Input(component_id='c16tric', component_property='value'),
     Input(component_id='c22tric', component_property='value'),
     Input(component_id='c23tric', component_property='value'),
     Input(component_id='c24tric', component_property='value'),
     Input(component_id='c25tric', component_property='value'),
     Input(component_id='c26tric', component_property='value'),
     Input(component_id='c33tric', component_property='value'),
     Input(component_id='c34tric', component_property='value'),
     Input(component_id='c35tric', component_property='value'),
     Input(component_id='c36tric', component_property='value'),
     Input(component_id='c44tric', component_property='value'),
     Input(component_id='c45tric', component_property='value'),
     Input(component_id='c46tric', component_property='value'),
     Input(component_id='c55tric', component_property='value'),
     Input(component_id='c56tric', component_property='value'),
     Input(component_id='c66tric', component_property='value'),
     Input(component_id='rhotric', component_property='value'),
     Input(component_id='kxtric', component_property='value'),
     Input(component_id='kytric', component_property='value'),
     Input(component_id='kztric', component_property='value'),
     Input(component_id='sol_num_tric', component_property='value'),
    ],

)


def update_numerical_tric(cc11,cc12,cc13,cc14,cc15,cc16,cc22,cc23,cc24,cc25,cc26,cc33,cc34,cc35,cc36,cc44,cc45,cc46,cc55,cc56,cc66,rho,kx,ky,kz,sol):


    a11=cc11*10**9/rho
    a12=cc12*10**9/rho
    a13=cc13*10**9/rho
    a14=cc14*10**9/rho
    a15=cc15*10**9/rho
    a16=cc16*10**9/rho
    a22=cc22*10**9/rho
    a23=cc23*10**9/rho
    a24=cc24*10**9/rho
    a25=cc25*10**9/rho
    a26=cc26*10**9/rho
    a33=cc33*10**9/rho
    a34=cc34*10**9/rho
    a35=cc35*10**9/rho
    a36=cc36*10**9/rho
    a44=cc44*10**9/rho
    a45=cc45*10**9/rho
    a46=cc46*10**9/rho
    a55=cc55*10**9/rho
    a56=cc56*10**9/rho
    a66=cc66*10**9/rho
    
    kk=np.sqrt(kx**2+ky**2+kz**2)
    kkx=kx/kk
    kky=ky/kk
    kkz=kz/kk
    
    
    vx0,vy0,vz0 = vel(a11,a12,a13,a14,a15,a16,a22,a23,a24,a25,a26,a33,a34,a35,a36,a44,a45,a46,a55,a56,a66,kkx,kky,kkz,sol)
    

    v0=np.sqrt(vx0**2+vy0**2+vz0**2)
  
  
    return vx0,vy0,vz0,v0    






############## Wang_method_3D_plot

@app.callback(
    Output('tric_3D', 'figure'),
    [Input(component_id='c11tric3d', component_property='value'),
     Input(component_id='c12tric3d', component_property='value'),
     Input(component_id='c13tric3d', component_property='value'),
     Input(component_id='c14tric3d', component_property='value'),
     Input(component_id='c15tric3d', component_property='value'),
     Input(component_id='c16tric3d', component_property='value'),
     Input(component_id='c22tric3d', component_property='value'),
     Input(component_id='c23tric3d', component_property='value'),
     Input(component_id='c24tric3d', component_property='value'),
     Input(component_id='c25tric3d', component_property='value'),
     Input(component_id='c26tric3d', component_property='value'),
     Input(component_id='c33tric3d', component_property='value'),
     Input(component_id='c34tric3d', component_property='value'),
     Input(component_id='c35tric3d', component_property='value'),
     Input(component_id='c36tric3d', component_property='value'),
     Input(component_id='c44tric3d', component_property='value'),
     Input(component_id='c45tric3d', component_property='value'),
     Input(component_id='c46tric3d', component_property='value'),
     Input(component_id='c55tric3d', component_property='value'),
     Input(component_id='c56tric3d', component_property='value'),
     Input(component_id='c66tric3d', component_property='value'),
     Input(component_id='rhotric3d', component_property='value'),
     Input(component_id='ntric3d', component_property='value'),
     Input(component_id='soltric3d', component_property='value'),
    ],

)


def update_tric3d(cc11,cc12,cc13,cc14,cc15,cc16,cc22,cc23,cc24,cc25,cc26,cc33,cc34,cc35,cc36,cc44,cc45,cc46,cc55,cc56,cc66,rho,nn,sol):

    
    n=int(np.sqrt(nn))
    
    aa=complex(0,n)
    
    a11=cc11*10**9/rho
    a12=cc12*10**9/rho
    a13=cc13*10**9/rho
    a14=cc14*10**9/rho
    a15=cc15*10**9/rho
    a16=cc16*10**9/rho
    a22=cc22*10**9/rho
    a23=cc23*10**9/rho
    a24=cc24*10**9/rho
    a25=cc25*10**9/rho
    a26=cc26*10**9/rho
    a33=cc33*10**9/rho
    a34=cc34*10**9/rho
    a35=cc35*10**9/rho
    a36=cc36*10**9/rho
    a44=cc44*10**9/rho
    a45=cc45*10**9/rho
    a46=cc46*10**9/rho
    a55=cc55*10**9/rho
    a56=cc56*10**9/rho
    a66=cc66*10**9/rho
    
    u, v = np.mgrid[0:np.pi:aa, 0:2*np.pi:aa]
    kkx = np.sin(u)*np.cos(v)
    kky = np.sin(u)*np.sin(v)
    kkz = np.cos(u)
    
    
    vx0=np.zeros((n,n))
    vy0=np.zeros((n,n))
    vz0=np.zeros((n,n))
    v0=np.zeros((n,n))
    
    
    for ii in range(0, n):
  
      for jj in range(0, n):
    
        kx=kkx[ii,jj]
        ky=kky[ii,jj]
        kz=kkz[ii,jj]
        
        vvx,vvy,vvz = vel(a11,a12,a13,a14,a15,a16,a22,a23,a24,a25,a26,a33,a34,a35,a36,a44,a45,a46,a55,a56,a66,kx,ky,kz,sol)
    
        vx0[ii,jj]=vvx
        vy0[ii,jj]=vvy
        vz0[ii,jj]=vvz
        v0[ii,jj]=np.sqrt(vx0[ii,jj]**2+vy0[ii,jj]**2+vz0[ii,jj]**2)
    

    x = v0*kkx
    y = v0*kky
    z = v0*kkz


    list00 = np.stack((np.transpose(x),np.transpose(y),np.transpose(z),np.transpose(v0)),axis=0)
    list0 = np.stack((v0,vx0,vy0,vz0,kkx,kky,kkz,u*(180.0/np.pi),v*(180.0/np.pi)),axis=-1)



    fig = make_subplots(rows=1, cols=1,
                    specs=[[{'is_3d': True}]],
                    subplot_titles=['  Color corresponds to the magnitude of sound velocity (group velocity) |v|(m/s) '])


    fig.add_trace(go.Surface(x=list00[0], y=list00[1], z=list00[2], surfacecolor=list00[3], customdata=list0, name=" ", hoverinfo="name",
                                 hovertemplate = """v = %{customdata[0]:.6g} m/s<br>vx = %{customdata[1]:.6g} m/s<br>vy = %{customdata[2]:.6g} m/s<br>vz = %{customdata[3]:.6g} m/s<br>nx = kx/k = %{customdata[4]:.6g}<br>ny = ky/k = %{customdata[5]:.6g}<br>nz = kz/k = %{customdata[6]:.6g}<br>θ = %{customdata[7]:.6g}°<br>φ = %{customdata[8]:.6g}°<br>"""),1, 1)


    fig.update_layout(transition_duration=500)

    fig.update_layout(
        scene = {
            "xaxis": {"showticklabels": False},
            "yaxis": {"showticklabels": False},
            "zaxis": {"showticklabels": False}
        })
        
    fig.update_layout(
        scene = {
            "xaxis": {"title": "nx"},
            "yaxis": {"title": "ny"},
            "zaxis": {"title": "nz"}
        })
    

    
  #  stat = 'The figure has been generated successfully!'
    
    return fig

def vel(a11,a12,a13,a14,a15,a16,a22,a23,a24,a25,a26,a33,a34,a35,a36,a44,a45,a46,a55,a56,a66,n1,n2,n3,sol):
  
  g11=a11*n1*n1+2.0*a16*n1*n2+2.0*a15*n1*n3+a66*n2*n2+2.0*a56*n2*n3+a55*n3*n3
  g12=a16*n1*n1+(a12+a66)*n1*n2+(a14+a56)*n1*n3+a26*n2*n2+(a25+a46)*n2*n3+a45*n3*n3
  g13=a15*n1*n1+(a14+a56)*n1*n2+(a13+a55)*n1*n3+a46*n2*n2+(a36+a45)*n2*n3+a35*n3*n3
  g22=a66*n1*n1+2.0*a26*n1*n2+2.0*a46*n1*n3+a22*n2*n2+2.0*a24*n2*n3+a44*n3*n3
  g23=a56*n1*n1+(a25+a46)*n1*n2+(a36+a45)*n1*n3+a24*n2*n2+(a23+a44)*n2*n3+a34*n3*n3
  g33=a55*n1*n1+2.0*a45*n1*n2+2.0*a35*n1*n3+a44*n2*n2+2.0*a34*n2*n3+a33*n3*n3

  bb=-(g11+g22+g33)
  cc=g11*g33+g22*g33+g11*g22-g12**2-g13**2-g23**2
  dd=g23**2*g11+g13**2*g22+g12**2*g33-g11*g22*g33-2.0*g12*g13*g23


#  p=g11+g22+g33
#  q=g11*g22-g12**2+g22*g33-g23**2+g11*g33-g13**2
#  detg=g11*(g22*g33-g23**2)-g12*(g12*g33-g23*g13)+g13*(g12*g23-g22*g13)
#  r=np.sqrt(-(1.0/27.0)*(q-((p**2)/3.0))**3)


  dbdn1= -2.0*a11*n1 - 2.0*a15*n3 - 2.0*a16*n2 - 2.0*a26*n2 - 2.0*a35*n3 - 2.0*a45*n2 - 2.0*a46*n3 - 2.0*a55*n1 - 2.0*a66*n1
  dbdn2= -2.0*a16*n1 - 2.0*a22*n2 - 2.0*a24*n3 - 2.0*a26*n1 - 2.0*a34*n3 - 2.0*a44*n2 - 2.0*a45*n1 - 2.0*a56*n3 - 2.0*a66*n2
  dbdn3= -2.0*a15*n1 - 2.0*a24*n2 - 2.0*a33*n3 - 2.0*a34*n2 - 2.0*a35*n1 - 2.0*a44*n3 - 2.0*a46*n1 - 2.0*a55*n3 - 2.0*a56*n2


  dcdn1= (2*a11*n1 + 2.0*a15*n3 + 2.0*a16*n2)*(a22*n2**2 + 2.0*a24*n2*n3 + 2.0*a26*n1*n2 + a44*n3**2 + 2.0*a46*n1*n3 + a66*n1**2) + (2*a11*n1 + 2.0*a15*n3 + 2.0*a16*n2)*(a33*n3**2 + 2.0*a34*n2*n3 + 2.0*a35*n1*n3 + a44*n2**2 + 2.0*a45*n1*n2 + a55*n1**2) - (4*a15*n1 + 2*n2*(a14 + a56) + 2*n3*(a13 + a55))*(a15*n1**2 + a35*n3**2 + a46*n2**2 + n1*n2*(a14 + a56) + n1*n3*(a13 + a55) + n2*n3*(a36 + a45)) - (4*a16*n1 + 2*n2*(a12 + a66) + 2*n3*(a14 + a56))*(a16*n1**2 + a26*n2**2 + a45*n3**2 + n1*n2*(a12 + a66) + n1*n3*(a14 + a56) + n2*n3*(a25 + a46)) + (2.0*a26*n2 + 2.0*a46*n3 + 2*a66*n1)*(a11*n1**2 + 2.0*a15*n1*n3 + 2.0*a16*n1*n2 + a55*n3**2 + 2.0*a56*n2*n3 + a66*n2**2) + (2.0*a26*n2 + 2.0*a46*n3 + 2*a66*n1)*(a33*n3**2 + 2.0*a34*n2*n3 + 2.0*a35*n1*n3 + a44*n2**2 + 2.0*a45*n1*n2 + a55*n1**2) + (2.0*a35*n3 + 2.0*a45*n2 + 2*a55*n1)*(a11*n1**2 + 2.0*a15*n1*n3 + 2.0*a16*n1*n2 + a55*n3**2 + 2.0*a56*n2*n3 + a66*n2**2) + (2.0*a35*n3 + 2.0*a45*n2 + 2*a55*n1)*(a22*n2**2 + 2.0*a24*n2*n3 + 2.0*a26*n1*n2 + a44*n3**2 + 2.0*a46*n1*n3 + a66*n1**2) - (4*a56*n1 + 2*n2*(a25 + a46) + 2*n3*(a36 + a45))*(a24*n2**2 + a34*n3**2 + a56*n1**2 + n1*n2*(a25 + a46) + n1*n3*(a36 + a45) + n2*n3*(a23 + a44))

  dcdn2= (2.0*a16*n1 + 2.0*a56*n3 + 2*a66*n2)*(a22*n2**2 + 2.0*a24*n2*n3 + 2.0*a26*n1*n2 + a44*n3**2 + 2.0*a46*n1*n3 + a66*n1**2) + (2.0*a16*n1 + 2.0*a56*n3 + 2*a66*n2)*(a33*n3**2 + 2.0*a34*n2*n3 + 2.0*a35*n1*n3 + a44*n2**2 + 2.0*a45*n1*n2 + a55*n1**2) + (2*a22*n2 + 2.0*a24*n3 + 2.0*a26*n1)*(a11*n1**2 + 2.0*a15*n1*n3 + 2.0*a16*n1*n2 + a55*n3**2 + 2.0*a56*n2*n3 + a66*n2**2) + (2*a22*n2 + 2.0*a24*n3 + 2.0*a26*n1)*(a33*n3**2 + 2.0*a34*n2*n3 + 2.0*a35*n1*n3 + a44*n2**2 + 2.0*a45*n1*n2 + a55*n1**2) - (4*a24*n2 + 2*n1*(a25 + a46) + 2*n3*(a23 + a44))*(a24*n2**2 + a34*n3**2 + a56*n1**2 + n1*n2*(a25 + a46) + n1*n3*(a36 + a45) + n2*n3*(a23 + a44)) - (4*a26*n2 + 2*n1*(a12 + a66) + 2*n3*(a25 + a46))*(a16*n1**2 + a26*n2**2 + a45*n3**2 + n1*n2*(a12 + a66) + n1*n3*(a14 + a56) + n2*n3*(a25 + a46)) + (2.0*a34*n3 + 2*a44*n2 + 2.0*a45*n1)*(a11*n1**2 + 2.0*a15*n1*n3 + 2.0*a16*n1*n2 + a55*n3**2 + 2.0*a56*n2*n3 + a66*n2**2) + (2.0*a34*n3 + 2*a44*n2 + 2.0*a45*n1)*(a22*n2**2 + 2.0*a24*n2*n3 + 2.0*a26*n1*n2 + a44*n3**2 + 2.0*a46*n1*n3 + a66*n1**2) - (4*a46*n2 + 2*n1*(a14 + a56) + 2*n3*(a36 + a45))*(a15*n1**2 + a35*n3**2 + a46*n2**2 + n1*n2*(a14 + a56) + n1*n3*(a13 + a55) + n2*n3*(a36 + a45))

  dcdn3= (2.0*a15*n1 + 2*a55*n3 + 2.0*a56*n2)*(a22*n2**2 + 2.0*a24*n2*n3 + 2.0*a26*n1*n2 + a44*n3**2 + 2.0*a46*n1*n3 + a66*n1**2) + (2.0*a15*n1 + 2*a55*n3 + 2.0*a56*n2)*(a33*n3**2 + 2.0*a34*n2*n3 + 2.0*a35*n1*n3 + a44*n2**2 + 2.0*a45*n1*n2 + a55*n1**2) + (2.0*a24*n2 + 2*a44*n3 + 2.0*a46*n1)*(a11*n1**2 + 2.0*a15*n1*n3 + 2.0*a16*n1*n2 + a55*n3**2 + 2.0*a56*n2*n3 + a66*n2**2) + (2.0*a24*n2 + 2*a44*n3 + 2.0*a46*n1)*(a33*n3**2 + 2.0*a34*n2*n3 + 2.0*a35*n1*n3 + a44*n2**2 + 2.0*a45*n1*n2 + a55*n1**2) + (2*a33*n3 + 2.0*a34*n2 + 2.0*a35*n1)*(a11*n1**2 + 2.0*a15*n1*n3 + 2.0*a16*n1*n2 + a55*n3**2 + 2.0*a56*n2*n3 + a66*n2**2) + (2*a33*n3 + 2.0*a34*n2 + 2.0*a35*n1)*(a22*n2**2 + 2.0*a24*n2*n3 + 2.0*a26*n1*n2 + a44*n3**2 + 2.0*a46*n1*n3 + a66*n1**2) - (4*a34*n3 + 2*n1*(a36 + a45) + 2*n2*(a23 + a44))*(a24*n2**2 + a34*n3**2 + a56*n1**2 + n1*n2*(a25 + a46) + n1*n3*(a36 + a45) + n2*n3*(a23 + a44)) - (4*a35*n3 + 2*n1*(a13 + a55) + 2*n2*(a36 + a45))*(a15*n1**2 + a35*n3**2 + a46*n2**2 + n1*n2*(a14 + a56) + n1*n3*(a13 + a55) + n2*n3*(a36 + a45)) - (4*a45*n3 + 2*n1*(a14 + a56) + 2*n2*(a25 + a46))*(a16*n1**2 + a26*n2**2 + a45*n3**2 + n1*n2*(a12 + a66) + n1*n3*(a14 + a56) + n2*n3*(a25 + a46))

  dddn1= (-2*a11*n1 - 2.0*a15*n3 - 2.0*a16*n2)*(a22*n2**2 + 2.0*a24*n2*n3 + 2.0*a26*n1*n2 + a44*n3**2 + 2.0*a46*n1*n3 + a66*n1**2)*(a33*n3**2 + 2.0*a34*n2*n3 + 2.0*a35*n1*n3 + a44*n2**2 + 2.0*a45*n1*n2 + a55*n1**2) + (2*a11*n1 + 2.0*a15*n3 + 2.0*a16*n2)*(a24*n2**2 + a34*n3**2 + a56*n1**2 + n1*n2*(a25 + a46) + n1*n3*(a36 + a45) + n2*n3*(a23 + a44))**2 + (-2*a15*n1 - n2*(a14 + a56) - n3*(a13 + a55))*(2.0*a16*n1**2 + 2.0*a26*n2**2 + 2.0*a45*n3**2 + 2.0*n1*n2*(a12 + a66) + 2.0*n1*n3*(a14 + a56) + 2.0*n2*n3*(a25 + a46))*(a24*n2**2 + a34*n3**2 + a56*n1**2 + n1*n2*(a25 + a46) + n1*n3*(a36 + a45) + n2*n3*(a23 + a44)) + (4*a15*n1 + 2*n2*(a14 + a56) + 2*n3*(a13 + a55))*(a15*n1**2 + a35*n3**2 + a46*n2**2 + n1*n2*(a14 + a56) + n1*n3*(a13 + a55) + n2*n3*(a36 + a45))*(a22*n2**2 + 2.0*a24*n2*n3 + 2.0*a26*n1*n2 + a44*n3**2 + 2.0*a46*n1*n3 + a66*n1**2) + (4*a16*n1 + 2*n2*(a12 + a66) + 2*n3*(a14 + a56))*(a16*n1**2 + a26*n2**2 + a45*n3**2 + n1*n2*(a12 + a66) + n1*n3*(a14 + a56) + n2*n3*(a25 + a46))*(a33*n3**2 + 2.0*a34*n2*n3 + 2.0*a35*n1*n3 + a44*n2**2 + 2.0*a45*n1*n2 + a55*n1**2) + (4.0*a16*n1 + 2.0*n2*(a12 + a66) + 2.0*n3*(a14 + a56))*(-a15*n1**2 - a35*n3**2 - a46*n2**2 - n1*n2*(a14 + a56) - n1*n3*(a13 + a55) - n2*n3*(a36 + a45))*(a24*n2**2 + a34*n3**2 + a56*n1**2 + n1*n2*(a25 + a46) + n1*n3*(a36 + a45) + n2*n3*(a23 + a44)) + (2.0*a26*n2 + 2.0*a46*n3 + 2*a66*n1)*(-a11*n1**2 - 2.0*a15*n1*n3 - 2.0*a16*n1*n2 - a55*n3**2 - 2.0*a56*n2*n3 - a66*n2**2)*(a33*n3**2 + 2.0*a34*n2*n3 + 2.0*a35*n1*n3 + a44*n2**2 + 2.0*a45*n1*n2 + a55*n1**2) + (2.0*a26*n2 + 2.0*a46*n3 + 2*a66*n1)*(a15*n1**2 + a35*n3**2 + a46*n2**2 + n1*n2*(a14 + a56) + n1*n3*(a13 + a55) + n2*n3*(a36 + a45))**2 + (2.0*a35*n3 + 2.0*a45*n2 + 2*a55*n1)*(-a11*n1**2 - 2.0*a15*n1*n3 - 2.0*a16*n1*n2 - a55*n3**2 - 2.0*a56*n2*n3 - a66*n2**2)*(a22*n2**2 + 2.0*a24*n2*n3 + 2.0*a26*n1*n2 + a44*n3**2 + 2.0*a46*n1*n3 + a66*n1**2) + (2.0*a35*n3 + 2.0*a45*n2 + 2*a55*n1)*(a16*n1**2 + a26*n2**2 + a45*n3**2 + n1*n2*(a12 + a66) + n1*n3*(a14 + a56) + n2*n3*(a25 + a46))**2 + (2*a56*n1 + n2*(a25 + a46) + n3*(a36 + a45))*(-a15*n1**2 - a35*n3**2 - a46*n2**2 - n1*n2*(a14 + a56) - n1*n3*(a13 + a55) - n2*n3*(a36 + a45))*(2.0*a16*n1**2 + 2.0*a26*n2**2 + 2.0*a45*n3**2 + 2.0*n1*n2*(a12 + a66) + 2.0*n1*n3*(a14 + a56) + 2.0*n2*n3*(a25 + a46)) + (4*a56*n1 + 2*n2*(a25 + a46) + 2*n3*(a36 + a45))*(a11*n1**2 + 2.0*a15*n1*n3 + 2.0*a16*n1*n2 + a55*n3**2 + 2.0*a56*n2*n3 + a66*n2**2)*(a24*n2**2 + a34*n3**2 + a56*n1**2 + n1*n2*(a25 + a46) + n1*n3*(a36 + a45) + n2*n3*(a23 + a44))

  dddn2= (-2.0*a16*n1 - 2.0*a56*n3 - 2*a66*n2)*(a22*n2**2 + 2.0*a24*n2*n3 + 2.0*a26*n1*n2 + a44*n3**2 + 2.0*a46*n1*n3 + a66*n1**2)*(a33*n3**2 + 2.0*a34*n2*n3 + 2.0*a35*n1*n3 + a44*n2**2 + 2.0*a45*n1*n2 + a55*n1**2) + (2.0*a16*n1 + 2.0*a56*n3 + 2*a66*n2)*(a24*n2**2 + a34*n3**2 + a56*n1**2 + n1*n2*(a25 + a46) + n1*n3*(a36 + a45) + n2*n3*(a23 + a44))**2 + (2*a22*n2 + 2.0*a24*n3 + 2.0*a26*n1)*(-a11*n1**2 - 2.0*a15*n1*n3 - 2.0*a16*n1*n2 - a55*n3**2 - 2.0*a56*n2*n3 - a66*n2**2)*(a33*n3**2 + 2.0*a34*n2*n3 + 2.0*a35*n1*n3 + a44*n2**2 + 2.0*a45*n1*n2 + a55*n1**2) + (2*a22*n2 + 2.0*a24*n3 + 2.0*a26*n1)*(a15*n1**2 + a35*n3**2 + a46*n2**2 + n1*n2*(a14 + a56) + n1*n3*(a13 + a55) + n2*n3*(a36 + a45))**2 + (2*a24*n2 + n1*(a25 + a46) + n3*(a23 + a44))*(-a15*n1**2 - a35*n3**2 - a46*n2**2 - n1*n2*(a14 + a56) - n1*n3*(a13 + a55) - n2*n3*(a36 + a45))*(2.0*a16*n1**2 + 2.0*a26*n2**2 + 2.0*a45*n3**2 + 2.0*n1*n2*(a12 + a66) + 2.0*n1*n3*(a14 + a56) + 2.0*n2*n3*(a25 + a46)) + (4*a24*n2 + 2*n1*(a25 + a46) + 2*n3*(a23 + a44))*(a11*n1**2 + 2.0*a15*n1*n3 + 2.0*a16*n1*n2 + a55*n3**2 + 2.0*a56*n2*n3 + a66*n2**2)*(a24*n2**2 + a34*n3**2 + a56*n1**2 + n1*n2*(a25 + a46) + n1*n3*(a36 + a45) + n2*n3*(a23 + a44)) + (4.0*a26*n2 + 2.0*n1*(a12 + a66) + 2.0*n3*(a25 + a46))*(-a15*n1**2 - a35*n3**2 - a46*n2**2 - n1*n2*(a14 + a56) - n1*n3*(a13 + a55) - n2*n3*(a36 + a45))*(a24*n2**2 + a34*n3**2 + a56*n1**2 + n1*n2*(a25 + a46) + n1*n3*(a36 + a45) + n2*n3*(a23 + a44)) + (4*a26*n2 + 2*n1*(a12 + a66) + 2*n3*(a25 + a46))*(a16*n1**2 + a26*n2**2 + a45*n3**2 + n1*n2*(a12 + a66) + n1*n3*(a14 + a56) + n2*n3*(a25 + a46))*(a33*n3**2 + 2.0*a34*n2*n3 + 2.0*a35*n1*n3 + a44*n2**2 + 2.0*a45*n1*n2 + a55*n1**2) + (2.0*a34*n3 + 2*a44*n2 + 2.0*a45*n1)*(-a11*n1**2 - 2.0*a15*n1*n3 - 2.0*a16*n1*n2 - a55*n3**2 - 2.0*a56*n2*n3 - a66*n2**2)*(a22*n2**2 + 2.0*a24*n2*n3 + 2.0*a26*n1*n2 + a44*n3**2 + 2.0*a46*n1*n3 + a66*n1**2) + (2.0*a34*n3 + 2*a44*n2 + 2.0*a45*n1)*(a16*n1**2 + a26*n2**2 + a45*n3**2 + n1*n2*(a12 + a66) + n1*n3*(a14 + a56) + n2*n3*(a25 + a46))**2 + (-2*a46*n2 - n1*(a14 + a56) - n3*(a36 + a45))*(2.0*a16*n1**2 + 2.0*a26*n2**2 + 2.0*a45*n3**2 + 2.0*n1*n2*(a12 + a66) + 2.0*n1*n3*(a14 + a56) + 2.0*n2*n3*(a25 + a46))*(a24*n2**2 + a34*n3**2 + a56*n1**2 + n1*n2*(a25 + a46) + n1*n3*(a36 + a45) + n2*n3*(a23 + a44)) + (4*a46*n2 + 2*n1*(a14 + a56) + 2*n3*(a36 + a45))*(a15*n1**2 + a35*n3**2 + a46*n2**2 + n1*n2*(a14 + a56) + n1*n3*(a13 + a55) + n2*n3*(a36 + a45))*(a22*n2**2 + 2.0*a24*n2*n3 + 2.0*a26*n1*n2 + a44*n3**2 + 2.0*a46*n1*n3 + a66*n1**2)

  dddn3= (-2.0*a15*n1 - 2*a55*n3 - 2.0*a56*n2)*(a22*n2**2 + 2.0*a24*n2*n3 + 2.0*a26*n1*n2 + a44*n3**2 + 2.0*a46*n1*n3 + a66*n1**2)*(a33*n3**2 + 2.0*a34*n2*n3 + 2.0*a35*n1*n3 + a44*n2**2 + 2.0*a45*n1*n2 + a55*n1**2) + (2.0*a15*n1 + 2*a55*n3 + 2.0*a56*n2)*(a24*n2**2 + a34*n3**2 + a56*n1**2 + n1*n2*(a25 + a46) + n1*n3*(a36 + a45) + n2*n3*(a23 + a44))**2 + (2.0*a24*n2 + 2*a44*n3 + 2.0*a46*n1)*(-a11*n1**2 - 2.0*a15*n1*n3 - 2.0*a16*n1*n2 - a55*n3**2 - 2.0*a56*n2*n3 - a66*n2**2)*(a33*n3**2 + 2.0*a34*n2*n3 + 2.0*a35*n1*n3 + a44*n2**2 + 2.0*a45*n1*n2 + a55*n1**2) + (2.0*a24*n2 + 2*a44*n3 + 2.0*a46*n1)*(a15*n1**2 + a35*n3**2 + a46*n2**2 + n1*n2*(a14 + a56) + n1*n3*(a13 + a55) + n2*n3*(a36 + a45))**2 + (2*a33*n3 + 2.0*a34*n2 + 2.0*a35*n1)*(-a11*n1**2 - 2.0*a15*n1*n3 - 2.0*a16*n1*n2 - a55*n3**2 - 2.0*a56*n2*n3 - a66*n2**2)*(a22*n2**2 + 2.0*a24*n2*n3 + 2.0*a26*n1*n2 + a44*n3**2 + 2.0*a46*n1*n3 + a66*n1**2) + (2*a33*n3 + 2.0*a34*n2 + 2.0*a35*n1)*(a16*n1**2 + a26*n2**2 + a45*n3**2 + n1*n2*(a12 + a66) + n1*n3*(a14 + a56) + n2*n3*(a25 + a46))**2 + (2*a34*n3 + n1*(a36 + a45) + n2*(a23 + a44))*(-a15*n1**2 - a35*n3**2 - a46*n2**2 - n1*n2*(a14 + a56) - n1*n3*(a13 + a55) - n2*n3*(a36 + a45))*(2.0*a16*n1**2 + 2.0*a26*n2**2 + 2.0*a45*n3**2 + 2.0*n1*n2*(a12 + a66) + 2.0*n1*n3*(a14 + a56) + 2.0*n2*n3*(a25 + a46)) + (4*a34*n3 + 2*n1*(a36 + a45) + 2*n2*(a23 + a44))*(a11*n1**2 + 2.0*a15*n1*n3 + 2.0*a16*n1*n2 + a55*n3**2 + 2.0*a56*n2*n3 + a66*n2**2)*(a24*n2**2 + a34*n3**2 + a56*n1**2 + n1*n2*(a25 + a46) + n1*n3*(a36 + a45) + n2*n3*(a23 + a44)) + (-2*a35*n3 - n1*(a13 + a55) - n2*(a36 + a45))*(2.0*a16*n1**2 + 2.0*a26*n2**2 + 2.0*a45*n3**2 + 2.0*n1*n2*(a12 + a66) + 2.0*n1*n3*(a14 + a56) + 2.0*n2*n3*(a25 + a46))*(a24*n2**2 + a34*n3**2 + a56*n1**2 + n1*n2*(a25 + a46) + n1*n3*(a36 + a45) + n2*n3*(a23 + a44)) + (4*a35*n3 + 2*n1*(a13 + a55) + 2*n2*(a36 + a45))*(a15*n1**2 + a35*n3**2 + a46*n2**2 + n1*n2*(a14 + a56) + n1*n3*(a13 + a55) + n2*n3*(a36 + a45))*(a22*n2**2 + 2.0*a24*n2*n3 + 2.0*a26*n1*n2 + a44*n3**2 + 2.0*a46*n1*n3 + a66*n1**2) + (4*a45*n3 + 2*n1*(a14 + a56) + 2*n2*(a25 + a46))*(a16*n1**2 + a26*n2**2 + a45*n3**2 + n1*n2*(a12 + a66) + n1*n3*(a14 + a56) + n2*n3*(a25 + a46))*(a33*n3**2 + 2.0*a34*n2*n3 + 2.0*a35*n1*n3 + a44*n2**2 + 2.0*a45*n1*n2 + a55*n1**2) + (4.0*a45*n3 + 2.0*n1*(a14 + a56) + 2.0*n2*(a25 + a46))*(-a15*n1**2 - a35*n3**2 - a46*n2**2 - n1*n2*(a14 + a56) - n1*n3*(a13 + a55) - n2*n3*(a36 + a45))*(a24*n2**2 + a34*n3**2 + a56*n1**2 + n1*n2*(a25 + a46) + n1*n3*(a36 + a45) + n2*n3*(a23 + a44))


  c2 = unaryCubicEquation(bb, cc, dd)
  
  c2 = np.array(c2)
  c4 = c2 * c2
  pv = np.sqrt(c2)
  EPS = 10**-7

  if np.abs(pv[1] - pv[2]) < EPS:
    nRoot = 2
    if np.abs(pv[0] - pv[2]) < EPS:
      nRoot = 1
  else:
    nRoot = 3
      
  if nRoot == 1:
    g = 6.0 * pv 
    vx=-dbdn1/g[0]
    vy=-dbdn2/g[0]
    vz=-dbdn3/g[0]
    
  elif nRoot == 2:
    g = np.array([2.0 * pv[0] * (3.0 * c4[0] + 2.0 * bb * c2[0] + cc),
                      4.0 * pv[1] * (3.0 * c2[1] + bb),
                      4.0 * pv[2] * (3.0 * c2[2] + bb)])
    if sol == 'sol_1':
      vx=-(c4[0] * dbdn1 + c2[0] * dcdn1 + dddn1) / g[0]
      vy=-(c4[0] * dbdn2 + c2[0] * dcdn2 + dddn2) / g[0]
      vz=-(c4[0] * dbdn3 + c2[0] * dcdn3 + dddn3) / g[0]
      
    elif sol == 'sol_2':
      vx=-(2.0 * c2[1] * dbdn1 + dcdn1) / g[1]
      vy=-(2.0 * c2[1] * dbdn2 + dcdn2) / g[1]
      vz=-(2.0 * c2[1] * dbdn3 + dcdn3) / g[1]
    
    elif sol == 'sol_3':
      vx=-(2.0 * c2[2] * dbdn1 + dcdn1) / g[2]
      vy=-(2.0 * c2[2] * dbdn2 + dcdn2) / g[2]
      vz=-(2.0 * c2[2] * dbdn3 + dcdn3) / g[2]
    
  else:
    g = 2.0 * pv * (3.0 * c4 + 2.0 * bb * c2 + cc)
    if sol == 'sol_1':
      vx=-(c4[0] * dbdn1 + c2[0] * dcdn1 + dddn1) / g[0]
      vy=-(c4[0] * dbdn2 + c2[0] * dcdn2 + dddn2) / g[0]
      vz=-(c4[0] * dbdn3 + c2[0] * dcdn3 + dddn3) / g[0]
      
    elif sol == 'sol_2':
      vx=-(c4[1] * dbdn1 + c2[1] * dcdn1 + dddn1) / g[1]
      vy=-(c4[1] * dbdn2 + c2[1] * dcdn2 + dddn2) / g[1]
      vz=-(c4[1] * dbdn3 + c2[1] * dcdn3 + dddn3) / g[1]
    
    elif sol == 'sol_3':
      vx=-(c4[2] * dbdn1 + c2[2] * dcdn1 + dddn1) / g[2]
      vy=-(c4[2] * dbdn2 + c2[2] * dcdn2 + dddn2) / g[2]
      vz=-(c4[2] * dbdn3 + c2[2] * dcdn3 + dddn3) / g[2]
  
  
  v0x=np.real(vx)
  v0y=np.real(vy)
  v0z=np.real(vz)
     
  return v0x,v0y,v0z

def unaryCubicEquation(B, C, D):
    # solve equation x**3 + Bx**2 + Cx + D = 0
    w = complex(-0.5, cmath.sqrt(0.75))
    w2 = w * w
    res = [0, 0, 0]
    sig = 1
    P = B * C / 6.0 - B ** 3 / 27.0 - 0.5 * D
    Q = (3.0 * C - B * B) / 9.0
    v = cmath.sqrt(P * P + Q ** 3)
    u = P + v
    v = P - v
    if abs(v) > abs(u):
        u = v
        sig = -1
    u = u ** (1.0 / 3.0)
    if abs(u) > 1.0e-15:
        v = -Q / u
    else:
        v = 0.0
    res[0] = -B / 3.0
    res[0] += u + v
    res[1] = -B / 3.0
    res[1] += u * w + v * w2    
    res[2] = -B / 3.0
    res[2] += u * w2 + v * w

    return res

############## cub_field_3D_plot

@app.callback(
    Output('output_cf', 'figure'),
    [Input(component_id='c11cf', component_property='value'),
     Input(component_id='c12cf', component_property='value'),
     Input(component_id='c44cf', component_property='value'),
     Input(component_id='mscf', component_property='value'),
     Input(component_id='k1cf', component_property='value'),
     Input(component_id='k2cf', component_property='value'),
     Input(component_id='b1cf', component_property='value'),
     Input(component_id='b2cf', component_property='value'),
     Input(component_id='hxcf', component_property='value'),
     Input(component_id='hycf', component_property='value'),
     Input(component_id='hzcf', component_property='value'),
     Input(component_id='rhocf', component_property='value'),
     Input(component_id='ncf', component_property='value'),
     Input(component_id='solcf', component_property='value'),
     Input(component_id='scalecf', component_property='value'),
    ],

)


def update_cf(cc11,cc12,cc44,ms,kk1,kk2,bb1,bb2,hx,hy,hz,rho,nn,sol,s):

    delta=0.0*10.0**(-5)
    mu0 = 4.0*np.pi*10.0**(-7)
    ms = ms/mu0
    k1 = kk1*10.0**6  #J/m^3
    k2 = kk2*10.0**6  #J/m^3
    b1 = bb1*10.0**6  # Pa
    b2 = bb2*10.0**6  # Pa
  #  dk1 = ((b1**2)/(c11 - c12)) - ((b2**2)/(2.0*c44))
  #  k1eff = (k1 + dk1)
    
    hx=hx+delta
    hy=hy+delta
    hz=hz+delta
    
    a = [hx,hy,hz,ms,k1,k2]  
  
    x0 = minimize(enecub,np.array([0.2,0.3]),args=(a),method='Nelder-Mead',options={'maxiter': 1000, 'maxfev': 1000, 'disp': True, 'xatol': 0.0000001})

    xx=float(x0.x[0])
    yy=float(x0.x[1])
    
    ett0=ett(xx,yy,hx,hy,hz,ms,k1,k2)
    epp0=epp(xx,yy,hx,hy,hz,ms,k1,k2)
    
    chizz= (ms**2*np.sin(xx)**2)/ett0
    chiyz= -(ms**2*np.sin(xx)*np.cos(xx)*np.sin(yy))/(ett0)
    chixz= -(ms**2*np.sin(xx)*np.cos(xx)*np.cos(yy))/(ett0)
    chiyy= ms**2*(((np.cos(xx)**2*np.sin(yy)**2)/ett0) + ((np.sin(xx)**2*np.cos(yy)**2)/epp0))
    chixx= ms**2*(((np.cos(xx)**2*np.cos(yy)**2)/ett0) + ((np.sin(xx)**2*np.sin(yy)**2)/epp0))
    chixy= -ms**2*(((np.cos(xx)**2*np.cos(yy)*np.sin(yy))/ett0) - ((np.sin(xx)**2*np.cos(yy)*np.sin(yy))/epp0))
    
    
    ax= np.sin(xx)*np.cos(yy)
    ay= np.sin(xx)*np.sin(yy)
    az= np.cos(xx)
    
    dc11= -(b1/ms)**2*(4.0*chixx*ax**2)  #Pa
    dc12= -(b1/ms)**2*(4.0*chixy*ax*ay)
    dc22= -(b1/ms)**2*(4.0*chiyy*ay**2)
    dc33= -(b1/ms)**2*(4.0*chizz*az**2)
    dc44= -(b2/ms)**2*(chizz*ay**2 + 2.0*chiyz*ay*az + chiyy*az**2)
    dc55= -(b2/ms)**2*(chixx*az**2 + chizz*ax**2 + 2.0*chixz*ax*az)
    dc66= -(b2/ms)**2*(chixx*ay**2 + chiyy*ax**2 + 2.0*chixy*ax*ay)
    dc13= -(b1/ms)**2*(4.0*chixz*ax*az)
    dc23= -(b1/ms)**2*(4.0*chiyz*ay*az)
    dc14= -((2.0*b1*b2)/(ms**2))*(chixy*ax*az + chixz*ax*ay)
    dc15= -((2.0*b1*b2)/(ms**2))*(chixx*ax*az + chixz*ax*ax)
    dc16= -((2.0*b1*b2)/(ms**2))*(chixx*ax*ay + chixy*ax*ax)
    dc24= -((2.0*b1*b2)/(ms**2))*(chiyy*ay*az + chiyz*ay*ay)
    dc25= -((2.0*b1*b2)/(ms**2))*(chixy*ay*az + chiyz*ax*ay)
    dc26= -((2.0*b1*b2)/(ms**2))*(chixy*ay*ay + chiyy*ax*ay)
    dc34= -((2.0*b1*b2)/(ms**2))*(chiyz*az*az + chizz*az*ay)
    dc35= -((2.0*b1*b2)/(ms**2))*(chixz*az*az + chizz*ax*az)
    dc36= -((2.0*b1*b2)/(ms**2))*(chixz*ay*az + chiyz*ax*az)
    dc45= -(b2/ms)**2*(chixy*az**2 + chixz*ay*az + chiyz*ax*az + chizz*ax*ay)
    dc46= -(b2/ms)**2*(chixy*ay*az + chixz*ay*ay + chiyy*ax*az + chiyz*ax*ay)
    dc56= -(b2/ms)**2*(chixx*ay*az + chixy*ax*az + chixz*ax*ay + chiyz*ax*ax)

    
    n=int(np.sqrt(nn))
    
    aa=complex(0,n)
    
    a11=(cc11*10**9/rho)+(dc11/rho)
    a12=(cc12*10**9/rho)+(dc12/rho)
    a13=(cc12*10**9/rho)+(dc13/rho)
    a14=(0.0*10**9/rho)+(dc14/rho)
    a15=(0.0*10**9/rho)+(dc15/rho)
    a16=(0.0*10**9/rho)+(dc16/rho)
    a22=(cc11*10**9/rho)+(dc22/rho)
    a23=(cc12*10**9/rho)+(dc23/rho)
    a24=(0.0*10**9/rho)+(dc24/rho)
    a25=(0.0*10**9/rho)+(dc25/rho)
    a26=(0.0*10**9/rho)+(dc26/rho)
    a33=(cc11*10**9/rho)+(dc33/rho)
    a34=(0.0*10**9/rho)+(dc34/rho)
    a35=(0.0*10**9/rho)+(dc35/rho)
    a36=(0.0*10**9/rho)+(dc36/rho)
    a44=(cc44*10**9/rho)+(dc44/rho)
    a45=(0.0*10**9/rho)+(dc45/rho)
    a46=(0.0*10**9/rho)+(dc46/rho)
    a55=(cc44*10**9/rho)+(dc55/rho)
    a56=(0.0*10**9/rho)+(dc56/rho)
    a66=(cc44*10**9/rho)+(dc66/rho)
    
    a011=cc11*10**9/rho
    a012=cc12*10**9/rho
    a013=cc12*10**9/rho
    a014=0.0*10**9/rho
    a015=0.0*10**9/rho
    a016=0.0*10**9/rho
    a022=cc11*10**9/rho
    a023=cc12*10**9/rho
    a024=0.0*10**9/rho
    a025=0.0*10**9/rho
    a026=0.0*10**9/rho
    a033=cc11*10**9/rho
    a034=0.0*10**9/rho
    a035=0.0*10**9/rho
    a036=0.0*10**9/rho
    a044=cc44*10**9/rho
    a045=0.0*10**9/rho
    a046=0.0*10**9/rho
    a055=cc44*10**9/rho
    a056=0.0*10**9/rho
    a066=cc44*10**9/rho
    
    u, v = np.mgrid[0:np.pi:aa, 0:2*np.pi:aa]
    kkx = np.sin(u)*np.cos(v)
    kky = np.sin(u)*np.sin(v)
    kkz = np.cos(u)
    
    
    vx0=np.zeros((n,n))
    vy0=np.zeros((n,n))
    vz0=np.zeros((n,n))
    v0=np.zeros((n,n))
    
    vx00=np.zeros((n,n))
    vy00=np.zeros((n,n))
    vz00=np.zeros((n,n))
    v00=np.zeros((n,n))
    
    v000=np.zeros((n,n))
    
    
    
    for ii in range(0, n):
  
      for jj in range(0, n):
    
        kx=kkx[ii,jj]
        ky=kky[ii,jj]
        kz=kkz[ii,jj]
        
        vvx,vvy,vvz = vel(a11,a12,a13,a14,a15,a16,a22,a23,a24,a25,a26,a33,a34,a35,a36,a44,a45,a46,a55,a56,a66,kx,ky,kz,sol)
        
        vvvx,vvvy,vvvz = vel(a011,a012,a013,a014,a015,a016,a022,a023,a024,a025,a026,a033,a034,a035,a036,a044,a045,a046,a055,a056,a066,kx,ky,kz,sol)
    
        vx0[ii,jj]=vvx
        vy0[ii,jj]=vvy
        vz0[ii,jj]=vvz
        v0[ii,jj]=np.sqrt(vx0[ii,jj]**2+vy0[ii,jj]**2+vz0[ii,jj]**2)
        
        vx00[ii,jj]=vvvx
        vy00[ii,jj]=vvvy
        vz00[ii,jj]=vvvz
        v00[ii,jj]=np.sqrt(vx00[ii,jj]**2+vy00[ii,jj]**2+vz00[ii,jj]**2)
        
        v000[ii,jj]=(v0[ii,jj]-v00[ii,jj])/v00[ii,jj]
    

    
    
    x = (1.0+s*v000)*kkx
    y = (1.0+s*v000)*kky
    z = (1.0+s*v000)*kkz


    list00 = np.stack((np.transpose(x),np.transpose(y),np.transpose(z),np.transpose(v000)),axis=0)
    list0 = np.stack((v000,kkx,kky,kkz,u*(180.0/np.pi),v*(180.0/np.pi)),axis=-1)



    fig = make_subplots(rows=1, cols=1,
                    specs=[[{'is_3d': True}]],
                    subplot_titles=['  Color corresponds to the magnitude of fractional change in sound velocity (group velocity) (v-v0)/v0 '])


    fig.add_trace(go.Surface(x=list00[0], y=list00[1], z=list00[2], surfacecolor=list00[3], customdata=list0, name=" ", hoverinfo="name",
                                 hovertemplate = """(v-v0)/v0 = %{customdata[0]:.6g}<br>nx = kx/k = %{customdata[1]:.6g}<br>ny = ky/k = %{customdata[2]:.6g}<br>nz = kz/k = %{customdata[3]:.6g}<br>θ = %{customdata[4]:.6g}°<br>φ = %{customdata[5]:.6g}°<br>"""),1, 1)


    fig.update_layout(transition_duration=500)

    fig.update_layout(
        scene = {
            "xaxis": {"showticklabels": False},
            "yaxis": {"showticklabels": False},
            "zaxis": {"showticklabels": False}
        })
        
    fig.update_layout(
        scene = {
            "xaxis": {"title": "nx"},
            "yaxis": {"title": "ny"},
            "zaxis": {"title": "nz"}
        })
    

    
  #  stat = 'The figure has been generated successfully!'
    
    return fig



############## hex_field_3D_plot

@app.callback(
    Output('output_hf', 'figure'),
    [Input(component_id='c11hf', component_property='value'),
     Input(component_id='c12hf', component_property='value'),
     Input(component_id='c13hf', component_property='value'),
     Input(component_id='c33hf', component_property='value'),
     Input(component_id='c44hf', component_property='value'),
     Input(component_id='mshf', component_property='value'),
     Input(component_id='k1hf', component_property='value'),
     Input(component_id='k2hf', component_property='value'),
     Input(component_id='b21hf', component_property='value'),
     Input(component_id='b22hf', component_property='value'),
     Input(component_id='b3hf', component_property='value'),
     Input(component_id='b4hf', component_property='value'),
     Input(component_id='hxhf', component_property='value'),
     Input(component_id='hyhf', component_property='value'),
     Input(component_id='hzhf', component_property='value'),
     Input(component_id='rhohf', component_property='value'),
     Input(component_id='nhf', component_property='value'),
     Input(component_id='solhf', component_property='value'),
     Input(component_id='scalehf', component_property='value'),
    ],

)


def update_hf(cc11,cc12,cc13,cc33,cc44,ms,kk1,kk2,bb21,bb22,bb3,bb4,hx,hy,hz,rho,nn,sol,s):

    delta=0.0*10.0**(-5)
    mu0 = 4.0*np.pi*10.0**(-7)
    ms = ms/mu0
    k1 = kk1*10.0**6  #J/m^3
    k2 = kk2*10.0**6  #J/m^3
    b21 = bb21*10.0**6  # Pa
    b22 = bb22*10.0**6  # Pa
    b3 = bb3*10.0**6  # Pa
    b4 = bb4*10.0**6  # Pa
    
    hx=hx+delta
    hy=hy+delta
    hz=hz+delta
    
    a = [hx,hy,hz,ms,k1,k2]  
  
    x0 = minimize(enehex,np.array([0.2,0.3]),args=(a),method='Nelder-Mead',options={'maxiter': 1000, 'maxfev': 1000, 'disp': True, 'xatol': 0.0000001})

    xx=float(x0.x[0])
    yy=float(x0.x[1])
    
    ett0=etth(xx,yy,hx,hy,hz,ms,k1,k2)
    epp0=epph(xx,yy,hx,hy,hz,ms,k1,k2)
    
    chizz= (ms**2*np.sin(xx)**2)/ett0
    chiyz= -(ms**2*np.sin(xx)*np.cos(xx)*np.sin(yy))/(ett0)
    chixz= -(ms**2*np.sin(xx)*np.cos(xx)*np.cos(yy))/(ett0)
    chiyy= ms**2*(((np.cos(xx)**2*np.sin(yy)**2)/ett0) + ((np.sin(xx)**2*np.cos(yy)**2)/epp0))
    chixx= ms**2*(((np.cos(xx)**2*np.cos(yy)**2)/ett0) + ((np.sin(xx)**2*np.sin(yy)**2)/epp0))
    chixy= -ms**2*(((np.cos(xx)**2*np.cos(yy)*np.sin(yy))/ett0) - ((np.sin(xx)**2*np.cos(yy)*np.sin(yy))/epp0))
    
    
    ax= np.sin(xx)*np.cos(yy)
    ay= np.sin(xx)*np.sin(yy)
    az= np.cos(xx)
    
    dc11= (1.0/ms)**2*(-b3**2*(chixx*ax**2+chiyy*ay**2-chixy*ax*ay)+2.0*b21*b3*az*(chiyz*ay-chixz*ax)-chizz*4.0*b21**2*az**2)  #Pa
    dc22= (1.0/ms)**2*(-b3**2*(chixx*ax**2+chiyy*ay**2-chixy*ax*ay)-2.0*b21*b3*az*(chiyz*ay-chixz*ax)-chizz*4.0*b21**2*az**2) 
    dc33= -(b22/ms)**2*(4.0*chizz*az**2)
    dc44= -(b4/ms)**2*(chizz*ay**2 + chiyz*ay*az + chiyy*az**2)
    dc55= -(b4/ms)**2*(chixx*az**2 + chizz*ax**2 + chixz*ax*az)
    dc66= -(b3/ms)**2*(chixx*ay**2 + chiyy*ax**2 + chixy*ax*ay)
    dc12= (1.0/ms)**2*(b3**2*(chixx*ax**2+chiyy*ay**2-chixy*ax*ay)-4.0*b21**2*az**2*chizz)
    dc13= (1.0/ms)**2*(-b22*b3*(chixz*ax*az-chiyz*ay*az)-4.0*chizz*b21*b22*az**2)
    dc14= -(1.0/ms)**2*(0.5*b4)*(b3*(-2.0*chiyy*ay*az+chixy*ax*az+chixz*ax*ay-chiyz*ay**2)+b21*(4.0*chizz*ay*az+2.0*chiyz*az**2))
    dc15= -(1.0/ms)**2*(0.5*b4)*(b3*(2.0*chixx*ax*az-chixy*ay*az-chiyz*ax*ay+chixz*ax**2)+b21*(4.0*chizz*ax*az+2.0*chixz*az**2))
    dc16= -(1.0/ms)**2*(0.5*b3)*(2.0*b3*ax*ay*(chixx-chiyy)+b3*chixy*(ax**2-ay**2)+2.0*b21*az*(ay*chixz+ax*chiyz))
    dc23= (1.0/ms)**2*(b3*b22*az*(ax*chixz-ay*chiyz)-4.0*b21*b22*az**2*chizz)
    dc24= -(1.0/ms)**2*(0.5*b4)*(b3*(2.0*chiyy*ay*az-chixy*ax*az-chixz*ax*ay+chiyz*ay**2)+b21*(4.0*chizz*ay*az+2.0*chiyz*az**2))
    dc25= -(1.0/ms)**2*(0.5*b4)*(b3*(-2.0*chixx*ax*az+chixy*ay*az-chixz*ax**2+chiyz*ax*ay)+b21*(4.0*chizz*ax*az+2.0*chixz*az**2))
    dc26= -(1.0/ms)**2*(0.5*b4)*(b3*(-2.0*chixx*ay*ax+2.0*chiyy*ax*ay+chixy*ay*ay-chixy*ax**2)+b21*(2.0*chixz*ay*az+2.0*chiyz*az*ax))
    dc34= -((b22*b4)/(ms**2))*az*(2.0*chizz*ay + az*chiyz)
    dc35= -((b22*b4)/(ms**2))*az*(2.0*chizz*ax + az*chixz)
    dc36= -((b22*b3)/(ms**2))*az*(chixz*ay + ax*chiyz)
    dc45= -0.5*(b4/ms)**2*(chixy*az**2 + chixz*ay*az + chiyz*ax*az + 2.0*chizz*ax*ay)
    dc46= -0.5*(1.0/ms)**2*b3*b4*(chixy*ay*az + chixz*ay*ay + 2.0*chiyy*ax*az + chiyz*ax*ay)
    dc56= -0.5*(1.0/ms)**2*b3*b4*(2.0*chixx*ay*az + chixy*ax*az + chixz*ax*ay + chiyz*ax*ax)

    
    n=int(np.sqrt(nn))
    
    aa=complex(0,n)
    
    a11=(cc11*10**9/rho)+(dc11/rho)
    a12=(cc12*10**9/rho)+(dc12/rho)
    a13=(cc13*10**9/rho)+(dc13/rho)
    a14=(0.0*10**9/rho)+(dc14/rho)
    a15=(0.0*10**9/rho)+(dc15/rho)
    a16=(0.0*10**9/rho)+(dc16/rho)
    a22=(cc11*10**9/rho)+(dc22/rho)
    a23=(cc13*10**9/rho)+(dc23/rho)
    a24=(0.0*10**9/rho)+(dc24/rho)
    a25=(0.0*10**9/rho)+(dc25/rho)
    a26=(0.0*10**9/rho)+(dc26/rho)
    a33=(cc33*10**9/rho)+(dc33/rho)
    a34=(0.0*10**9/rho)+(dc34/rho)
    a35=(0.0*10**9/rho)+(dc35/rho)
    a36=(0.0*10**9/rho)+(dc36/rho)
    a44=(cc44*10**9/rho)+(dc44/rho)
    a45=(0.0*10**9/rho)+(dc45/rho)
    a46=(0.0*10**9/rho)+(dc46/rho)
    a55=(cc44*10**9/rho)+(dc55/rho)
    a56=(0.0*10**9/rho)+(dc56/rho)
    a66=(0.5*(cc11-cc12)*10**9/rho)+(dc66/rho)
    
    a011=(cc11*10**9/rho)
    a012=(cc12*10**9/rho)
    a013=(cc13*10**9/rho)
    a014=(0.0*10**9/rho)
    a015=(0.0*10**9/rho)
    a016=(0.0*10**9/rho)
    a022=(cc11*10**9/rho)
    a023=(cc13*10**9/rho)
    a024=(0.0*10**9/rho)
    a025=(0.0*10**9/rho)
    a026=(0.0*10**9/rho)
    a033=(cc33*10**9/rho)
    a034=(0.0*10**9/rho)
    a035=(0.0*10**9/rho)
    a036=(0.0*10**9/rho)
    a044=(cc44*10**9/rho)
    a045=(0.0*10**9/rho)
    a046=(0.0*10**9/rho)
    a055=(cc44*10**9/rho)
    a056=(0.0*10**9/rho)
    a066=(0.5*(cc11-cc12)*10**9/rho)
    
    u, v = np.mgrid[0:np.pi:aa, 0:2*np.pi:aa]
    kkx = np.sin(u)*np.cos(v)
    kky = np.sin(u)*np.sin(v)
    kkz = np.cos(u)
    
    
    vx0=np.zeros((n,n))
    vy0=np.zeros((n,n))
    vz0=np.zeros((n,n))
    v0=np.zeros((n,n))
    
    vx00=np.zeros((n,n))
    vy00=np.zeros((n,n))
    vz00=np.zeros((n,n))
    v00=np.zeros((n,n))
    
    v000=np.zeros((n,n))
    
    
    
    for ii in range(0, n):
  
      for jj in range(0, n):
    
        kx=kkx[ii,jj]
        ky=kky[ii,jj]
        kz=kkz[ii,jj]
        
        vvx,vvy,vvz = vel(a11,a12,a13,a14,a15,a16,a22,a23,a24,a25,a26,a33,a34,a35,a36,a44,a45,a46,a55,a56,a66,kx,ky,kz,sol)
        
        vvvx,vvvy,vvvz = vel(a011,a012,a013,a014,a015,a016,a022,a023,a024,a025,a026,a033,a034,a035,a036,a044,a045,a046,a055,a056,a066,kx,ky,kz,sol)
    
        vx0[ii,jj]=vvx
        vy0[ii,jj]=vvy
        vz0[ii,jj]=vvz
        v0[ii,jj]=np.sqrt(vx0[ii,jj]**2+vy0[ii,jj]**2+vz0[ii,jj]**2)
        
        vx00[ii,jj]=vvvx
        vy00[ii,jj]=vvvy
        vz00[ii,jj]=vvvz
        v00[ii,jj]=np.sqrt(vx00[ii,jj]**2+vy00[ii,jj]**2+vz00[ii,jj]**2)
        
        v000[ii,jj]=(v0[ii,jj]-v00[ii,jj])/v00[ii,jj]
    

    
    
    x = (1.0+s*v000)*kkx
    y = (1.0+s*v000)*kky
    z = (1.0+s*v000)*kkz


    list00 = np.stack((np.transpose(x),np.transpose(y),np.transpose(z),np.transpose(v000)),axis=0)
    list0 = np.stack((v000,kkx,kky,kkz,u*(180.0/np.pi),v*(180.0/np.pi)),axis=-1)



    fig = make_subplots(rows=1, cols=1,
                    specs=[[{'is_3d': True}]],
                    subplot_titles=['  Color corresponds to the magnitude of fractional change in sound velocity (group velocity) (v-v0)/v0 '])


    fig.add_trace(go.Surface(x=list00[0], y=list00[1], z=list00[2], surfacecolor=list00[3], customdata=list0, name=" ", hoverinfo="name",
                                 hovertemplate = """(v-v0)/v0 = %{customdata[0]:.6g}<br>nx = kx/k = %{customdata[1]:.6g}<br>ny = ky/k = %{customdata[2]:.6g}<br>nz = kz/k = %{customdata[3]:.6g}<br>θ = %{customdata[4]:.6g}°<br>φ = %{customdata[5]:.6g}°<br>"""),1, 1)


    fig.update_layout(transition_duration=500)

    fig.update_layout(
        scene = {
            "xaxis": {"showticklabels": False},
            "yaxis": {"showticklabels": False},
            "zaxis": {"showticklabels": False}
        })
        
    fig.update_layout(
        scene = {
            "xaxis": {"title": "nx"},
            "yaxis": {"title": "ny"},
            "zaxis": {"title": "nz"}
        })
    

    
  #  stat = 'The figure has been generated successfully!'
    
    return fig



if __name__ == '__main__':
        app.run_server(debug=True)
