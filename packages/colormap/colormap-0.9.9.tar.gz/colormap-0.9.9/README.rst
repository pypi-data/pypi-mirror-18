#############################
COLORMAP documentation
#############################

.. image:: https://badge.fury.io/py/colormap.svg
    :target: https://pypi.python.org/pypi/colormap

.. image:: https://secure.travis-ci.org/cokelaer/colormap.png
    :target: http://travis-ci.org/cokelaer/colormap

.. image:: https://coveralls.io/repos/cokelaer/colormap/badge.png?branch=master 
    :target: https://coveralls.io/r/cokelaer/colormap?branch=master 

.. image:: https://landscape.io/github/cokelaer/colormap/master/landscape.png
    :target: https://landscape.io/github/cokelaer/colormap/master

.. image:: https://badge.waffle.io/cokelaer/colormap.png?label=ready&title=Ready 
    :target: https://waffle.io/cokelaer/colormap


:version: Python 2.7, 3.3, 3.4, 3.5
:contributions: Please join https://github.com/cokelaer/colormap
:issues: Please use https://github.com/cokelaer/colormap/issues
:notebook: Please see https://github.com/cokelaer/colormap/tree/master/notebooks

What is it ?
################

**colormap** package provides simple utilities to convert colors between
RGB, HEX, HLS, HUV and a class to easily build colormaps for matplotlib. All
matplotlib colormaps and some R colormaps are available altogether. The
plot_colormap method (see below) is handy to quickly pick up a colormaps and
the test_colormap is useful to see test a new colormap.


Installation
###################

::

    pip install colormap

Example
##########

* Create your own colormap from red to green colors with intermediate color as
  whitish (diverging map from red to green)::

      c = Colormap()
      mycmap = c.cmap( {'red':[1,1,0], 'green':[0,1,.39], 'blue':[0,1,0]})
      cmap = c.test_colormap(mycmap)

* Even simpler if the colormap is linear::

      c = Colormap()
      mycmap = c.cmap_linear('red', 'black', 'green')
      cmap = c.test_colormap(mycmap)

.. image:: http://pythonhosted.org//colormap/_images/example.png
    :width: 50%
    :align: center
    
* check out the available colormaps::

      c = Colormap()
      c.plot_colormap('diverging')

.. image:: http://pythonhosted.org//colormap/_images/colormaps.png
    :width: 50%
    :align: center

See online documentation for details: http://pythonhosted.org//colormap/
