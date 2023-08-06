__author__ = 'Loris Mularoni'


# Import modules
import os
import logging
import configparser


# Path of the R script to create the plot
REGULOME_R_SCRIPT = os.path.join(os.path.dirname(__file__), 'regulome_plot', 'plot_IRB_main.R')


# Read the configuration file. It creates is if it does not exist.
configs = configparser.ConfigParser()
configs._interpolation = configparser.ExtendedInterpolation()
_ = configs.read(os.path.join(os.getcwd(), 'regulome.cfg'))


class Config:
    SECRET_KEY = configs['secret_key']['key']
    UPLOAD_FOLDER = configs['data']['uploads']
    # Maximum dimension of the uploaded file. If a larger file is transmitted,
    # Flask will raise an RequestEntityTooLarge exception.
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50Mb.
    # SQLALCHEMY_DATABASE_URI = configs['databases']['genes']
    # SQLALCHEMY_BINDS = {
    #     'regions': configs['databases']['regions'],
    #     'tfbs': configs['databases']['tfbs']
    # }
    # SQLALCHEMY_TRACK_MODIFICATIONS = True


class Development(Config):
    DEBUG = True


class Testing(Config):
    TESTING = True


class Production(Config):
    DEBUG = False


web_configuration = {
    'development': Development,
    'testing': Testing,
    'production': Production,
    'default': Development
}


# Logger
# Set the verbosity of the logger. Levels are:
# critical 50
# error	 40
# warning	 30
# info	 20
# debug	 10
# notset	 0

levels = {
    'critical': logging.CRITICAL,
    'error': logging.ERROR,
    'warning': logging.WARNING,
    'info': logging.INFO,
    'debug': logging.DEBUG,
    'notset': logging.NOTSET
}

# Set the logger
logger = logging.getLogger(__name__)
logger.setLevel(levels.get(configs['logs']['log_level'], logging.INFO))
formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s', datefmt='%H:%M')

# File handler
fh = logging.FileHandler(configs['logs']['regulome_log'])
fh.setLevel(levels.get(configs['logs']['log_level'], logging.INFO))
fh.setFormatter(formatter)
logger.addHandler(fh)

# Stdout handler
ch = logging.StreamHandler()
ch.setLevel(levels.get(configs['logs']['log_level'], logging.INFO))
ch.setFormatter(formatter)
logger.addHandler(ch)
