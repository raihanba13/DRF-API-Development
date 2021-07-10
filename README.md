
## _Thanks for giving me the opportunity!_
This documents contains the summary of the work that has been done.

> A way to import the contents of DSRs to the DB.

url: http://127.0.0.1:8000/resources/add_resource_from_csv/
method: POST
Body: 
	file : tsv file
	dsrs_id : dsrs object id
This url can be used to upload a tsv file. ResourceViewSet.add_resource_from_csv will be called first and it will save the validated data.

> Complete the API according to the OpenAPI specification.

url: http://127.0.0.1:8000/dsrs/
method: POST
Body:  
```sh
{
    "path": "my_data/Spotify_SpotifyFamilyPlan_SGAE_ES_EUR_20200101-20200331.tsv",
    "period_start": "2020-01-01",
    "period_end": "2020-03-31",
    "status": "ingested",
    "territory": {
        "name": "SPAIN",
        "code_2": "SP"
    },
    "currency": {
        "name": "EURO",
        "code": "EUR"
    }
}
```
This method will insert data in DSR model. DSRViewSet.create method is used. By default the create method should work but as the input json is nested, we need to
do it manually. Another point is, if we use Django default api documentation page to insert data, the json keys are flatten. If we use raw json, then we need to handle the nested json.  

url: http://127.0.0.1:8000/dsrs/{id}
method: GET

This will return the dsrs object of that id.
 
url: http://127.0.0.1:8000/resources/percentile/{number}
method: GET   
Param:
    number (Path)
    territory (Query)
    period_start (Query)
    period_end (Query)

This will return the top percentile resource data.

> A form in the admin page to delete DSRs and it's contents.

An admin action delete_dsr_resource is used, this will delete the dsr data along with territory, currency and resource object.

> Tests for each api endpoint, using any preferred testing framework.

Two test files are created to test serializers and views. Admin aciton is also tested from test_urls. 

> Dockerfile

Docker file (.tar) is attached as raihan_django_app.tar inside docker delivery folder. Also Dockerfile and docker-composer.json is in the project directory.

> DSPs report DSRs containing hundreds of millions of usages. If you were to 
  deploy this solution to production, would you do any change in the database 
  or process, in order to import the usages? Which ones?
  
Since the data is big and currently there is very small relation, I think mongodb, Amazon Neptune are some solutions that should be taken into consideration. Read and write ratio is also one important parameter to consider.

    

