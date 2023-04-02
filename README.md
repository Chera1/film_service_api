# Main films Api service
## Local run
Firstly create env file src/core/.env with following parameters:
```shell
PROJECT_NAME - name of project
REDIS_HOST - Redis host
REDIS_PORT - Redis port
ELASTIC_HOST - Elasticsearch host
ELASTIC_PORT - Elasticsearch port
SENTRY_DSN - DSN for sentry
```
To run under uvicorn execute following commands:
```shell
uvicorn main:app --reload --host localhost --port 8009
```
To run under gunicorn execute following commands:
```shell
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornH11Worker --bind 0.0.0.0:8009
```
OpenApi documentation url: http://localhost:8009/api/openapi/

## Run in Docker
Create .env file in the root folder of project with following parameters:
```shell
PROJECT_NAME - name of project
REDIS_HOST - Redis host
REDIS_PORT - Redis port
ELASTIC_HOST - Elasticsearch host
ELASTIC_PORT - Elasticsearch port
SENTRY_DSN - DSN for sentry
```
To run api in Docker execute following command:
```shell
docker compose up --build
```
OpenApi documentation url: http://localhost/api/openapi/
