# Import modules
import os
import datetime
import time
import subprocess
from regulome_app.config import logger, configs, REGULOME_R_SCRIPT
from regulome_app.webapp import models as models
from flask import request
import json


class Plot:
    """Create the regulome plot"""
    CACHE_TEMPLATE = os.path.join(
        configs['output']['cache'], 'cache',                       # Path of the cache
        '{build}', '{region}', '{tfbs}', '{snps}', '{chromatin}',  # Tree of directories
        '{build}_{chromosome}_{start}-{end}'                       # Name of the file
    )
    NOCACHE_TEMPLATE = os.path.join(
        configs['output']['cache'], 'nocache',       # Path of the cache
        '{user}_{build}_{chromosome}_{start}-{end}'  # Name of the file
    )
    # Script
    CMD = "{r_path} {r_script} "
    # Outputs
    CMD += "-p {cache_path}.pdf -o {cache_path}.txt -s {cache_path}.snp.txt "
    CMD += "-M {cache_path}.motifs.txt "
    # Coordinates
    CMD += "-B {build} -c {chromosome} -b {start} -e {end} -r {ranges} "
    # Data
    CMD += "-d {diagram_plot} -m {magic_plot} -u {user_regions} -U {user_snp} -Mt {mapTF} "
    CMD += "-Mr {mapRegion} -Mc {mapChromatin} "
    CMD += "-f {format_plot}"

    def __init__(self, messages, username):
        """Initiate the class. Load the message of the form"""
        self.msg = messages
        self.user = username

        if self.msg['upload_regions'] != 'None' or self.msg['upload_snps'] != 'None':
            self.cache = False
            self.cache_path = self.NOCACHE_TEMPLATE.format(
                user=self.user,
                build=self.msg['build'],
                chromosome=models.CHROMOSOMES_DICT[
                    self.msg['chromosome']
                ],
                start=self.msg['start'],
                end=self.msg['end']
            )
        else:
            self.cache = True
            self.cache_path = self.CACHE_TEMPLATE.format(
                build=self.msg['build'],
                region=self.msg['region'],
                tfbs=self.msg['tfbs'],
                snps=self.msg['select_snps'],
                chromatin='none' if self.msg['chromatin_profile'] == 'disabled' else self.msg['chromatin'],
                chromosome=models.CHROMOSOMES_DICT[
                    self.msg['chromosome']
                ],
                start=self.msg['start'],
                end=self.msg['end']
            )

        self.base_path = configs['output']['cache']
        self.cmd = self.define_cmd()
        self.ip = self.get_ip()
        # The creation ofg the plot is triggered by: self.run()

    def run(self):
        """Create the plot if needed"""
        if (not os.path.exists(self.cache_path + ".png") or
                    self.msg['upload_regions'] != 'None' or
                    self.msg['upload_snps'] != 'None'):
            exist = False
            logger.info('Building plot...')
            logger.info(self.cmd)
            self.do_plot()
            self.pdf_to_png()
        else:
            exist = True

        # Write the report
        self.report(exist=exist)

    def report(self, exist):
        """Write a line in the log file"""
        report = {
            'date': time.strftime("%Y-%m-%d"),
            'time': time.strftime("%H:%M:%S"),
            'datetime': datetime.datetime.now().isoformat(),
            'ip': self.ip,
            'user': self.user,
            'gene': None if self.msg['gene'] is None else self.msg['gene'],
            'command_line': self.cmd,
            'exist': exist
        }

        with open(configs['logs']['activity_log'], 'a') as log:
            log.write(json.dumps(report) + "\n")

    def define_cmd(self):
        """Define the R command line"""
        d = dict(
            r_path=configs['binaries']['Rscript_bin'],
            r_script=REGULOME_R_SCRIPT,
            cache_path=self.cache_path,
            build=self.msg['build'],
            chromosome=models.CHROMOSOMES_DICT[self.msg['chromosome']],
            start=self.msg['start'],
            end=self.msg['end'],
            ranges=self.msg['range_region'],
            diagram_plot='TRUE' if self.msg['select_snps'] == 'diagram' else 'FALSE',
            magic_plot='TRUE' if self.msg['select_snps'] == 'magic' else 'FALSE',
            user_regions='FALSE' if self.msg['upload_regions'] == 'None' else os.path.join(
             configs['data']['uploads'],
             "{}_{}".format(self.user, self.msg['upload_regions'])
            ),
            user_snp='FALSE' if self.msg['upload_snps'] == 'None' else os.path.join(
             configs['data']['uploads'],
             "{}_{}".format(self.user, self.msg['upload_snps'])
            ),
            format_plot='pdf',
            mapTF=self.msg['tfbs'],
            mapRegion=self.msg['region'],
            mapChromatin='FALSE' if (self.msg['chromatin'] == 'none' or self.msg['chromatin_profile'] == 'disabled') else self.msg['chromatin']
        )

        return self.CMD.format_map(d)

    def pdf_to_png(self):
        """Convert a pdf to a png"""
        cmd = [configs['binaries']['imagemagick']]
        cmd.extend('-geometry 1000 -quality 100 -density 150 -size 894x734'.split())
        cmd.extend([self.cache_path + '.pdf', self.cache_path + '.png'])
        with open(configs['logs']['regulome_log'], 'a') as log:
            log.write("Converting PDF tp PNG\n")
            result = subprocess.run(cmd, stdout=log)

    def do_plot(self):
        """Create the plot by executing the R script"""
        cmd = self.cmd.split()
        with open(configs['logs']['regulome_log'], 'a') as log:
            log.write("Creating plot\n")
            log.write(self.cmd + "\n")
            _ = subprocess.run(cmd, stdout=log)

    def get_results_path(self):
        """Return the last layers of the results path"""
        common_path = os.path.commonprefix([self.cache_path, configs['output']['cache']])
        relative_path = os.path.relpath(self.cache_path, common_path)
        return relative_path

    def get_results_name(self):
        """Return the name the file will be given"""
        name = os.path.split(self.get_results_path())[1]
        if self.cache:
            return name
        else:
            return name.split("_", 1)[-1]

    @staticmethod
    def get_ip():
        """Get the IP address of the user"""
        # ip = cgi.escape(os.environ["REMOTE_ADDR"])
        # request.remote_addr
        # request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        #
        # t.environ.get('REMOTE_ADDR', request.remote_addr)
        ip = (os.getenv("HTTP_CLIENT_IP") or
              os.getenv("HTTP_X_FORWARDED_FOR") or
              os.getenv("REMOTE_ADDR") or
              "UNKNOWN")
        return ip