import functions_framework
import os
import glob
from pathlib import Path
import pandas as pd
from datetime import datetime
from google.cloud import storage


@functions_framework.http
def hello_http(request):
    
    request_json = request.get_json(silent=True)
    request_args = request.args

    get_github_data()
    get_snyk_data()
    get_gitlab_data()
    generate_csv_data()
    

    a= test()
    return a

def test():
    return 'Hello! :)'

def get_github_data():
    for x in open("./repository.txt", "r"):
        
        print("repository: "+x)
        repository = x

        os.system(f'python3 ./gh-extract.py {repository}')

        repository=repository.replace("\n",'')
        repository=repository.replace('/','_')
        repository=repository.replace('-','_')

        file_bucket= f'./out_{repository}.csv'
        file_tmp=f'out_{repository}.csv'


        upload_blob('extract-data-appsec',file_bucket,file_tmp)


def get_snyk_data():
    
    for x in open("./project_id_snyk.txt", "r"):
    
        print("project_id: "+x)
        project_id = x
        project_id=project_id.strip()


        if project_id.strip() == '5e157f37-dace-4d41-91ba-3c3430cc8f5a':
            issues = '4efa198c-68ce-49c3-b24c-e10325285171'
        
        elif project_id.strip() == '418342d6-080d-4cb4-93da-cea893bfab53':
            issues = '5b9b8a05-0d10-4f5f-9360-a552fca808da'
        
        else:
            issues = '5d2d3a90-cdac-4a63-951d-285904c71104'

        os.system(f'python3 ./snyk-extract-data.py {project_id} {issues}')

        
        project_id=project_id.replace("\n",'')
        project_id=project_id.replace('/','_')
        project_id=project_id.replace('-','_')

        file_bucket= f'./out_{project_id}.csv'
        file_tmp=f'out_{project_id}.csv'

        
        upload_blob('extract-data-appsec',file_bucket,file_tmp)


def get_gitlab_data():
    for x in open("./project_id_gitlab.txt", "r"):
    
        print("project_id: "+x)
        project_id = x

        os.system(f'python3 ./gitlab-extract-data.py {project_id}')

        project_id=project_id.replace("\n",'')
        project_id=project_id.replace('/','_')
        project_id=project_id.replace('-','_')

        file_bucket= f'./out_{project_id}.csv'
        file_tmp=f'out_{project_id}.csv'


        upload_blob('extract-data-appsec',file_bucket,file_tmp)


def generate_csv_data():
    file_list = list(Path("./").glob("*.csv"))
    li = []

    for filename in file_list:
        df = pd.read_csv(filename, index_col=0, header=0)
        li.append(df)

    df = pd.concat(li, axis=0, ignore_index=True)
    df['month_beggining'] = df['date_created'].str[:7]
    df['month_end'] = df['date_end'].str[:7]
    df['index'] = range(len(df))
    
    df = df.rename(columns={'index': 'id_vulnerability','squad': 'nm_squad', 'title': 'ds_title' , 'repository':'nm_repository', 'criticity':'in_criticity', 'date_created':'dt_created', 'date_end':'dt_closed', 'status':'st_vulnerability', 'deadline':'in_deadline', 'url_issue':'ds_url_issue', 'source_data':'nm_source_data', 'month_beggining':'cd_month_start', 'month_end':'cd_month_end'})
    
    df.to_csv('./final_csv.csv')
    print('created csv')


    generate_json_data()


def generate_json_data():

    file_tmp='final_csv.csv'

    
    df = pd.read_csv(file_tmp)
    df.pop('Unnamed: 0')
    date=datetime.today().strftime('%Y-%m-%d')
    df.to_json(f'final_csv.json', orient='records', lines=True)

    file_tmp2= f'final_csv.json'


    file_bucket= f'./{file_tmp2}'
    file_tmp=f'{file_tmp2}'



    upload_blob('appsec-data',file_bucket,file_tmp)
    
    print('finished')
   


def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"
    # The path to your file to upload
    # source_file_name = "local/path/to/file"
    # The ID of your GCS object
    # destination_blob_name = "storage-object-name"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)


    generation_match_precondition = 0

    blob.upload_from_filename(source_file_name, if_generation_match=generation_match_precondition)


    print(
        f"File {source_file_name} uploaded to {destination_blob_name}."
    )
