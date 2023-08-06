#!/usr/bin/env python

### setup.py

#from distutils.core import setup

from setuptools import setup, find_packages
import sys, os

setup(name='NonlinearLeastSquares',
      version='1.1.1',
      author='Avinash Kak',
      author_email='kak@purdue.edu',
      maintainer='Avinash Kak',
      maintainer_email='kak@purdue.edu',
      url='https://engineering.purdue.edu/kak/distNonlinearLeastSquares/NonlinearLeastSquares-1.1.1.html',
      download_url='https://engineering.purdue.edu/kak/distNonlinearLeastSquares/NonlinearLeastSquares-1.1.1.tar.gz#md5=9ede50a98a7fbce5e2d588ea69e10258',
      description='A Python module for solving optimization problems with nonlinear least-squares',
      long_description=''' 

Consult the module API page at 

      https://engineering.purdue.edu/kak/distNonlinearLeastSquares/NonlinearLeastSquares-1.1.1.html

for all information related to this module, including
information regarding the latest changes to the code. The
page at the URL shown above lists all of the module
functionality you can invoke in your own code.  

With regard to the basic purpose of this module, it provides
a domain agnostic implementation of nonlinear least-squares
algorithms (gradient-descent and Levenberg-Marquardt) for
fitting a model to observed data.  Typically, a model
involves several parameters and each observed data element
can be expressed as a function of those parameters plus
noise.  The goal of nonlinear least-squares is to estimate
the best values for the parameters given all of the observed
data.  In order to illustrate how to use the
NonlinearLeastSquares class, the module also comes with
another class, OptimizeSurfaceFit, whose job is to fit the
best surface to noisy height data over an XY-plane. The
model in this case would be an analytical expression for the
height surface and the goal of nonlinear least-squares would
be to estimate the best values for the parameters in the
model.

Typical usage syntax for invoking the domain-agnostic
NonlinearLeastSquares through your own domain-specific class
such as OptimizeSurfaceFit is shown below:

::

        optimizer =  NonlinearLeastSquares(                                            
                         max_iterations = 200,
                         delta_for_jacobian = 0.000001,
                         delta_for_step_size = 0.0001,
                     )
    
        surface_fitter = OptimizeSurfaceFit(                                           
                             gen_data_synthetically = True,
                             datagen_functional = "7.8*(x - 0.5)**4 + 2.2*(y - 0.5)**2",
                             data_dimensions = (16,16), 
                             how_much_noise_for_synthetic_data = 0.3, 
                             model_functional = "a*(x-b)**4 + c*(y-d)**2",
                             initial_param_values = {'a':2.0, 'b':0.4, 'c':0.8, 'd':0.4},
                             display_needed = True,
                             debug = True,
                         )

        surface_fitter.set_constructor_options_for_optimizer(optimizer)                

        result = surface_fitter.calculate_best_fitting_surface('lm')                             

        or 

        result = surface_fitter.calculate_best_fitting_surface('gd')                             

          ''',

      license='Python Software Foundation License',
      keywords='gradient descent, nonlinear least-squares, optimization',
      platforms='All platforms',
      classifiers=['Topic :: Scientific/Engineering :: Information Analysis', 'Programming Language :: Python :: 2.7', 'Programming Language :: Python :: 3.5'],
      packages=['NonlinearLeastSquares','OptimizeSurfaceFit']
)
