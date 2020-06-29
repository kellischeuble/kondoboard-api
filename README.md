# kondoboard-ds

This repo contains the Data Science API for Kondoboard, a platform that allows Lambda School students to browse, save, and track job postings during the job hunt. 

## Table of Contents
- [Diagrams](#diagrams)
- [Install](#install) 
- [Usage](#usage)
- [Testing](#testing)
- [API](#api)
- [Future Features]
- [License](#license)


## Diagrams
We created C4 diagrams to communicate the software architecture

### Context
![Context](./diagrams/kondo_context.svg)
### Container
![Container](./diagrams/kondo_container.svg)

## Install
```
pip install -r requirements.txt
```
## Usage
```
uvicorn main:app --reload
```
## Testing
```
pytest
```
## API

[FastAPI - Swagger documentation](http://kondoboard-ds-environment.eba-u7c3zdzn.us-east-1.elasticbeanstalk.com/docs)

## Future Features
- Allow users to search jobs by experience level. Currently there is just a penalty on all job results for anything that has master, senior, and lead in the title.
- Allow users to select a radius they want to search in
- Take user data to help improve job results (ex: Suggest jobs based on job listings that they have saved/applied to before)
- Automatically remove older jobs from database (by inserted date)
- Find a way to prevent multiple job postings from being stored in the cluster (ex: JobSearcher makes people repost every couple of days, so there are a lot of job postings that are reposts. maybe cross check with the link and the title)
- Autocomplete with Elasticsearch

## License
![License](./LICENSE)
