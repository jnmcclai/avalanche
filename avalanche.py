#!/usr/bin/python
#coding: utf-8

__author__    = "jnmcclai"
__copyright__ = "Copyright 2016, Adtran, Inc."
__version__   = "2.7.7"

import logging
import time
import subprocess
import os
import re

#define some logging
log_file = __file__.split('.')[0].split('/')[-1] + '.log'
logging.basicConfig(format='%(asctime)s %(message)s', filename=log_file, level=logging.DEBUG, filemode='w')

class Avalanche():
    """
    Spirent Avalanche traffic generator library
    
    args = {
                arg: description

            } 
    """

    def __init__(self, avalanche_path="C:\AvalancheExeDir"):
        """
        Class initialization
        """
        self.avalanche_path = avalanche_path
    def start(self):
        """
        Starts Avalanche TCL test case

        Navigates to avalanche_path directory and runs 'tchlsh test.tcl'
        """
        #change directories 
        logging.info("Directory changed {0}".format(self.avalanche_path))
        try:    
            os.chdir(self.avalanche_path)
        except:
            logging.warning("Unknown directory {0}".format(self.avalanche_path))
            raise AssertionError("Unknown directory {0}".format(self.avalanche_path))

        #start test
        logging.info("Starting Avalanche test...")
        try:    
            os.system('tclsh test.tcl')
        except:
            logging.warning("Avalanche test.tcl does not exist")
            raise AssertionError("Avalanche test.tcl does not exist".format(self.avalanche_path))
    def generate_avalanche_tcl_script(self):
        """
        Generates TCL script from an Avalanche test via test.tcl
        """
    def force_reserve_ports(self):
        """
        Modifies the Avalanche TCL script to fore reserve the ports
        """
    def force_release_ports(self):
        """
        Force releases Avalanche ports
        """
    def set_license_file(self):
        """
        Modifies the Avalanche TCL script to set the license file
        """
    def set_output_dir(self):
        """
        Modifies the Avalanche TCL script to set the results output directory
        """
    def set_associations(self):
        """
        Modifies the Avalanche TCL script to enables/disable Avalanche associations
        """
    def set_runtime(self):
        """
        Modifies the Avalanche TCL script to set the Avalanche run time properties

        Allow to change RampUp, Steady Time, RampDown time via arguments with defaults
        """
    def analyze_results(self):
        """
        Analyze the Avalanche test results
        """
    def analyze_goodput(self):
        """
        Analzye the Avalanche test results goodput
        """
    def analyze_fairness(self):
        """
        Analyze the Avalanche test results fairness
        """
    def get_directories(self):
        """
        Get a list of directories
        """
    def publish_results(self):
        """
        Publish Avalanche test results to database
        """
    def get_config_files(self):
        """
        Get the Avalanche TCL config files from version controlled repository and move them to avalanche_path
        """

if __name__ == '__main__':
    """
    Spirent Avalanche traffic generator library
    """

    ###########################################
    #EXAMPLES
    ###########################################

    instance = Avalanche()
    instance.start()