![](https://bitbucket.org/batterio/regulome_web/raw/master/regulome_app/webapp/static/images/regulome_logo.jpg)

This repository contains the code of the Islet Regulome Browser.
The Islet Regulome Browser is a visualization tool that enables viewing 
of human islet TF bindings, human islet open chromatin states, clusters 
of enhancers, islet motifs, and DIAGRAM type2 diabetes association 
p-values as well as MAGIC fasting glycemia p-values at desired levels of 
resolution throughout the genome. In addition to these standard tracks, 
it is also possible for users to upload their own variants or regions 
sets for temporary display.


## Islet regulome dependencies  
* [Python 3.5](https://www.python.org/) and newer with the following packages:
    * Flask  
    * Click  
    * pandoc (optional)
    * Optional modules that will probably be used in the future are:  
        * intervaltree
        * SQLAlchemy
	    * Flask-SQLAlchemy
        * matplotlib
* [R](https://www.r-project.org/)
* [ImageMagick](http://www.imagemagick.org/)
    

## Islet regulome data sources  
Since the data sources are large files (~ 8Gb) contact the author (info@isletregulome.com) to download them.  


## How to install the regulome
The regulome browser can be installed with various approaches:  

  
### Through PyPI (recommended)  
    pip install regulome_web  
    

### Through the source package  
    pip install regulome_web-2.0.tar.gz  
Put, if necessary, the correct version of the program in the name of the package  
    
    
### By cloning the repository:  
* Clone the regulome repository:  
    `git clone git@bitbucket.org:batterio/regulome_web.git`  
* Install the package:  
    `pip install -e .`  
        *or*  
    `python setup.py`  
      
      
## How to run the regulome_web 
First, install the regulome_web as described above. Then write `regulome_web --help`
to obtain some basic information about the usage of the regulome_web.
Once the package is installed, create the required structure by executing
`regulome_web init`. This command will create a structure of folders as
well as a `regulome.cfg` configuration file. Configure the configuration
file and then run the regulome_web by executing `regulome_web start`.
This will start a local web server on `http://127.0.0.1:5000/`. To deploy the
regulome_web with a web service such as Apache, use the `regulome.wsgi`
file instead. In order to be used in production the regulome_web should 
be configured with a secure `secret_key` (to be set in the `regulome.cfg` 
configuration file) and the `deploy_mode` section of the `regulome.cfg` file
should be set to `production`.


## Description of the `regulome.cfg` configuration file
The `regulome.cfg` configuration file is composed of 7 fields, denoted by square brackets:  

* **binaries**: contains two variables:
	* **Rscript_bin**: path of the R binary
	* **imagemagick**: path of the imagemagick convert tool

* **working_directory**: contains one variable:
	* **cwd**: current working directory. This field is set automatically by the program when `regulome_web init` is executed

* **data**: contains two variables:
	* **data**: path of the data used by the R script to generate the plot. By default the program searches for the folder `data` in the current working directory (see above)
	* **uploads**: path where the files uploaded by the users are stored. By default the program searches for the folder `data/uploads` in the current working directory (see above)

* **output**: contains one variable:
	* **cache**: path where the results of the program (plots and tables) will be saved. By default the program searches for the folder `output` in the current working directory (see above). The default folder will be created, if not existing, when `regulome_web init` is executed

* **logs**: contains 4 variables:
	* **log_folder**: path where the logs of the program are written. By default the program searches for the folder `logs` in the current woring directory (seea bove). The default folder will be created, if not existing, when `regulome_web init` is executed
	* **activity_log**: path of the `activity.log` file. By default this file is placed inside `log_folder`
	* **regulome_log**: path of the `regulome.log` file. By default this file is placed inside `log_folder`
	* **log_level**: level of log verbosity: can be: notset, debug, info, warning, error, critical. By default log_level is set to info

* **deploy_mode**: contains one variable:
	* **configuration**: mode of deploy of the `regulome_web` program. Can be development, testing, production. By default cofiguration is set to development

* **secret_key**: contains one variable:
	* **key**: key used to encrypt the session coockies. Make sure to keep the key secret.

