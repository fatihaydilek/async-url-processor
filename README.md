## async-url-processor

Async url processor example using dynamodb streams.

#### Prerequisites

* Install npm/Node js
```
   https://github.com/creationix/nvm 
```

* Install Serverless Framework
```
  npm install -g serverless
```

#### Deployment

* Get Repo
```
    git clone https://github.com/fatihaydilek/async-url-processor.git
    
    cd async-url-processor && npm install 
```

* Set Bucket Name
```
    update bucketName in serverless.yml with unique identifier
```

* Serverless Stack Deployment
```
    serverless deploy --aws-profile <aws-profile> --region <region-to-deploy>
```

#### Usage

* Make url request
```
curl -X GET '< api-endpoint >/dev/api/url?url=< request-url >'
```

* Get url with identifier
```
curl -X GET '< api-endpoint/dev/url >?identifier=<identifier-from-request>'
```

#### Clean Up

* Remove Serveless Stack:
```
    serverless remove --region <deployed-region>
```