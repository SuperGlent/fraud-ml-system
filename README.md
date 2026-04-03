# ML fraud detection system with CI/CD pipeline.

## Used technologies:

 - Airflow
 - MlFlow
 - PostrgeSQL, SQLAlchemy
 - Docker, docker-compose
 - Git/Github
 - FastAPI
 - Nginx
 - Scikit-learn, kagglehub, pandas, SMOTE (method), 
 
## About Project

Complex system with pipeline of live learning, reload and use of ml model, which detects fraud transactions. 

### About dataset

Dataset for learning was taken from kagglehub, uri: goyaladi/fraud-detection-dataset.
Analyzing dataset we could see a lot of unneccessary features and target features oversampling.

### General structure

Project is disturbed to 6 services: database, nginx server, airflow server, mlflow server, training service and application service. This structure allows us to scale our application as we need and incapsulate different modules logic from each other. Database server is running postgresql database with databases: fraud_training (for preproccessed training data), mlflow-artifacts (for collecting and saving model parametrs and logs, it's a volume), db-data (for new users transactions). Next service is nginx server whic serves index form of our transaction, and if user sends transaction with js fetch, ngin proxing request to our app service. Then airflow server. It's an independent service which allows us to run DAGs and create an acyclic pipeline for loading data and training the model. Mlflow UI gives u an opportunity to manage our models, experiments and so on. Training service is a container which just build in docker-compose file, but it' actually running in airflow DockerOperator, and we have to specify there a lot of params, such as network (trainig have to be on the same fraud-ml-system-default network, but not in main bridge) or env vars. And the last one is application service which just gives us api points for interaction.


## Docs

### How to run application on your local machine

1. First of all, you have to install docker on your machine, docker-compose should be in package as well. So then run it to set up docker daemon. Download docker desctop at: https://www.docker.com/products/docker-desktop/

2. Then you have to pull project from github, you can specify you own env variables if you want but it not neccessary.

3. When all is ready, run command:  `docker-compose up --build` anyway if you already had docker or not.
If you want to rebuild it, you could use those commands: 
```
docker-compose down --rmi all -v
docker-compose up --buld
```
to remoove all images and volumes and then build again.

4. Next steps are: in your browser go to url: http://localhost:8080 - so to the airflow, and log in with user "admin" and password "admin", or specified by you in project. Then go to DAGs and run the dag if it wasn't triggered by scheduler.

5. After successful pipeline execution, go to mlflow at http://localhost:5000 and see model metrics, train it again if you're not impressed :).

6. Then you can go to http://localhost:8000/docs, send post request to admin/reload-model and see that you have your model in production detecting frauds! You just have to fill trasaction form on http://localhost:80, and send it, you will have response if model think your transaction is fraud. Or better use this: 
`curl -X 'POST' 'http://localhost:8000/admin/reload-model' -H 'accept: application/json' -d ''`


Congratulations!!!

### Allowed hosts
- http://localhost:8080 - Airflow
- http://localhost:5000  - MlFlow
- http://localhost:80 - transaction form
- http://localhost:8000/docs - for fastapi documentation 


## Future improvements

There's still a lot of work to do to improve this app, at first I would get rid of docker-compose mounts on production,
and use COPY at Dockerfile for immutable images. In dev mode it's really more comfortable to use mounts but... 

Then I would like to write unit tests, and testing this application before it even built, snd to have some marks of how I changed a code with a new feature. 

Partiate airflow standalone to webserver, scheduler and executor. So as it's recomended in docs.

(I've pointed that I purposely left env file in git, and didn't wrote in it some path's and vars!)

Make alembic migration DAG, to improve flexibility of our app.

Set up s3 storage for mlflow artifacts.

*If you have any ideas or advices, I would be really gratefull to you for writing to my e-mail or create some push request! Thanks!*