#!/usr/bin/python
#coding: utf-8

__author__    = "jnmcclai"
__copyright__ = "Copyright 2016, Adtran, Inc."
__version__   = "2.7.7"

import logging
import time
import os
import re
from tempfile import mkstemp
from shutil import move

#define some logging
log_file = __file__.split('.')[0].split('/')[-1] + '.log'
logging.basicConfig(format='%(asctime)s %(message)s', filename=log_file, level=logging.DEBUG, filemode='w')

class Avalanche():
    """
    Spirent Avalanche traffic generator library
    
    args = {
                avalanche_path: filepath to work with Avalanche config files
                avalanche_config_filename: Avalanche config.tcl test filename

            }

    Class assumes TCL config file has already been built out 
    """

    def __init__(self, avalanche_path="C:\AvalancheExeDir", avalanche_config_filename="config.tcl"):
        """
        Class initialization
        """
        self.avalanche_path = avalanche_path
        self.avalanche_config_filename = avalanche_config_filename
        self.avalanche_abs_config_file = self.avalanche_path + "\\" + self.avalanche_config_filename

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
    def force_reserve_ports(self, force_reserve=True):
        """
        Modifies the Avalanche TCL script to fore reserve the ports

        args = {
                    force_reserve: if 'True', set the ReserveForce bit to 1 (default) and force reserve the Avalanche ports, else set bit to 0 to not force reserve
                }
        """
        #define file
        config_file = self.avalanche_abs_config_file
        #create a temporary file
        fh, temp_file = mkstemp()
        #set ReserveForce to 1 in config file
        if force_reserve:
            reserve_force_bit = '1'
        else:
            reserve_force_bit = '0'
        #open config file, make modifications, write to new file
        with open(temp_file, 'w') as new_file:
            with open(config_file) as old_file:
                for line in old_file:
                    if re.search('ReserveForce\s+\d', line):
                        new_file.write(re.sub('\d', str(reserve_force_bit), line))
                        logging.info("FILE: {0};ReserveForce: True".format(config_file.replace('\\', '/')))
                    else:
                        new_file.write(line)
        #close and move file                    
        os.close(fh) 
        move(temp_file, config_file)
    def set_license_file(self, lic_file):
        """
        Modifies the Avalanche TCL script to set the license file
        """
        #define config file
        config_file = self.avalanche_abs_config_file
        #create a temporary file
        fh, temp_file = mkstemp()
        #open config file, make modifications, write to new file
        with open(temp_file, 'w') as new_file:
            with open(config_file) as old_file:
                #set all the configrations to 
                for line in old_file:
                    if re.search('License\s+{', line):
                        new_file.write(re.sub('{.*?}', "{%s}", line) % lic_file)
                        logging.info('License: {0}'.format(lic_file))
                    else:
                        new_file.write(line)

        #close and move file                    
        os.close(fh) 
        move(temp_file, config_file) 

    def set_output_dir(self, output_dir=None):
        """
        Modifies the Avalanche TCL script to set the results output directory

        args = {
                    output_dir: the desired Avalanche results output directory
                }
        """
        #allow for output_dir to default to avalanche_path
        if output_dir:
            output_dir = output_dir
        else:
            output_dir = self.avalanche_path.replace('\\', '/')

        #define config file
        config_file = self.avalanche_abs_config_file
        #create a temporary file
        fh, temp_file = mkstemp()
        #open config file, make modifications, write to new file
        with open(temp_file, 'w') as new_file:
            with open(config_file) as old_file:
                #set all the configrations to 
                for line in old_file:
                    if re.search('OutputDir\s+{', line):
                        new_file.write(re.sub('{.*?}', "{%s}", line) % output_dir)
                        logging.info('Output Directory: {0}'.format(output_dir))
                    else:
                        new_file.write(line)

        #close and move file                    
        os.close(fh) 
        move(temp_file, config_file) 
    def set_associations(self, associations="all"):
        """
        Modifies the Avalanche TCL script to enables/disable Avalanche associations

        args = {
                    associations: the associaitions to enable [all|list of subnet names]
                }

        Sets both userBasedAssociations and globalAssociations for now...
        """

        #define config file
        config_file = self.avalanche_abs_config_file
        #create a temporary file
        fh, temp_file = mkstemp()

        if associations == "all":
            #open config file, make modifications, write to new file
            with open(temp_file, 'w') as new_file:
                with open(config_file) as old_file:
                    #enable all associations both userBased and global associations
                    for line in old_file:
                        if re.search('.client.userBasedAssociations.association\(\d+\).enabled', line) or re.search('.client.globalAssociations.association\(\d+\).enabled', line):
                            new_file.write(re.sub('{.*?}', "{true}", line))
                        else:
                            new_file.write(line)
                    logging.info("Associations enabled: {0}".format(assocations.lower()))
        else:
            #open config file, make modifications, write to new file
            with open(temp_file, 'w') as new_file:
                with open(config_file) as old_file:
                    #disable all associations both userBased and global associations
                    for line in old_file:
                        if re.search('.client.userBasedAssociations.association\(\d+\).enabled', line) or re.search('.client.globalAssociations.association\(\d+\).enabled', line):
                            new_file.write(re.sub('{.*?}', "{false}", line))
                        else:
                            new_file.write(line)

            #close and move file                    
            os.close(fh) 
            move(temp_file, config_file) 

            for association in association_list:
                print association
                #create a temporary file
                fh, temp_file = mkstemp()
                #open config file, make modifications, write to new file
                with open(temp_file, 'w') as new_file:
                    with open(config_file) as old_file:
                        #enable associations in list both userBased and global associations
                            for line in old_file:
                                if re.search('.clientSubnet\s+{%s}' % association, line):
                                    #write .clientSubnet line to file
                                    new_file.write(line)
                                    #skip to next line
                                    line = old_file.next()
                                    #use regex sub to enable association
                                    new_file.write(re.sub('{.*?}', "{true}", line))
                                else:
                                    new_file.write(line)
                #close and move file                    
                os.close(fh) 
                move(temp_file, config_file) 

            #log list of associations to be deleted
            logging.info("Associations enabled: {0}".format(associations))




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

    #initialize some example variables
    license_file = "C100_Lic"
    output_dir = "C:/AvalancheExeDir"
    #association_list = ["OctalOLT_Node1_Slot3", "OctalOLT_Node1_Slot4"]
    association_list = ["OctalOLT_Node1_Slot4"]

    instance = Avalanche()
    instance.force_reserve_ports(True)
    instance.set_license_file(license_file)
    instance.set_output_dir()
    instance.set_associations(association_list)
    #instance.start()