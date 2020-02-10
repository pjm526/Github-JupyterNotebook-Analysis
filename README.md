# Jupyter Trends

A data pipeline tool to analyze most popular libraries actively used in publicly available Jupyter Notebooks on Github given a problem domain and recommend popular Github users who follow code modularity as well as have sufficient hands-on experience in these popular libraries.

## Overview
With a massive volume of data being available to us, people are increasingly turning towards Data Science to make sense of this data and put it to effective use. Python being the most popular language these days, a wide variety of tools and libraries are available. However, budding data science fellows face the struggle of identifying which tools to use given a problem and getting access to the right resources to apply these tools in an efficient manner.

My project is an attempt to shorten this searching space by 
* Identifying the most popular tools used in various Data Science fields right from Data collection to visualizations.
* Recommending popular users on github who use these tools in their notebooks and also follow a modular way of writing code.

This tool also serves a dual purpose as recruiters can consider these recommended Github users as their potential future employees! 

## Dataset
Around July 2017, a team in the Design Lab at UC San Diego queried, downloaded, and analyzed publicly available Jupyter Notebooks on GitHub. According to their analysis this was about 95% of all Jupyter Notebooks available on public repositores on GitHub till date. 
The dataset is a combination of the following files:
* 1.25 million Jupyter Notebooks
* Json files with metadata for each Jupyter notebook
* Json files containing metadata for each of the nearly 200,000 public repositories with these Jupyter Notebook
* README files for nearly 150,000 repositories containing a Jupyter Notebook and csv files summarizing and indexing the notebooks, repositories, and READMEs

[Dataset Link](https://library.ucsd.edu/dc/object/bb2733859v)

## Requirements
* Python3
* [AWS CLI](https://aws.amazon.com/cli/)
* [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html#installation)

## Architecture
* [SPARK](https://blog.insightdatascience.com/simply-install-spark-cluster-mode-341843a52b88): 4 EC2 m4.large instances with (1 master 3 worker) spark cluster
* [POSTGRESQL](https://blog.insightdatascience.com/simply-install-postgresql-58c1e4ebf252): 1 EC2 m4.large instance
* [DASH](https://dash.plot.ly/installation): 1 EC2 t2.micro instance 

## Methodology

### Data Collection:
Parse and extract the urls available on UC San Diego Library Digital Collections into s3 buckets buy distributing the work among worker nodes as well.
Lambda Fucntion to unzip the zipped files inot ec2 instance and then write it to the s3 bucket using `s3.put_object()`
Loaded repository metadata to extract 'updated at:' timestamp.
Extracted notebooks ids, repository ids, github user names from the csv files and hence mapped the results to respective tables. 


### Extracting Libraries from Notebooks
Load the .ipynb notebooks which are in json format as dictionaries to make use of dictionary look up functions to access the source cells from the notebooks.Using regex functions look for keywords "import" and "from" to retrieve the libraries.

Extract timestamps from the repository metadata json files and attach it to each libraries.
`total_data.append(((library,year_month_date),1))`

Using RDD's calculate the count for each tuple crated above to get the total count.
`df = rdd.flatMap(process_notebooks.process_each_notebook) \
     .filter(lambda x: x[0][0] != 'nolibrary') \
     .reduceByKey(lambda n,m: n+m)`
     
 Store the final spark dataframe in PostgreSQL by setting up the connections.
 
 ![Library-Count-Schema](/lib-extract.png)
 
 ### Calculating Code Modularity Metrics
 
