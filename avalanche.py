#!/usr/bin/python
#coding: utf-8

__author__    = "jnmcclai"
__copyright__ = "Copyright 2016, Adtran, Inc."
__version__   = "2.7.7"

import logging
import time
import os
import re
import shutil
from tempfile import mkstemp


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
        logging.info("[FILE.INFO]: Directory changed {0}".format(self.avalanche_path))
        try:    
            os.chdir(self.avalanche_path)
        except:
            logging.warning("[FILE.WARNING]: Unknown directory {0}".format(self.avalanche_path))
            raise AssertionError("[FILE.WARNING]: Unknown directory {0}".format(self.avalanche_path))

        #start test
        logging.info("[AVALANCHE]: Starting Avalanche test...")
        try:    
            os.system('tclsh test.tcl')
        except:
            logging.warning("[FILE.WARNING]: Avalanche test.tcl does not exist")
            raise AssertionError("[FILE.WARNING]: Avalanche test.tcl does not exist".format(self.avalanche_path))
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
                        logging.info("[FILE.INFO]: {0}; ReserveForce: True".format(config_file.replace('\\', '/')))
                    else:
                        new_file.write(line)
        #close and move file                    
        os.close(fh) 
        shutil.move(temp_file, config_file)
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
                        logging.info('[FILE.INFO]: License: {0}'.format(lic_file))
                    else:
                        new_file.write(line)

        #close and move file                    
        os.close(fh) 
        shutil.move(temp_file, config_file) 

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
                        logging.info('[FILE.INFO]: Output Directory: {0}'.format(output_dir))
                    else:
                        new_file.write(line)

        #close and move file                    
        os.close(fh) 
        shutil.move(temp_file, config_file) 
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
                    logging.info("[FILE.INFO]: Associations enabled: {0}".format(assocations.lower()))
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
            shutil.move(temp_file, config_file) 

            for association in association_list: 
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
                shutil.move(temp_file, config_file) 

            #log list of associations to be deleted
            logging.info("[FILE.INFO]: Associations enabled: {0}".format(associations))

    def set_runtime(self, runtime, param="soak", loads=None):
        """
        Modifies the Avalanche TCL script to set the Avalanche run time properties

        args = {    
                    runtime: the time in seconds to change to
                    associations: the associaitions to enable [all|list of subnet names]
                    param: the runtime parameter to adjust [Soak|RampUp|RampDown] 
                    loads: if a list is defined then set the runtime properties for those load profiles only, else set the runtime properties for all the loads (including default) - again important on label syntax (if you do not know what this is, you probably want to leave it undefined)
                }

        Allow to change RampUp, Steady Time, RampDown time via arguments with defaults
        It is important to know this only works if the developer of the Avalanche test cases sets the load configuration labels appropriately - strictly using only case insensitive [Soak|Steady Time|RampUp|Ramp Up|RampDown|Ramp Down]
        """
                #define config file
        config_file = self.avalanche_abs_config_file
        #create a temporary file
        fh, temp_file = mkstemp()

        #Modify the Avalanche load time in config.tcl
        if "up" in param.lower():
            logging.info("[FILE.INFO]: config.tcl; load config; RampUp; Time: {0}".format(runtime))
            #open config file, make modifications, write to new file
            with open(temp_file, 'w') as new_file:
                with open(config_file) as old_file:
                    #set the rampTime for the available load profiles matching under {Ramp Up} or {RampUp} - case insensitive
                    for line in old_file:
                        if re.search('loadprofile_handle\s+-steps.step\(\d+\).label\s+{Ramp\s+Up}', line, re.IGNORECASE) or re.search('loadprofile_handle\s+-steps.step\(\d+\).label\s+{RampUp}', line, re.IGNORECASE):
                            #skip five lines and write them to the file to get to the rampTime property
                            new_file.write(line)
                            line = old_file.next()
                            new_file.write(line)
                            line = old_file.next()
                            new_file.write(line)
                            line = old_file.next()
                            new_file.write(line)
                            line = old_file.next()
                            new_file.write(line)
                            line = old_file.next()
                            #use regex sub to set the rampTime - units: seconds
                            new_file.write(re.sub('{.*?}', "{%s}" % runtime, line))
                        else:
                            new_file.write(line)

        elif "down" in param.lower():
            logging.info("[FILE.INFO]: config.tcl; load config; RampDown; Time: {0}".format(runtime))
            #open config file, make modifications, write to new file
            with open(temp_file, 'w') as new_file:
                with open(config_file) as old_file:
                    #set the rampTime for the available load profiles matching under {Ramp Down} or {RampDown} - case insensitive
                    for line in old_file:
                        if re.search('loadprofile_handle\s+-steps.step\(\d+\).label\s+{Ramp\s+Down}', line, re.IGNORECASE) or re.search('loadprofile_handle\s+-steps.step\(\d+\).label\s+{RampDown}', line, re.IGNORECASE):
                            #skip five lines and write them to the file to get to the rampTime property
                            new_file.write(line)
                            line = old_file.next()
                            new_file.write(line)
                            line = old_file.next()
                            new_file.write(line)
                            line = old_file.next()
                            new_file.write(line)
                            line = old_file.next()
                            new_file.write(line)
                            line = old_file.next()
                            #use regex sub to set the rampTime - units: seconds
                            new_file.write(re.sub('{.*?}', "{%s}" % runtime, line))
                        else:
                            new_file.write(line)
        else:
            logging.info("[FILE.INFO]: config.tcl; load config; SteadyState; Time: {0}".format(runtime))
            #open config file, make modifications, write to new file
            with open(temp_file, 'w') as new_file:
                with open(config_file) as old_file:
                    #set the rampTime for the available load profiles matching under {Soak} or {Steady\s+State} - case insensitive
                    for line in old_file:
                        if re.search('loadprofile_handle\s+-steps.step\(\d+\).label\s+{Soak}', line, re.IGNORECASE) or re.search('loadprofile_handle\s+-steps.step\(\d+\).label\s+{Steady\s+State}', line, re.IGNORECASE) or re.search('loadprofile_handle\s+-steps.step\(\d+\).label\s+{SteadyState}', line, re.IGNORECASE):
                            #skip six lines and write them to the file to get to the steadyTime property
                            new_file.write(line)
                            line = old_file.next()
                            new_file.write(line)
                            line = old_file.next()
                            new_file.write(line)
                            line = old_file.next()
                            new_file.write(line)
                            line = old_file.next()
                            new_file.write(line)
                            line = old_file.next()
                            new_file.write(line)
                            line = old_file.next()
                            #use regex sub to set the rampTime - units: seconds
                            new_file.write(re.sub('{.*?}', "{%s}" % runtime, line))
                        else:
                            new_file.write(line)

        #close and move file                    
        os.close(fh) 
        shutil.move(temp_file, config_file) 

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
    def get_config_files(self, testbed, avalanche_test_name, repo_dir="C:/iTest_4.0/PQ_Production_Project/ConfigurationFiles/Avalanche", license_dir="C:/iTest_4.0/PQ_Production_Project/ConfigurationFiles/Avalanche/Avalanche_License"):
        """
        Get the Avalanche TCL config files from version controlled repository and move them to avalanche_path

        args = {
                    testbed: testbed name - used for name of parent folder in repo to grab an Avalanche test case (e.g. ERPS)
                    avalanche_test_name: the sub parent folder under the testbed that defines the Avalanche project and test (e.g. ERPS_NODE1_1-NODE_1)
                    repo_dir: currently, the filepath to the shared SVN Avalanche config files - defaults to "C:/iTest_4.0/PQ_Production_Project/ConfigurationFiles/Avalanche"
                    license_dir: currently, the filepath to the shared SVN Avalanche license files - defaults to "C:/iTest_4.0/PQ_Production_Project/ConfigurationFiles/Avalanche/Avalanche_License"
                }

        The arguments here are needed to point to the SVN Avalanche configuration files - eventually will most likely be severed with migration to python/robot using some github/perforce version control

        """
        #overwrite avalanche_path directory "C:/AvalancheExeDir"
        avalanche_path = self.avalanche_path.replace("\\", "/")
        try:
            #delete directory
            shutil.rmtree(avalanche_path)
            logging.info("[FILE.INFO]: Deleted directory {0}".format(avalanche_path))
        except EnvironmentError, e:
            #directory not found
            logging.warning("[FILE.ERROR]: {0}; {1}".format(avalanche_path, e))

        #build out location containing the desired Avalanche test to run
        avalanche_src_filepath_test = repo_dir + "/" + testbed + "/" + avalanche_test_name
        avalanche_src_filepath_lic = license_dir
        logging.info("[FILE.INFO]: Avalanche license filepath: {0}".format(avalanche_src_filepath_lic))
        logging.info("[FILE.INFO]: Avalanche test filepath: {0}".format(avalanche_src_filepath_test))

        #must copy the license files first

        #loop over list of files within license directory and copy to avalanche_path
        self.copy_files(avalanche_src_filepath_lic, avalanche_path)
        #get list of files within Avalanche test directory and copy to avalanche_path
        self.copy_files(avalanche_src_filepath_test, avalanche_path)


    def copy_files(self, src, dst, symlinks=False, ignore=None):
        """
        Simple method to aid in copying over Avalanche files from one directory to another

        args = {
                    src: the absolute source directory (e.g "C:/iTest_4.0/PQ_Production_Project/ConfigurationFiles/Avalanche/ERPS/ERPS_NODE1_1-NODE_1")
                    dst: the absolute destination directory (e.g. "C:/AvalancheExeDir")
                    symlinks, ignore: shutil.copytree args
                }
        """
        for filename in os.listdir(src):
            #join the path and filename
            file_src = os.path.join(src, filename)
            file_dst = os.path.join(dst, filename)
            #if directory, use copytree; else, use copy2
            if os.path.isdir(file_src):
                shutil.copytree(file_src, file_dst, symlinks, ignore)
            else:
                shutil.copy2(file_src, file_dst)


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
    testbed = "ERPS"
    avalanche_test_name = "ERPS_NODE1_1-NODE_1"
    association_list = ["OctalOLT_Node1_Slot3", "OctalOLT_Node1_Slot4"]
    time_ramp_up = '15'
    time_steady = '100'
    time_ramp_down = '10'

    #initiate Avalanche instance
    instance = Avalanche()
    #copy Avlanche test and license files
    instance.get_config_files(testbed, avalanche_test_name)
    #force reserve Avlanche ports
    instance.force_reserve_ports(True)
    #set the Avalanche license file
    instance.set_license_file(license_file)
    #set the Avalanche results output directory
    instance.set_output_dir()
    #set the Avalanche associations to run for a given test
    instance.set_associations(association_list)
    #set the RampUp rampTime
    instance.set_runtime(time_ramp_up, param="RampUp")
    #set the Steady State steadyTime
    instance.set_runtime(time_steady)
    #set the RampDown rampTime
    instance.set_runtime(time_ramp_down, param="RampDown")
    #start the test
    instance.start()