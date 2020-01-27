import json
import boto3
import datetime
import os
import pyspark
from pyspark.sql import SparkSession,SQLContext
from pyspark import SparkConf, SparkContext


class GetImportedLibraries():

    def get_libraries(self,nb_id,s3_res):
        """
        Given a filename, returns a list of modules imported by the program.
        This program does not run the code, so import statements
        in if/else or try/except blocks will always be included.
        """

	print("Inside get_libraries function!..........................................")
	print("nb_id",nb_id)
	#s3_res = boto3.resource('s3')
	notebook_path = "s3a://gotcha/sample_data/data/notebooks/nb_"+ nb_id+".ipynb"
	#notebook_path = notebook_path.encode("utf-8")
	bucket_name = "gotcha"
	key = str(notebook_path)[13:]
	print("Key is",key)
	file_name = "nb_"+nb_id+".ipynb"
        s3_res.Bucket(bucket_name).download_file(key,file_name)

        importedItems = []
        
	# Check for import statements in each line in the notebook


	with open(file_name, 'r') as pyFile:
		for line in pyFile:
			if line == []:
				pass
			else:
		    # ignore comments
				line = line.strip().strip(',').strip('"').strip('n').strip('\\').partition("#")[0].partition(" as ")[0].split(' ')
		    # get libraries from 'import library1, library2,...' statements
				print("Liness.......................")
				if line[0] == "import":
					for imported in line[1:]:
						# remove commas - this doesn't check for commas if
						# they're supposed to be there!
						imported = imported.strip(",")
						if "." in imported:
							imported = imported.split('.')[0]
						else:
							pass
						importedItems.append(imported)
						
						print(".................",importedItems)
				# get imported libraries from 'from library import ...' statements
				if len(line) > 2:
					if line[0] == "from" and line[2] == "import":
						imported = line[1]
						if "." in imported:
							imported = imported.split('.')[0]
						else:
							pass
						importedItems.append(imported)
						print("--------------------",importedItems)
	print("Libraries",importedItems)
	importedItems = list(dict.fromkeys(importedItems))
	print("libs",importedItems)

	return importedItems
