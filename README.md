# Serverless Wiki

## Overview

A Wiki application implemented using Serverless technology

## Technology

Lambda
Cognito
S3

### CloudFormation

#### Create the stack

aws --region=us-east-1 cloudformation create-stack --stack-name ServerlessWiki --template-body "$(cat cfn.json)" --capabilities CAPABILITY_IAM && aws --region=us-east-1 cloudformation wait stack-create-complete --stack-name ServerlessWiki


#### Update the stack

aws --region=us-east-1 cloudformation update-stack --stack-name ServerlessWiki --template-body "$(cat cfn.json)" --capabilities CAPABILITY_IAM && aws --region=us-east-1 cloudformation wait stack-update-complete --stack-name ServerlessWiki


#### Delete the stack

aws --region=us-east-1 cloudformation delete-stack --stack-name ServerlessWiki && aws --region=us-east-1 cloudformation wait stack-delete-complete --stack-name ServerlessWiki


### Generate the JS client

sudo docker run --rm -v ${PWD}:/local swaggerapi/swagger-codegen-cli generate -i /local/swagger.yaml -l javascript-closure-angular -o /local/web/js/wikiapi
sudo docker run --rm -v ${PWD}:/local swaggerapi/swagger-codegen-cli generate -i /local/swagger.yaml -l javascript -o /local/web/js/wikiapi
