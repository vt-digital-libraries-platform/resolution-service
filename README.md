# VTDLP Resolution Service

This project contains source code and supporting files for a serverless application - VTDLP resolution service. This service resolves VTDLP's permanent link. For example, it redirects ```http://idn.lib.vt.edu/ark:/53696/kr10gt01``` to ```https://iawa.lib.vt.edu/archive/kr10gt01```.

The application uses several AWS resources, including Lambda functions and an API Gateway API. These resources are defined in the `template.yaml` file in this project.

## Lambda Function
* [app.py](apps/app.py): Handle URL redirection

## API Gateway
* ```GET``` https://xxxx.execute-api.us-east-1.amazonaws.com/Prod/{arklabel}/53696/{shortid}
	* arklabel: ```ark:```
	* shortid: ```Noid```

## DynamoDB Table
* [Table Schema](example/table_schema.json)
* [Sample record](example/record.json)


### Deploy VTDLP Resolution Service application using CloudFormation stack
#### Step 1: Launch CloudFormation stack
[![Launch Stack](https://cdn.rawgit.com/buildkite/cloudformation-launch-stack-button-svg/master/launch-stack.svg)](https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/new?&templateURL=https://vtdlp-dev-cf.s3.amazonaws.com/7db2bd3b29f387d3ea3639726f7e535c.template)

Click *Next* to continue

#### Step 2: Specify stack details

| Name | Description |
|:---  |:------------|
| Stack name | any valid name |
| TargetTable | a DynamoDB table |
| Image404 | 404 Image URL |
| REGION | a valid AWS region. e.g. us-east-1  |

#### Step 3: Configure stack options
Leave it as is and click **Next**

#### Step 4: Review
Make sure all checkboxes under Capabilities section are **CHECKED**

Click *Create stack*

### Deploy VTDLP Resolution Service application using SAM CLI

To use the SAM CLI, you need the following tools.

* SAM CLI - [Install the SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
* [Python 3 installed](https://www.python.org/downloads/)
* Docker - [Install Docker community edition](https://hub.docker.com/search/?type=edition&offering=community)

To build and deploy your application for the first time, run the following in your shell:

```bash
sam build --use-container
```

Above command will build the source of the application. The SAM CLI installs dependencies defined in `requirements.txt`, creates a deployment package, and saves it in the `.aws-sam/build` folder.

To package the application, run the following in your shell:
```bash
sam package --output-template-file packaged.yaml --s3-bucket BUCKETNAME
```
Above command will package the application and upload it to the S3 bucket you specified.

Run the following in your shell to deploy the application to AWS:
```bash
sam deploy --template-file packaged.yaml --stack-name STACKNAME --s3-bucket BUCKETNAME --parameter-overrides 'TargetTableName=resolutiontable Region=us-east-1 Image404=https://images/404.jpg' --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM --region us-east-1
```

## Postdeployment
* URL redirection
```
curl https://xxxxx.execute-api.us-east-1.amazonaws.com/Prod/ark:/53696/kr10gt01
```
* Output
```
{"statusCode": 301, "location": "https://iawa.lib.vt.edu/archive/kr10gt01"}
```

ps. Setting up custom domain names (e.g. http://idn.lib.vt.edu ) for REST APIs. [Guide](https://docs.aws.amazon.com/apigateway/latest/developerguide/how-to-custom-domains.html)

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```bash
aws cloudformation delete-stack --stack-name resolution-service
```
