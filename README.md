Installation instructions:
==========================

Use Python's zappa to deploy lambda application to AWS. You will need an AWS account and IAM role first.

    $ zappa deploy production

Next set up a DynamoDB table named "crypto-market-data".
Create a partition key called 'currency_code' and a sort key called 'utc_timestamp'.
Set up policies in the lambda IAM execution role to gain access to the newly created DB.

There are a few environment variables that may require configuration for proper usage:

* **LOG_LEVEL** sets the level of logging the lambda will output to Cloudwatch.
* **ENVIRONMENT** will determine whether to use DynamoDB database to store market data or a mock database for testing purposes. Choose "PROD" to use DynamoDB. Otherwise set to "TEST".

To automatically set up the lambda to trigger on a reoccuring schedule, do the following:

    $ zappa schedule production

To make updates to your existing lambda, type the following:

    $ zappa update production
