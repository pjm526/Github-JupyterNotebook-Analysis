from __future__ import print_function
from pyspark.sql import SparkSession
from spark_processing import spark_processing

def final_run():
	
	
	parallel_processing = spark_processing()
	print("Converting file urls list to file urls dataframe .................................")
	files_urls_df = parallel_processing.nb_repo_df()
	files_urls_df.show(10)


	# Process each notebook file to get library,timestamp,users
	print("Sending files to process..................................")
	processed_df = parallel_processing.NotebookMapper(files_urls_df)
	print("Files Processed")
	processed_df.show()
	return processed_df


df = final_run()
print("Gotcha!")
df.show(10)

df.write.format("jdbc") \
    .option("url", "jdbc:postgresql://ec2-34-196-79-237.compute-1.amazonaws.com:5432/testing") \
    .option("dbtable", "public.mvptrial") \
    .option("user", "ubuntu") \
    .option("password", "password!") \
    .option("driver","org.postgresql.Driver") \
    .mode("append").save()


