import sys
import os
import pyspark
import boto3
import pandas as pd
from timestamp import GetTimeStamps
from import_lib import GetImportedLibraries


class ProcessNotebooks(object):

	def process_each_notebook(self, file_info):
		
		print("Inside process_each_notebook function!................")		
		s3_resource = boto3.resource('s3')
       		total_data = []
		#bucket_name = "mvptrial"

		"""
        s3_resource = boto3.resource('s3')
        file_path = file_info.s3_url
        file_path = file_path.encode("utf-8")

        # strip off the starting s3a:// from the bucket
        bucket_name = os.path.dirname(str(file_path))[6:13]

        # strip off the starting s3a://<bucket_name>/ the file path
        key = str(file_path)[14:]
        file_name = os.path.basename(str(file_path))
        notebook_id = os.path.splitext(file_name)[0][3:]
		"""
		
        # Get timestamp for each notebook
		get_timestamp = GetTimeStamps()
		print("Getting Time stamps!......................")
		year_month_date = get_timestamp.get_time_stamps(str(file_info.repo_id), s3_resource)
		if year_month_date == 'none':
			total_data.append((('nolibrary','nodate'),0))
			return total_data
        

        # Get list of imported libraries for each notebook
		lib = GetImportedLibraries()
		libraries_imported = lib.get_libraries(str(file_info.nb_id),s3_resource)
		
		print("Got processed libraries!....................................................")
		
		if libraries_imported != None:
			for library in libraries_imported:
				total_data.append(((library,year_month_date),1))

		else:
			return 	
		print(total_data)
		return total_data

