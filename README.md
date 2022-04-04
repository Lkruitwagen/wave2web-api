# wave2web-api
A basic API Flask app to serve wave2web inference.

The API is live at [https://h2ox-api.herokuapp.com/api/]. The API must be queried with a reservoir name, one of {harangi, hemavathy, kabini, krisharaja}, and the query date in YYYY-MM-DD format. See [demo.ipynb](demo.ipynb) or below for useage details.

A username and password are required. Please contact us for access!

**Useage (e.g. using Python's requests library):**

    import requests, json

    url = "https://h2ox-api.herokuapp.com/api/"

    r = requests.get(
        url = url,
        params = {"reservoir":"kabini", "date":"2014-03-03"},
        auth = ("<username>","<password>")
    )

    data = json.loads(r.text)

## Running the app
First load Google Cloud credentials from a Service Account JSON:
```
export GOOGLE_CREDENTIALS=$(cat credentials.json)
export REDIS_HOST=...
export REDIS_PORT=...
export REDIS_PW=...
```
```
USERNAME=... USERPASSWORD=... uvicorn app:app --port=5111 --reload
```

## Running with Docker
```
docker build -t h2ox-api .
```

```
docker run \
  -e GOOGLE_CREDENTIALS="$GOOGLE_CREDENTIALS" \
  -e REDIS_HOST="$REDIS_HOST" \
  -e REDIS_PORT="$REDIS_PORT" \
  -e REDIS_PW=$REDIS_PW \
  -e USERNAME=... \
  -e PASSWORD=... \
  -e PORT=5111 \
  -p 5111:5111 \
  h2ox-api
```

And then go to http://localhost:8000/

## Build on GCloud
```
gcloud builds submit . \
  --tag=eu.gcr.io/oxeo-main/h2ox-api \
  --ignore-file=.dockerignore
```
