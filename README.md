# Password Cracking Game!
This is a small 3 page websie built to take a punch!
The aim of the game is to guess the password, I littered a few clues around for peeps to find the password but battle hardend the server for brute force attacks from the nerds. 
of which we had a few.

[dashboard](https://charts.mongodb.com/charts-cracker-zorha/dashboards/5f9bdc06-8f99-4775-88f3-2a7aefdffe55)

# How?
- Bottle api
- Fancy request intercepting
- Custom redis queue
- Custom password checker
- User Caching
- Faat cluster

# I wana run on my local!
- Clone this bad boy,
- Create an env file with
  - MONGO_DB_URL=<mongo url>
  - ITS_AN_ENV_VAR_BRO=<the password>
  - REDIS_HOST=<redis host address>
- `pip install -r requirements.txt`
- `rq-worker`
- In a new terminal (or Ctrl+X if u bougee): `python main.py`
- Hit up loaclhost:5000
- Make an account on the UI
- Write your bot to hit the api (bad example in brute.py)
  
Or you can use docker (--net="host")

  
# Host this for free!
- Set up a mongodb at mongodbatlas
- Sign up at GCP for $300 credit
- Start a k8 cluster
- use the deploy scripts to start her up.

## Deploy scripts
- docker build -t gcr.io/cracker-294009/cracker:latest .
- docker run --net=host gcr.io/cracker-294009/cracker:latest
- docker push gcr.io/cracker-294009/cracker:latest
- kubectl get pods
- kubectl get service --all-namespaces           
- kubectl delete pod <pod-id>
- kubectl get pods
- kubectl rollout restart deployment bottle
