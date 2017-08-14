import requests

links = ['https://github.com/kwmsmith/scipy-2017-cython-tutorial',
         'https://github.com/gforsyth/numba_tutorial_scipy2017',
         'https://github.com/sympy/scipy-2017-codegen-tutorial',
         'https://github.com/mmckerns/tutmom',
         'https://github.com/AllenDowney/CompStats',
         'https://github.com/mwcraig/scipy2017-jupyter-widgets-tutorial',
         'https://github.com/tomkooij/scipy2017',
         'https://github.com/ioam/scipy-2017-holoviews-tutorial',
         'https://github.com/enthought/Numpy-Tutorial-SciPyConf-2017',
         'https://github.com/chendaniely/pandas_for_everyone',
         'https://github.com/amueller/scipy-2017-sklearn',
         'https://github.com/dask/dask-tutorial',
         'https://github.com/pydata/parallel-tutorial',
         'https://github.com/WeatherGod/AnatomyOfMatplotlib',
         'https://github.com/scikit-image/skimage-tutorials',
         'https://github.com/ericmjl/Network-Analysis-Made-Simple',
         'https://github.com/mwickert/SP-Comm-Tutorial-using-scikit-dsp-comm']

titles = ['Cython for Data, Scientists, and Data Scientists (Intermediate-Advanced)',
          'Numba - Tell Those C_plusplus Bullies to Get Lost (Intermediate)',
          'Automatic Code Generation with SymPy (Advanced)',
          'Modern Optimization Methods in Python (Intermediate-Advanced)',
          'Computational Statistics (Beginner)',
          'The Jupyter Interactive Widget Ecosystem (Intermediate-Advanced)',
          'HDF5 take 2 - h5py and PyTables (Intermediate-Advanced)',
          'Interactive Data Visualization with HoloViews and Bokeh (Advanced)',
          'Introduction to Numerical Computing with NumPy (Beginner)',
          'Pandas for Data Analysis (Beginner)',
          'Machine Learning with scikit-learn Part One (Intermediate)',
          'Parallelizing Scientific Python with Dask (Intermediate)',
          'Parallel Data Analysis in Python (Intermediate)',
          'Anatomy of Matplotlib (Beginner)',
          'scikit-image - Image Processing for Python (Intermediate)',
          'Network Science and Statistics - Fundamentals and Applications (Intermediate)',
          'Signal Processing and Communications Hands-On Using scikit-dsp-comm (Intermediate)']

for link, fname in zip(links, titles):
    with open(fname+'.zip', 'wb') as fp:
        res = requests.get(link+'/archive/master.zip', stream=True)
        for chunk in res.iter_content(chunk_size=1024):
            if chunk:
                fp.write(chunk)
    print('Completed: {}'.format(fname+'.zip'))
