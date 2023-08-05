# ruxitools

Miscellaneous tools.

# Installation

method1:
    
    pip install -e git+https://github.com/ruxi/tools.git
 
method2:
    git clone https://github.com/ruxi/tools.git
    cd tools
    python setup.py install
    python setup.py tests
    

# Modules

## XyDB: a container for intermediate data
    
XyDB is used to organize intermediate data by attaching it to the source dataset. 
It solves the problem of namespace pollution, especially if many intermediate
datasets are derived from the source.
    
Usage:
        
    ```python

    from ruxitools.xydb import XyDB

    # attach container to source data
    mydata.Xy = XyDB()

    # store intermediate info & documentation into the containers
    mydata.Xy.push(dict(
                            key="config1"           # keyword
                          , X=[mydata*2]            # intermediate data
                          , desc = "multiply by 2"  # description of operation
                  ))

    # To retrieve intermediate data as a dict:
    mydata.Xy.pull.config1 

    # To retrieve intermediate data as attributes:
    mydata.Xy.show.config1.desc

    # To show keys
    mydata.Xy.keys
    ```

# TODO:

 requirements.txt - not sure if it works
 