import json
import datetime
import boto3

class GetTimeStamps(object):

        def get_time_stamps(self,repo_id,s3_resource):

                print("Repo is is:",repo_id)
                repo_path = "s3a://gotcha/sample_data/data/repository_metadata/repo_"+repo_id+".json"
                #repo_path = repo_path.encode("utf-8")
                bucketName = "gotcha"
                key = str(repo_path)[13:]
                print("Key is",key)
                file_name = "repo_"+repo_id+".json"
                s3_resource.Bucket(bucketName).download_file(key,file_name)

                #print("Able to open timestamp files!")
                try:
                        print("Able to open timestamp files!")
                        with open(file_name, 'r') as file_data:
                                data = file_data.read()
                        json_data = json.loads(data)
                        #print(json_data)
                        if 'updated_at' in json_data:
                                timestamp = str(json_data['updated_at'])
                                timestamp = str(timestamp)
                                d = datetime.datetime.strptime(timestamp,'%Y-%m-%dT%H:%M:%SZ')
                                formatted_timestamp = "%Y-%m"
                                final = d.strftime(formatted_timestamp)
                                print("Final Date:",final)
                                return final
                        else:
                                return 'none'
                except:
                        pass


s"""
library_count = []

                        return 'none'
"""







