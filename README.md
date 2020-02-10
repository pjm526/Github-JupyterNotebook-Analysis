# Jupyer Trends

A data pipeline tool to analyze most popular libraries actively used in publicly available Jupyter Notebooks on Github given a problem domain and recommend popular Github users who follow code modularity as well as have sufficient hands-on experience in these popular libraries.

# Overview
With a massive volume of data being available to us, people are increasingly turning towards Data Science to make sense of this data and put it to effective use. Python being the most popular language these days, a wide variety of tools and libraries are available. However, budding data science fellows face the struggle of identifying which tools to use given a problem and getting access to the right resources to apply these tools in an efficient manner.

My project is an attempt to shorten this searching space by 
* Identifying the most popular tools used in various Data Science fields right from Data collection to visualizations.
* Recommending popular users on github who use these tools in their notebooks and also follow a modular way of writing code.

This tool also serves a dual purpose as recruiters can consider these recommended Github users as their potential future employees! 

# Dataset
Around July 2017, a team in the Design Lab at UC San Diego queried, downloaded, and analyzed publicly available Jupyter Notebooks on GitHub. According to their analysis this was about 95% of all Jupyter Notebooks available on public repositores on GitHub till date. 
The dataset is a combination of the following files:
* 1.25 million Jupyter Notebooks
* Json files with metadata for each Jupyter notebook
* Json files containing metadata for each of the nearly 200,000 public repositories with these Jupyter Notebook
* README files for nearly 150,000 repositories containing a Jupyter Notebook and csv files summarizing and indexing the notebooks, repositories, and READMEs

[Dataset Link](https://library.ucsd.edu/dc/object/bb2733859v)

