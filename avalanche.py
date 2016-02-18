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
#import database


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

    def __init__(self, avalanche_path="C:\AvalancheExeDir", avalanche_config_filename="config.tcl", output_dir="C:\AvalancheExeDir"):
        """
        Class initialization
        """
        self.avalanche_path = avalanche_path
        self.avalanche_config_filename = avalanche_config_filename
        self.avalanche_abs_config_file = self.avalanche_path + "\\" + self.avalanche_config_filename
        self.output_dir = output_dir

    def start(self, trial_mode=False):
        """
        Starts Avalanche TCL test case

        args = {
                    trial_mode: if 'True', run Avalanche test in trial mode and only run through action list once, else run normal (default)
                }

        Navigates to avalanche_path directory and runs 'tchlsh test.tcl'
        """
        #toggle the trial mode bit
        if trial_mode:
            self.enable_trial_mode(True)
        else:
            self.enable_trial_mode(False)

        #change directories 
        logging.info("[FILE.INFO]: Directory changed {0}".format(self.avalanche_path.replace('\\', '/')))
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
                        logging.info("[FILE.INFO]: {0}; ReserveForce: {1}".format(self.avalanche_config_filename, force_reserve))
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
                        logging.info('[FILE.INFO]: {0}; License: {1}'.format(self.avalanche_config_filename, lic_file))
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
        #set output_dir - allow user to set the directory or just use the one initialized with the class
        if output_dir:
            output_dir = output_dir
        else:
            output_dir = self.output_dir.replace('\\', '/')

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
                        logging.info('[FILE.INFO]: {0}; Result Output Directory: {1}'.format(self.avalanche_config_filename, output_dir))
                    else:
                        new_file.write(line)

        #close and move file                    
        os.close(fh) 
        shutil.move(temp_file, config_file)


    def enable_trial_mode(self, enable_trial_mode=False):
        """
        Modifies the Avalanche TCL script to enable the trial run bit to start the test and run the action list only once

        args = {
                    enable_trial_run: if 'True', set the Trial run bit to 1 and run test in trial mode, else set bit to 0 and run normal mode (default)
                }
        """
        #define file
        config_file = self.avalanche_abs_config_file

        #create a temporary file
        fh, temp_file = mkstemp()

        #intialize the enable_trial_bit
        if enable_trial_mode:
            enable_trial_bit = '1'
        else:
            enable_trial_bit = '0'

        #create a temporary file
        fh, temp_file = mkstemp()
        #open config file, make modifications, write to new file
        with open(temp_file, 'w') as new_file:
            with open(config_file) as old_file:
                for line in old_file:
                    if re.search('Trial\s+\d', line):
                        new_file.write(re.sub('\d', str(enable_trial_bit), line))
                        logging.info("[FILE.INFO]: {0}; Trial Mode: {1}".format(self.avalanche_config_filename, enable_trial_mode))
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
                    logging.info("[FILE.INFO]: {0}; Associations enabled: {1}".format(self.avalanche_config_filename, assocations.lower()))
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
            logging.info("[FILE.INFO]: config.tcl; Associations enabled: {0}".format(associations))

    def get_results_and_post_to_db(self, dir_list, output_dir=None):
        """
        Retrieve the Avalanche generated results from the client side hostStats.csv files and publish to database

        args = {
                    dir_list: list of Avalanche generated client result directories containing hostStats.csv files (e.g. client-subtest_0_core1)

                }

        #for each client hostStats.csv Avalanche results file open up that file
        #parse through that file looking for valid VLANs (pairs)
        #exctract 
        -"Bytes Received"
        -"Goodput[Http] Cumulative Receive"
        -"Goodput[Http] Ave Receive Rate (bps)"
        #publish these results and other test run properties to a database 
        #these results can then be pulled down and manipulated to test goodput, fairness, etc
        """
        #set output_dir - allow user to set the directory or just use the one initialized with the class.  Also tack on '/results' to give something like "C:/AvalancheExeDir/results"
        if output_dir:
            results_dir = output_dir + "/results"
        else:
            results_dir = self.output_dir.replace('\\', '/') + "/results"

        for filename in dir_list:   
            #build the absolute path to hostStats.csv file
            client_results = results_dir + "/" + filename + "/hostStats.csv"

            #create a temporary file
            fh, temp_file = mkstemp()

            #initialize vlan lists
            vlan_list = list()
            vlan_list_pairs = list()

            #open the hostStats.csv file in each directory to retrieve data
            #open the hostStats.csv file in each directory to retrieve list of VLANs
            with open(temp_file, 'w') as new_file:
                with open(client_results) as old_file:
                    for line in old_file:
                        #print line
                        #get full list of VLANs
                        if re.search('VLAN,\d+', line):
                            #print line
                            #strip the newline character
                            vlan = line.strip()
                            #just grab the VLAN value
                            vlan = vlan.split(",")[1]
                            vlan_list.append(vlan)
                            # new_file.write(re.sub('\d', str(reserve_force_bit), line))
                            # logging.info("[FILE.INFO]: {0}; ReserveForce: {1}".format(self.avalanche_config_filename, force_reserve))
                        else:
                            pass
                            # new_file.write(line)

            #close and move file                    
            os.close(fh) 
            
            #printing list for sanity
            #print vlan_list

            #get a list of VLAN pairs - [[1,2], [2,3], [3,4], ... [n,m], [m, m+1]]
            for n in range(len(vlan_list)):
                try:
                    vlan_list_pairs.append([vlan_list[n], vlan_list[n+1]])
                except:
                    #handle if run into an odd number of VLANs 
                    vlan_list_pairs.append([vlan_list[n], "NULL"])

            #printing vlan pair list for sanity
            # print len(vlan_list)
            # print vlan_list_pairs

            #grab a block of data from the Avalanche client results file contained within a set of VLANs
            # with open(temp_file, 'r') as new_file:
            #     #reading the file into memory here (probably will do this once above when grabbing vlans)
            #     file_contents = new_file.read()

            for vlan_pair in vlan_list_pairs:
                #get start and stop VLAN
                vlan_start = vlan_pair[0]
                vlan_stop = vlan_pair[1]

            #open the hostStats.csv file in each directory to retrieve data within block of VLANs
            with open(client_results, 'r') as old_file:
                    #read the Avalanche client results file into memory
                    file_contents = old_file.read()
                    #get block of data between VLANs for each VLAN pair
            block = re.findall("VLAN,{0}(.*?)VLAN,{1}".format(vlan_start, vlan_stop), file_contents, re.DOTALL|re.MULTILINE)
            print block
                        
            #grab a block of data between VLANs (use regexp)
            #then grab info from db (SELECT * FROM `Vlan_Slot_Pon_Mapping` WHERE `TestBed` like "[param node]" and `Vlan` like "$startVlan1")
            #grab bytes resceived - regex
            #grab goodput cumulative received - regex
            #grab goodput avg received rate (bps) - regex
            #publish results to db ($insertCommand ("0","$testRun","$testCaseName","$startVlan1","0","$slotNum","$ponNum","$bytesRcvd","$gPutCumRcv","$gPutAvgRcvRate","$timeStamp");)

    def analyze_goodput(self):
        """
        Analzye the Avalanche test results goodput
        """
    def analyze_fairness(self):
        """
        Analyze the Avalanche test results fairness
        """
    def get_directories(self, output_dir=None):
        """
        Get a list of directories
        """
        
        #set output_dir - allow user to set the directory or just use the one initialized with the class.  Also tack on '/results' to give something like "C:/AvalancheExeDir/results"
        if output_dir:
            results_dir = output_dir + "/results"
        else:
            results_dir = self.output_dir.replace('\\', '/') + "/results"

        #initialize client results directory name list 
        client_results = list()

        #loop over the directories in Avalanche result directory and append directory name if contains client
        try:
            for directory in os.listdir(results_dir):
                if re.search('client', directory):
                    client_results.append(directory)
                else:
                    pass
        except EnvironmentError, e:
            #directory not found
            logging.warning("[AVALANCHE.ERROR]: {0}; {1}".format(results_dir, e))
        #verify we got something
        if len(client_results) == 0:
            raise AssertionError("[AVALANCHE.ERROR]: {0}; No client results found!".format(results_dir))
        #log the client result directories retrieved
        logging.info("[AVALANCHE.RESULTS]: {0}; Client Directories: {1}".format(results_dir, client_results))
        #return list of client results directories
        return client_results

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
            #create a temporary file - just noticed this could be happening twice in this case!!!
            fh, temp_file = mkstemp()

            ###only adjust runtime properties for those load profiles defined###
            if loads:
                logging.info("[FILE.INFO]: {0}; load config; loads: {1}".format(self.avalanche_config_filename, loads))
                #loop over all the loads
                for load in loads:
                    #create a temporary file
                    fh, temp_file = mkstemp()
                    #open config file, make modifications, write to new file
                    with open(temp_file, 'w') as new_file:
                        with open(config_file) as old_file:
                            #find all the load profiles that match
                            for line in old_file:
                                if re.search('set\s+loadprofile_handle\s+\[getOrCreateNode\s+\$projectHandle\s+loads\s+%s' % load, line):
                                    #found a matching load profile
                                    #write that line
                                    new_file.write(line)
                                    while True:
                                        #get the next line, if it exists
                                        try:
                                            line = old_file.next()
                                        except StopIteration:
                                            break
                                        #see if the line deals with loadprofile handling
                                        if re.search('set\s+loadprofile_handle', line):
                                            #it does so will break and check to see if it is one of the loads we want
                                            new_file.write(line)
                                            break
                                        else:
                                            #set RampUp rampTime property
                                            if "up" in param.lower():
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
                                                    #log the changes
                                                    logging.info("[FILE.INFO]: config.tcl; load '{0}'; RampUp; Time: {1}".format(load, runtime))
                                                else:
                                                    new_file.write(line)
                                                
                                            
                                            #set RampDown rampTime property
                                            elif "down" in param.lower():
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
                                                    #log the changes
                                                    logging.info("[FILE.INFO]: config.tcl; load '{0}'; RampDown; Time: {1}".format(load, runtime))
                                                else:
                                                    new_file.write(line)

                                            #set Steady State/Soak steadyTime property
                                            else:
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
                                                    #log the changes
                                                    logging.info("[FILE.INFO]: config.tcl; load '{0}'; Soak; Time: {1}".format(load, runtime))
                                                else:
                                                    new_file.write(line)
                                else:
                                    #not a line with matching load profile
                                    new_file.write(line)

                    #close and move file each time
                    os.close(fh) 
                    shutil.move(temp_file, config_file) 

            ####adjust the runtime properties for all the load profiles###
            else:
                if "up" in param.lower():
                    logging.info("[FILE.INFO]: {0}; load config; RampUp; Time: {1}".format(self.avalanche_config_filename, runtime))
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
                    logging.info("[FILE.INFO]: {0}; load config; RampDown; Time: {1}".format(self.avalanche_config_filename, runtime))
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
                    logging.info("[FILE.INFO]: {0}; load config; SteadyState; Time: {1}".format(self.avalanche_config_filename, runtime))
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
    avalanche_test_name = "ERPS_NODE1-NODE_1"
    association_list = ["OctalOLT_Node1_Slot3", "OctalOLT_Node1_Slot4"]
    loads = ["erpsClientLoadProfile_Node1", "Default"]
    time_ramp_up = '10'
    time_steady = '120'
    time_ramp_down = '15'

    #initiate Avalanche instance
    instance = Avalanche()

    ########MODIFY_CONFIG########
    # #copy Avlanche test and license files
    # #instance.get_config_files(testbed, avalanche_test_name)
    # #force reserve Avlanche ports
    # instance.force_reserve_ports(True)
    # # #set the Avalanche license file
    # instance.set_license_file(license_file)
    # # #set the Avalanche results output directory
    # instance.set_output_dir()
    # # #set the Avalanche associations to run for a given test
    # instance.set_associations(association_list)
    # # #set the RampUp rampTime
    # instance.set_runtime(time_ramp_up, param="RampUp")
    # # #set the Steady State steadyTime
    # instance.set_runtime(time_steady)
    # # #set the RampDown rampTime
    # instance.set_runtime(time_ramp_down, param="RampDown")
    # #example setting RampUp rampTime for a set of loads
    # #instance.set_runtime(time_ramp_up, param="RampUp", loads=loads)
    # #example setting Steady State steadyTime for a set of loads
    # #instance.set_runtime_runtime(time_steady, loads=loads)
    # #example setting RampDown rampTime for a set of loads
    # #instance.set_runtime(time_ramp_down, param="RampDown", loads=loads)

    ############START############
    # #start the test
    # instance.start(True)

    ###########ANALYSIS##########
    #get list of client result directories - multiple cores
    filenames = instance.get_directories()
    #for now, just open up the hostStats.csv and print each line
    instance.get_results_and_post_to_db(filenames)


    #############################
    #NOTES
    #############################
    """
    -For the associations and loads, it would be nice to grab a count when the regex finds a match
    or find a way to verify that the user defined associations and loads actually exist in the config.tcl
    file.  If so great, else can throw in some logging with a warning indicating that association or load
    was not found in the config file
    -Might see if can poll C:\ProgramData\Spirent\Avalanche 4.42\user\jnmcclai\workspaces\.tempxxx...results\..
    to poll some of the stats realtime (success/fails)


    >>> var = "VLAN,1801\nthis is some text\nhere is some more\nVLAN,1801"
    >>> print var
    VLAN,1801
    this is some text
    here is some more
    VLAN,1801
    >>>
    >>>
    >>> import re
    >>> var = "VLAN,1801\nthis is some text\nhere is some more\nVLAN,1802"
    >>>
    >>> r = re.findall('VLAN,1801(.*?)VLAN,1802', var, re.S)
    >>> print r
    ['\nthis is some text\nhere is some more\n']

    >>> r = re.findall('VLAN,1801(.*?)VLAN,1802', var, re.MULTILINE)
    >>> print r
    []
    >>> r = re.findall('VLAN,1801(.*?)VLAN,1802', var, re.DOTALL|re.MULTILINE)
    >>> print r
    ['\nthis is some text\nhere is some more\n']

    probably worth reading the client results into memory as it is not changing (unless realtime analysis)
    and allow 

    """