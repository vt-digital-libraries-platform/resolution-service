# VTDLP Resolution Service
This service resolves VTDLP's permanent link. For example, it redirects ```http://idn.lib.vt.edu/ark:/53696/r335gm22``` to ```https://iawa.lib.vt.edu/archive/r335gm22```

## Lambda Function
* [lambda_function.py](lambda_function.py): Handle URL redirection
	* Env variables
		* Region: ```us-east-1```
		* TargetTable: ```DDBtablename```
		* Image404: ```404.jpg```

## Parameter Override
```
{"TargetTableName":"resolutiontable","Region":"us-east-1","Image404":"https://images/404.jpg"}
```

## API Gateway
* /{arklabel}/53696/{shortid}/GET
	* arklabel: ```ark:```
	* shortid: ```Noid```

## URL redirection
```
curl https://xxxxx.execute-api.us-east-1.amazonaws.com/Prod/ark:/53696/8c10n70v
```
Output
```
{"statusCode": 301, "location": "https://lib.vt.edu/}
```
