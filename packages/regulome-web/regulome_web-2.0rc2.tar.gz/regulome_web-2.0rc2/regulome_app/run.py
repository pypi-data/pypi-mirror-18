# Import modules
import os
import click
import configparser
import shutil
from regulome_app.webapp.models import BUILDS, REGIONS, TFBS, SNPS, CHROMATIN


class CheckStructure:
    """Check and create the structure of the regulome browser"""
    def __init__(self):
        self.configs = None
        self.check_config_file()
        self.create_cache_structure()
        self.create_log_structure()

    def check_config_file(self):
        """Read the configuration file. It creates it if it does not exist."""
        self.configs = configparser.ConfigParser()
        self.configs._interpolation = configparser.ExtendedInterpolation()

        cwd = os.getcwd()

        # Check for the existence of the regulome.cfg file.
        if not os.path.exists(os.path.join(cwd, 'regulome.cfg')):
            # Copy the template
            shutil.copyfile(
                os.path.join(os.path.dirname(__file__), 'regulome.cfg.template'),
                os.path.join(cwd, 'regulome.cfg')
            )

            # Set the section [working_directory] to the current working directory
            _ = self.configs.read(os.path.join(cwd, 'regulome.cfg'))
            self.configs.set('working_directory', 'cwd', cwd)
            with open(os.path.join(cwd, 'regulome.cfg'), 'w') as fo:
                self.configs.write(fo)
            print('WARNING: configure the "regulome.cfg" file before starting the regulome_web')
        else:
            _ = self.configs.read(os.path.join(cwd, 'regulome.cfg'))

    def create_cache_structure(self):
        """Create the structure of directories of the cache"""
        for directory_build in BUILDS.keys():
            for directory_region in REGIONS.keys():
                for directory_tfbs in TFBS.keys():
                    for directory_snps in SNPS.keys():
                        for directory_chromatin in CHROMATIN.keys():
                            os.makedirs(os.path.join(self.configs['output']['cache'], 'nocache'),
                                        exist_ok=True)
                            os.makedirs(name=os.path.join(self.configs['output']['cache'],
                                                          'cache',
                                                          directory_build,
                                                          directory_region,
                                                          directory_tfbs,
                                                          directory_snps,
                                                          directory_chromatin),
                                        exist_ok=True)  # mode='755',

    def create_log_structure(self):
        """Create the structure of directories of the logs"""
        try:
            os.mkdir(path=self.configs['logs']['log_folder'])
        except FileExistsError as e:
            pass


def get_deploy_mode():
    """Read the regulome configuration file and return the deploy_mode value"""
    configs = configparser.ConfigParser()
    configs._interpolation = configparser.ExtendedInterpolation()
    _ = configs.read(os.path.join(os.getcwd(), 'regulome.cfg'))
    return configs['deploy_mode']['configuration']


@click.group()
@click.version_option()
def main():
    """Human Islet Regulome Browser."""
    pass


@main.command()
def start():
    """Starts the web application (Flask)."""
    from regulome_app.webapp.app import app
    from regulome_app.config import web_configuration
    deploy_mode = get_deploy_mode()
    app.config.from_object(web_configuration.get(deploy_mode, 'development'))
    app.run(host='0.0.0.0')  # debug=True


@main.command()
def init():
    """Creates the structure of the regulome browser.
    Checks for the presence of the regulome.cfg and the file will be created if it does not exist.
    Also creates, if not existing, the structures of the output and the logs folders.
    """
    _ = CheckStructure()
