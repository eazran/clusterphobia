import os
import json
from pprint import pprint

#
# This dictionary contains Key-Value of the servers and the application path on each
# Debug value
server_dictionary={"server1":"C:\\workspace\\clusterphobia\\resources\\server1","server2":"C:\\workspace\\clusterphobia\\resources\\server2"}
#
configuration_map=[]

for server in server_dictionary:
	
	print "Processing configuration files on", server
	current_server_parameters={}
	current_environment_name=""
	current_environment_parameters={}
	current_application_parameters={}
	
	for root, dirs, files in os.walk(server_dictionary[server], topdown=True):			
		for config_file_name in files:
			if (config_file_name.endswith(".conf")):
				config_file_path = os.path.join(root, config_file_name)				
				print "Fetching configuration parameters in", config_file_path
				config_file_handle = open(config_file_path, 'r')				
				try:
					config_data = json.load(config_file_handle)
										
					if (config_file_name == "cluster.conf"):
						current_server_parameters=config_data
						
					elif (config_file_name == "env.conf"):
						current_environment_name=root[len(server_dictionary[server])+1:]
						current_environment_parameters=config_data						
						
					elif (config_file_name.startswith("app")):
						current_application_name=config_file_name[:-5]						
						current_application_parameters=current_server_parameters
						current_application_parameters.update(current_environment_parameters)
						current_application_parameters.update(config_data)
						
						configuration_map.append({server:{current_environment_name:{current_application_name:current_application_parameters}}})

						# Clean application parameters before next loop
						current_application_name=""
						current_application_parameters=""
						
				finally:
					config_file_handle.close()					
	
pprint(configuration_map)
