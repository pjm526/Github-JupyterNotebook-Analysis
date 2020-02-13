from __future__ import print_function
#import postgres
import sys
import pyspark
from pyspark import SQLContext
from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession
from pyspark.sql import Row
from pyspark.sql.types import StructType
from pyspark.sql.types import StructField
from pyspark.sql.types import StringType
from pyspark.sql.functions import udf, expr, concat, col
from notebook_processing import ProcessNotebooks


class spark_processing(object):

    def __init__(self):
        self.spark = SparkSession \
            .builder \
            .appName("LibraryInsights") \
            .getOrCreate()

	
		#sqlContext = SQLContext(sc)

        # Add modules
        self.spark.sparkContext.addPyFile('notebook_processing.py')
        self.spark.sparkContext.addPyFile('timestamp.py')
        self.spark.sparkContext.addPyFile('import_lib.py')

        self.bucket = "gotcha"


    def nb_repo_df(self):
	print("inside the nb_repo_df function")
	df = self.spark.read.format("csv").option("header", "true").load("s3a://gotcha/sample_data/data/csv/notebooks_sample.csv")
	df_selected_columns = df.select(df['nb_id'], df['repo_id'])
	print(df_selected_columns.show(10))
	return df_selected_columns


    def NotebookMapper(self,df_selected_columns):

        print('got file df ..................................')

        # Farm out jupyter notebook files to Spark workers with a flatMap and
        # aggregrate users for each month for each library
        process_notebooks = ProcessNotebooks()
        processed_rdd = df_selected_columns.rdd.flatMap(process_notebooks.process_each_notebook) \
                        .filter(lambda x: x[0][0] != 'nolibrary') \
                        .reduceByKey(lambda n,m: n+m) \
                        .map(lambda x: (x[0][0],x[0][1],x[1]))
        print('got processed rdd ..................................')

		#print(processed_rdd.collect())
        # Save processed rdd as a dataframe using the following schema:
        processed_schema = StructType([StructField("library", StringType(), False),
                                         StructField("datetime", StringType(), False ),
                                         StructField("lib_counts", StringType(), False )])
		#print("Schema processed")
        processed_df = (
            processed_rdd \
            .map(lambda x: [x[0],x[1],x[2]]) \
            .toDF(processed_schema) \
            .select("library","datetime","lib_counts")
        )
		#print(processed_df.show(5))
        return processed_df


    
