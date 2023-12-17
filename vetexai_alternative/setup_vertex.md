# Using Google Vertex AI for this course

1. go to: https://cloud.google.com/vertex-ai?hl=en
2. Start free which should give you $300
3. Go to generative ai studio -> language and enable the Vertex AI api
4. go to: https://cloud.google.com/sdk/docs/install#mac and download the google sdk appropriate for your os
5. in your commandline after installing the sdk, run:
```
gcloud init
gcloud auth application-default login
```
6. you should now be authenticated with google cloud and be able to run the notebooks.
