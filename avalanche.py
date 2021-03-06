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
import database
import socket
from datetime import datetime

#define some logging
log_file = __file__.split('.')[0].split('/')[-1] + '.log'
logging.basicConfig(format='%(asctime)s %(message)s', filename=log_file, level=logging.DEBUG, filemode='w')

class Avalanche():
    """
    Spirent Avalanche traffic generator library
    
    args = {
                avalanche_path: filepath to work with Avalanche config files
                avalanche_config_filename: Avalanche config.tcl test filename
                output_dir: the Avalanche results output directory
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
        self.testbed = testbed
        self.hostname = socket.gethostbyaddr(socket.gethostname())[0].split(".")[0].upper()
        self.date_time = datetime.now().strftime('%Y%m%d%H%M%S')
        self.test_run = self.hostname + self.date_time
        self.time_stamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

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

    def get_results_and_post_to_db(self, testbed, dir_list, avalanche_test_name, my_subnet="10.213.", output_dir=None, db_ip="10.21.1.181", db_port=3306, db_database="pqGeneral"):
        """
        Retrieve the Avalanche generated results from the client side hostStats.csv files and publish to database

        args = {
                    testbed: the test bed name - used for database queries (Generally the TID but may vary) - (e.g. 'FTTP-NODE-1' or 'PQ2E-NODE1_S16')
                    dir_list: list of Avalanche generated client result directories containing hostStats.csv files (e.g. client-subtest_0_core1)
                    avalanche_test_name: the Avalanche test name (e.g. SM040_CSLAG-4_Data_Verification-Avalanche)
                    my_subnet: the users subnet (10.213.*) - this is used to filter down some more giving a desired line to extract result stats
                    output_dir: the location where the Avalanche results files live (e.g. C:/AvalancheExeDir) this + '/results' + dir_list gives desired path containing hostStats.csv
                    db_ip: the database server IP address
                    db_port: the database server port (3306)
                    db_database: the database to select
                }

        Open up each client side Avalanche results hostStats.csv file.
        Parse through the file and grab a list of VLANs.
        Create a list of VLAN pairs.
        Extract data from the files that lives in between the VLAN pairs.
        Connect to database and get VLAN mapping
        Get the below:
            -"Bytes Received"
            -"Goodput[Http] Cumulative Receive"
            -"Goodput[Http] Ave Receive Rate (bps)"
        Publish these results and other test run properties to a database 
        These results can then be pulled down and manipulated to test goodput, fairness, etc

        Connects to MySQLdb using the custom database module - this assumes the user has pre-built vlan mappings in the database

        """
        #db initialize variables
        db_username = "pqgen"
        db_pwd = "pqgen"
        #db vlan map pull variables
        db_table_vlan_mapping = "Vlan_Slot_Pon_Mapping"
        db_vlan_map = database.Database(db_ip, db_port, db_database, db_username, db_pwd)
        #db traffic push variables
        db_database_traffic = "trafficResults" #static for now
        db_traffic = database.Database(db_ip, db_port, db_database_traffic, db_username, db_pwd)
        db_avalanche_test_results = "trafficResults"
        db_table_avalanche_test_results = "Avalanche_Test_Results"
        sql_fields = "(`id`, `testRun`, `testName`, `vlan`, `vlan2`, `slot`, `pon`, `port`, `bytesReceived`, `goodPutCumRcv`, `goodputAvgRcvRate`, `timestamp`)"

        #connect to database
        db_vlan_map.db_connect()
        db_traffic.db_connect()
        
        #set output_dir - allow user to set the directory or just use the one initialized with the class.  Also tack on '/results' to give something like "C:/AvalancheExeDir/results"
        if output_dir:
            results_dir = output_dir + "/results"
        else:
            results_dir = self.output_dir.replace('\\', '/') + "/results"

        for filename in dir_list:   
            #build the absolute path to hostStats.csv file
            client_results = results_dir + "/" + filename + "/hostStats.csv"

            #initialize vlan lists
            vlan_list_outer = list()
            vlan_list_inner = list()
            vlan_list_pairs_outer = list()
            vlan_list_pairs_inner = list()

            #open the hostStats.csv file in each directory to retrieve data within blocks of VLANs
            #client_results_file = open(client_results, 'r')
            with open(client_results, 'r') as client_results_file:
                #retrieve a list of VLANs
                for line in client_results_file:
                    #get full list of VLANs
                    if re.search('VLAN,\d+', line):
                        #print line
                        #strip the newline character
                        vlan = line.strip()
                        #just grab the VLAN value
                        vlan_outer = vlan.split(",")[1].split("/")[0]
                        #also going back to grab the inner VLAN
                        try:
                            vlan_inner = vlan.split(",")[1].split("/")[1]
                        except:
                            vlan_inner = "NULL"
                        vlan_list_outer.append(vlan_outer)
                        vlan_list_inner.append(vlan_inner)
                    
                    else:
                        pass
       
            #printing list for sanity
            #print vlan_list

            #get a list of VLAN pairs ~ [[1,2], [2,3], [3,4], ... [n,m], [m, m+1]]
            for n in range(len(vlan_list_outer)):
                try:
                    vlan_list_pairs_outer.append([vlan_list_outer[n], vlan_list_outer[n+1]])
                    vlan_list_pairs_inner.append([vlan_list_inner[n], vlan_list_inner[n+1]])
                except:
                    #handle if run into an unique number of VLANs 
                    vlan_list_pairs_outer.append([vlan_list_outer[n], "NULL"])
                    vlan_list_pairs_inner.append([vlan_list_inner[n], "NULL"])

            # #printing vlan pair list for sanity
            # print len(vlan_list_outer)
            # print vlan_list_pairs


            #read the Avalanche client results file into memory - may not need to open file twice
            client_results_file = open(client_results, 'r')
            file_contents = client_results_file.read()

            #temp_count = 0
            #print my_subnet
            for vlan_pair_outer, vlan_pair_inner in zip(vlan_list_pairs_outer, vlan_list_pairs_inner):

                #get start and stop VLAN
                vlan_start_outer = vlan_pair_outer[0]
                vlan_stop_outer = vlan_pair_outer[1]
                #get this for inner VLAN if exists
                vlan_start_inner = vlan_pair_inner[0]

                #get block of data between VLANs for each VLAN pair
                vlan_block = re.findall("VLAN,{0}(.*?)VLAN,{1}".format(vlan_start_outer, vlan_stop_outer), file_contents, re.DOTALL|re.MULTILINE)
                #print vlan_block
                #break
                
                #check to see if my_subnet is found in the VLAN block, if so, pull VLAN mapping from db, else skip to the next pair
            
                #still may want to sift down to just get the data block minus the headers
                for element in vlan_block:
                    if my_subnet in element:
                        #print vlan_block
                        #temp_count += 1
                        #determine valid VLANs
                        start_vlan_01 = vlan_start_outer
                        start_vlan_02 = vlan_start_inner
                        # print start_vlan_01
                        # print start_vlan_02
                        #perform VLAN mapping db retrieval for the corresponding VLANs
                        if start_vlan_02 == "NULL":
                            sql_vlan_map_query = "SELECT * FROM {0} WHERE `TestBed` like '{1}' AND `Vlan` LIKE {2}".format(db_table_vlan_mapping, testbed, start_vlan_01)
                            #print sql_vlan_map_query
                        else:
                            sql_vlan_map_query = "SELECT * FROM {0} WHERE `TestBed` like '{1}' AND `Vlan` LIKE {2} AND `vlan2` LIKE {3}".format(db_table_vlan_mapping, testbed, start_vlan_01, start_vlan_02)
                            #print sql_vlan_map_query

                        #get the row count and query response
                        query_response = db_vlan_map.db_pull(sql_vlan_map_query)
                        #print "Row count: " + query_response[0]
                        #print "SQL Response: " + query_response[1]
                        if query_response[1]:
                            sql_response = query_response[1][0]
                            #print sql_response
                        else:
                            logging.warning("[DB.WARNING]: ENTRY NOT FOUND; {0}".format(sql_vlan_map_query))

                        #query SQL response to extract slot, pon, port, etc
                        slot = sql_response[3]
                        pon = sql_response[4]
                        port = sql_response[9]
                        

                        #grab the statistics - bytes received, goodput cumulative received, goodput avg received rate (bps)
                        vlan_block_list = vlan_block[0].split(",")
                        base = 712 * 2
                        bytes_received = vlan_block_list[base + 9]
                        goodput_cum_received = vlan_block_list[base + 249]
                        goodput_avg_received_rate = vlan_block_list[base + 250]

                        #printing results for sanity
                        # print "bytes received: " + bytes_received
                        # print "goodput cumulative received: " + goodput_cum_received
                        # print "goodput avg received rate (bps): " + goodput_avg_received_rate

                        #check if inner tag is defined for publishing to results db -----> figure out what to do with port 'None'/Null val
                        if start_vlan_02 == "NULL":
                            values = ('0', self.test_run, avalanche_test_name, start_vlan_01, '0', str(slot), str(pon), str(port), bytes_received, goodput_cum_received, goodput_avg_received_rate, self.time_stamp) 

                        else:
                            values = ('0', self.test_run, avalanche_test_name, start_vlan_01, start_vlan_02, str(slot), str(pon), str(port), bytes_received, goodput_cum_received, goodput_avg_received_rate, self.time_stamp) 

                        #publish data to db
                        sql_query_push = "INSERT INTO `{0}`.`{1}` {2} VALUES {3}".format(db_avalanche_test_results, db_table_avalanche_test_results, sql_fields, values)
                        logging.info("[DB.INFO]: DB PUBLISH; VALUES: {0}".format(values))
                        db_traffic.db_push(sql_query_push)

                    else:
                        #my_subnet not found in block
                        pass

        #close database
        db_vlan_map.db_close()
        db_traffic.db_close()

    def analyze_goodput(self, avalanche_test_name, min_goodput=0.85, mode="", slot="", pon="", summary_txt_file_path="C:/AvalancheExeDir/Summary_Results.txt", overwrite=True):
        """
        Analzye the Avalanche test results goodput

        args = {
                    avalanche_test_name: the Avalanche test name (e.g. SM040_CSLAG-4_Data_Verification-Avalanche) - really probably should be a class variable
                    mode: this is a string designator that aids in indicating what data to fetch from the db where the results live (default: uses run id, test name, slot, pon) - if use something else, need to define it (e.g. slot then need to define the slot). options: [SM|SLOT]
                    summary_txt_file_path: location to generate the summary results text file (e.g. C:/AvalancheExeDir)
                    min_goodput: threshold value for the minimum acceptable goodput rate (e.g. 0.85)
                    overwrite: if True overwrite the Summary_Results.txt file; else, append
                }

        #fetch results from db
        #perform calculations to get pass/fail values and return/print out/log this information
        #build out summary results text file
        #publish the results of the calculations to db


        Calculations:
        goodPutCumRcv/Bytes Received (Mbps) - return value as is and as a percent and report pass/fail msg with threshold %
        if throughput < 0 need to notify and throw some fail msgs/logs
        "you've recently achieved saint hood and are now entering a flux in which your throughput values are > 100 % - consult your physician"
        """

        ##########################
        #WRITING SUMMARY FILE
        ##########################
        """

        In the middle, there was retVal + vlanMsg
            retVal = "" initially
            then, retVal = retVal + vlanMsg where vlanMsg is something like: 
                -"OK: Goodput for vlan [query testResults vlan($i)] is $thruputMB (KB) or [format %.2f [expr $value * 100]]$percent which is greater than or equal to [expr $minGoodput * 100]$percent"
                -"Error: Goodput for vlan [query testResults vlan($i)] is $thruputMB (KB) or [format %.2f [expr $value * 100]]$percent which is less than [expr $minGoodput * 100]$percent"
                -"Info: No Goodput for VLAN [query testResults vlan($i)]"   ---> indicates throughput results were < 0 all of them

        """

        #db initialize variables - this needs to be more global/encrypted
        db_ip = "10.21.1.181"
        db_port = 3306
        db_username = "pqgen"
        db_pwd = "pqgen"
        #db Avalanche result pull variables
        db_database_traffic = "trafficResults"
        db_table_avalanche_test_results = "Avalanche_Test_Results"
        db_traffic = database.Database(db_ip, db_port, db_database_traffic, db_username, db_pwd)

        #connect to db
        db_traffic.db_connect()

        #fetch results from db based on a 'mode'
        if mode.lower() == "sm":
            #fetch with test_run id and avalanche_test_name
            sql_query = "SELECT * FROM `Avalanche_Test_Results` WHERE `testRun` LIKE '{0}' AND `testName` LIKE '{1}' ORDER BY `vlan`".format(self.test_run, avalanche_test_name)
        elif mode.lower() == "slot":
            #fetch with test_run id, avalanche_test_name, and slot
            sql_query = "SELECT * FROM `Avalanche_Test_Results` WHERE `testRun` LIKE '{0}' AND `testName` LIKE '{1}' AND `slot` LIKE '{2}' ORDER BY `vlan`".format(self.test_run, avalanche_test_name, str(slot))
        else:
        #fetch with test_run id, avalanche_test_name, slot, and pon
            sql_query = "SELECT * FROM `Avalanche_Test_Results` WHERE `testRun` LIKE '{0}' AND `testName` LIKE '{1}' AND `slot` LIKE '{2}' AND `pon` LIKE '{3}' ORDER BY `vlan`".format(self.test_run, avalanche_test_name, str(slot), str(pon))

        #pull the results and verify you get some - if no results found then raise an assertion and throw log msg
        logging.info("[DB.RESULTS]: SQL QUERY: {0}".format(sql_query))

        #fetch the data
        query_response = db_traffic.db_pull(sql_query)
        row_count = query_response[0]

        #throw an error if no data is retrived from the database
        #print "Row count: " + query_response[0]
        if row_count == 0:
            logging.warning("[DB.RESULTS]: db: {0}; db_table: {1} - No Avalanche test results records retrieved from using SQL query {2}".format(db_database_traffic, db_table_avalanche_test_results, sql_query))
            AssertionError("[DB.RESULTS]: db: {0}; db_table: {1} - No Avalanche test results records retrieved from using SQL query {2}".format(db_database_traffic, db_table_avalanche_test_results, sql_query))
        #print "SQL Response: " + str(query_response[1])

        output = list(query_response[1])
        min_goodput = min_goodput * 100
        #print output
        
         #build out Avalanche summary results txt file
        with open(my_summary_file, summary_options) as summary_file:
            #write Summary_Results.txt header
            summary_file.write("##################### Analysis of Avalanche Good Put results per VLAN ######################\n")

            #now loop over each row of data
            for row in output:

                #do some math to get desired values in Mbps
                #print row
                bytes_received = row[8] * 8.0 #Mbps
                goodput_cum_received = row[9]
                goodput_avg_received_rate = row[10]
                test_name = row[2]
                outer_vlan = row[3]
                inner_vlan = row[4]

                
                goodput =  round((goodput_cum_received / bytes_received) * 100, 2) #percent
                

                # print "min goodput: " + str(min_goodput)
                # print "Percent goodput: " + str(goodput) + "%"
                # print "bytes received: " + str(bytes_received)
                # print "goodput_cum_received: " +  str(goodput_cum_received)
                # print "goodput_avg_received_rate: " + str(goodput_avg_received_rate)
                # print "testName: " + str(test_name)
                # print "outer vlan: " + str(outer_vlan)
                # print "inner vlan: " + str(inner_vlan)

                #print out pass/fail criteria with info (or just fail) and write to the file or create lists with pass/fail criteria and loop over it and then write it all at the end
                if goodput >= min_goodput:
                    #then we passed, not going to print anything but will log the throughput in Summary_Results.txt file
                    if inner_vlan == 0:
                        summary_output = "[PASS] VLAN: {0} - Percent Goodput: {1}%; Expected Percent Goodput: {2}%".format(outer_vlan, goodput, min_goodput)
                    else:
                        summary_output = "[PASS] VLAN: {0}/{1} - Percent Goodput: {2}%; Expected Percent Goodput: {3}%".format(outer_vlan, inner_vlan, goodput, min_goodput)
                else:
                    #we failed, print/log failures
                    if inner_vlan == 0:
                        summary_output = "[FAIL] VLAN: {0} - Percent Goodput: {1}%; Expected Percent Goodput: {2}%".format(outer_vlan, goodput, min_goodput)
                    else:
                        summary_output = "[FAIL] VLAN: {0}/{1} - Percent Goodput: {2}%; Expected Percent Goodput: {3}%".format(outer_vlan, inner_vlan, goodput, min_goodput)
                print summary_output

            #define config file
            my_summary_file = summary_txt_file_path

            if overwrite:
                #then set open options to 'w'
                summary_options = 'w'
            else:
                #then set open options to 'a'
                summary_options = 'a'
            
            #write Summary_Results.txt footer
            summary_file.write("##################### Analysis of Avalanche Good Put results per VLAN Completed #############\n")

        #close db session
        db_traffic.db_connect()


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
    testbed_db = "PQ2E-NODE1_S3"
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
    instance.force_reserve_ports(True)
    # # #set the Avalanche license file
    # instance.set_license_file(license_file)
    # # #set the Avalanche results output directory
    # instance.set_output_dir(output_dir)
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
    instance.start()

    ###########ANALYSIS##########
    # get list of client result directories - multiple cores
    filenames = instance.get_directories()
    #open up the hostStats.csv within the client dirs, filter, get data, post to db
    instance.get_results_and_post_to_db(testbed_db, filenames, avalanche_test_name)
    #modding this for dev:
    #instance.get_results_and_post_to_db(testbed_db, ['client-subtest_0_core1'], avalanche_test_name)
    #could allow pass in primary key id value for test run
    instance.analyze_goodput(avalanche_test_name, mode="slot", slot=3)

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

    """