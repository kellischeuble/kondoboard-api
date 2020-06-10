import requests
import json
import os
import boto3
from requests_aws4auth import AWS4Auth
from elasticsearch import Elasticsearch, RequestsHttpConnection

host = os.environ["AWS_ENDPOINT"]
region = os.environ["REGION"]

service = "es"
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(
    credentials.access_key,
    credentials.secret_key,
    region,
    service,
    session_token=credentials.token,
)

es = Elasticsearch(
    hosts=[host],
    # http_auth=awsauth,
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection,
)

def reformat(response_query):
    """
    Reformats elasticsearch query to remove extra information
    """
    print(response_query)
    data = list()
    # first three objects hold information about response
    for hit in response_query["hits"]["hits"][3:]:
        data.append(
            {
                "id": hit["_id"],
                "source_url": hit["_source"]["post_url"],
                "title": hit["_source"]["title"],
                "company": hit["_source"]["company"],
                "description": hit["_source"]["description"],
                "date_published": hit["_source"]["publication_date"],
                "location_city": hit["_source"]["location_city"],
                "location_state": hit["_source"]["location_state"],
                "geo_locat": hit["_source"]["location_point"],
            }
        )

    return {"jobs": data}


def get_all_jobs():
    """Simple Elasticsearch query that will return all jobs"""

    query = json.dumps({"query": {"match_all": {}}})

    response = es.search(body=query)
    reformatted = reformat(response)

    return reformatted


def search_all_locations(search):
    """
    Query to use if user does not specify a location
    Does a multi_match for the search string in the 
    description and title field
    """

    query = json.dumps(
        {
        "query": {
            "multi_match" : {
            "query": search, 
            "fields": [ "title", "description", "tags" ] 
            }
        }
        }
    )
    response = es.search(index="jobs", body=query)
    return reformat(response)


def search_city_state(search, city, state):
    """
    Query to call if user specifies the location 
    they want to search in. 
    
    Currently using "should" clause, so the locations 
    do not HAVE to match up-
    will change this later when we get more jobs in.
    """

    query = json.dumps(
        {
            "query": {
                "bool": {
                    "must": [
                        {"multi_match": {
                                "query": search,
                                "fields": ["description", "title", "tags"],
                                }},
                        {
                            "match": {"location_state": state}
                        }               
                    ],
                    "should": [
                        {"match": {"location_city": city}}
                    ],
                }
            }
        }
    )

    response = es.search(index="jobs", body=query)
    reformatted = reformat(response)

    return reformatted


def search_state(search, state):
    """
    Query to use if user just specifies the state
    that they want to search in
    """

    query = json.dumps(
        {
            "query": {
                "bool": {
                    "must": [
                        {
                            "multi_match": {
                                "query": search,
                                "fields": ["description", "title", "tags"],
                            }
                        },
                        {
                            "match": {"location_state": state}
                        }    
                    ],
                }
            }
        }
    )

    response = es.search(body=query)
    reformatted = reformat(response)

    return reformatted

def search_user(skills):
    """

    """
    query = json.dumps(
        {
        "query": {
            "multi_match" : {
            "query": skills, 
            "fields": [ "title", "description", "tags" ] 
            }
        }
        }
    )
    response = es.search(index="jobs", body=query)
    return reformat(response)

def search_user_state(skills, state):
    """

    """
    query = json.dumps(
    {
        "query": {
            "bool": {
                "must": [
                    {
                        "multi_match": {
                            "query": skills,
                            "fields": ["description", "title", "tags"],
                        }
                    },
                    {
                        "match": {"location_state": state}
                    }    
                ],
            }
        }
    }
    )

    response = es.search(body=query)
    return reformat(response)

def search_user_city_state(skills, city, state):
    """
    Query to call if user specifies the location 
    they want to search in. 
    
    Currently using "should" clause, so the locations 
    do not HAVE to match up-
    will change this later when we get more jobs in.
    """

    query = json.dumps(
        {
            "query": {
                "bool": {
                    "must": [
                        {"multi_match": {
                                "query": skills,
                                "fields": ["description", "title", "tags"],
                                }},
                        {
                            "match": {"location_state": state}
                        }               
                    ],
                    "should": [
                        {"match": {"location_city": city}}
                    ],
                }
            }
        }
    )

    response = es.search(index="jobs", body=query)
    reformatted = reformat(response)

    return reformatted