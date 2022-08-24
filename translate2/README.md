# A python sample for get_metric_statistics_of_aws_translate_from_cloudwatch 
API for python
[https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.Client.get_metric_data](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.Client.get_metric_data)

	import boto3	
	from datetime import datetime, timezone	
	client = boto3.client(‘cloudwatch’)	
	response = client.get_metric_statistics(
	    Namespace=‘AWS/Translate’,
	    MetricName=‘CharacterCount’,
	    Dimensions=[
	        {
	            ‘Name’: ‘LanguagePair’,
	            ‘Value’: ‘en-zh’
	        },
	        {
	            ‘Name’: ‘Operation’,
	            ‘Value’: ‘TranslateText’
	        }
	    ],
	    StartTime=datetime(2022, 7, 21),
	    EndTime=datetime(2022, 8, 23),
	    Period=2592000,
	    Statistics=[
	        ‘Sum’,
	    ],
	    Unit=‘Count’
	)
	print(response)


result：

	{'Label': 'CharacterCount', 'Datapoints': [{'Timestamp': datetime.datetime(2022, 8, 20, 0, 0, tzinfo=tzutc()), 'Sum': 566.0, 'Unit': 'Count'}, {'Timestamp': datetime.datetime(2022, 7, 21, 0, 0, tzinfo=tzutc()), 'Sum': 1907.0, 'Unit': 'Count'}], 'ResponseMetadata': {'RequestId': '13a2be49-abe5-4ec5-b0a3-1c97b5682195', 'HTTPStatusCode': 200, 'HTTPHeaders': {'x-amzn-requestid': '13a2be49-abe5-4ec5-b0a3-1c97b5682195', 'content-type': 'text/xml', 'content-length': '625', 'date': 'Mon, 22 Aug 2022 04:38:21 GMT'}, 'RetryAttempts': 0}}


# API for Go

[https://docs.aws.amazon.com/sdk-for-go/api/service/cloudwatch/#CloudWatch.GetMetricStatistics](https://docs.aws.amazon.com/sdk-for-go/api/service/cloudwatch/#CloudWatch.GetMetricStatistics)
