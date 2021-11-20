# An automonous solution for importing/updating Amazon Translate Custom Terminology in all supported regions

NOTE:This doc and relative code had been updated after the new feature ["Amazon Translate now enables multidirectional custom terminology"](https://aws.amazon.com/about-aws/whats-new/2021/11/amazon-translate-enables-multidirectional-custom-terminology/) released on Nov18 2021.

## Requirements
There are one hard limit in Amazon Translate Custom Terminology Limits till 2021.11.18.:

1.Maximum number of target languages per custom terminology file is 10. 

Some customers want more than 10 languages, and only one single text covering all languages instead of multiple source text files. 

## Solution debrief
This solution decreases the burden of managing multiple source text files of Amazon Translate Custom Terminology by using autonomous processing all afterward jobs when uploading only one csv file composed of more than 10 languages columns.

In this example, there are 30 columns in the original.csv. When it is uploaded, a trigger will call lambda function1 to split it into (1+10+10)X3=63(30X3 for unidirection mode) files, then import all files to Amazon Translate Custom Terminology in all Amazon Translate supported regions respectively(regions = ['us-east-1','us-east-2','us-west-1','us-west-2','ap-east-1','ap-south-1','ap-northeast-2','ap-southeast-1','ap-southeast-2','ap-northeast-1','ca-central-1','eu-central-1','eu-west-1','eu-west-2','eu-west-3','eu-north-1'])

Chinese introduction: 客户上传一个包含30列（语言）的术语表csv文件，通过trigger触发lambda开始读取处理这个文件，分拆成为(1+10+10)*3=63个文件，然后导入到各个translate 所在region的术语表，最后使用调用代码动态根据识别出的源语言调用相对应的术语表。客户对术语表csv更改后再进行上传即可再次启动这个自动化流程。

## Step by step
Note: All stepps are executed successfully in us-east-1 region. If you want to run it in other regions, please adjust according to your destination.

### 1.create layer ‘pandas’ in lambda
Down this zip file from 
[https://raw.githubusercontent.com/khanakia/aws_lambda_python_packages/master/pandas_numpy/python%203.8/python.zip] Thanks to [khanakia](https://raw.githubusercontent.com/khanakia)

create a layer named pandas in lambda

### 2.create layer ‘boto3’ in lambda
Down this zip file from 
[https://github.com/shenshaoyong/awssample/blob/master/translate/boto3_v1-20-10_py38-aee338fb-6bc7-4237-ab71-1665f77a5511.zip] Thanks to [jeromevdl](https://github.com/jeromevdl/boto3-lambda-layer), you can visit his git to create your own boto3 layer with specific version.

create a layer named boto3 in lambda.
Q: Why build this layer?
A: Till 2021.11.21, the version of python sdk boto3 in lambda is 1.18.55, but the new feature "multidirectional custom terminology" of Translate needs the version of [1.20.4](https://github.com/boto/boto3/blob/9780362652c4e97fe523f074a50c8af2d6f9e6bb/.changes/1.20.4.json). So the latest version of 1.20.10 is used to build this layer to replace the built-in boto3.

### 3.create function1 in lambda python3.8
reference to pandas layer

create a new role, adding TranslateFullAccess and AmazonS3FullAccess policies.

[code](https://github.com/shenshaoyong/awssample/blob/master/translate/lambda_function11.py)

### 4.create bucket, folder, event notification
for example, bucket name: translate-xxxx

create a directroy named original

create a event notification: Event types：All object create events； Filters：original/, original.csv） trigger to function1

### 5.create/edit/upload csv file with utf-8 with 30 languages to the folder
such as [original.csv](https://github.com/shenshaoyong/awssample/blob/master/translate/original.csv)

en,de,tr,pt,ar,ru,fr,it,pl,cs,fi,af,sq,am,fr-CA,hy,az,bn,bs,bg,ca,zh,zh-TW,hr,gu,da,fa-AF,nl,et,fa

en-game1,de-game1,tr-game1,pt-game1,ar-game1,ru-game1,fr-game1,it-game1,pl-game1,cs-game1,fi-game1,af-game1,sq-game1,am-game1,fr-CA-game1,hy-game1,az-game1,bn-game1,bs-game1,bg-game1,ca-game1,zh-game1,zh-TW-game1,hr-game1,gu-game1,da-game1,fa-AF-game1,nl-game1,et-game1,fa-game1

en-game2,de-game2,tr-game2,pt-game2,ar-game2,ru-game2,fr-game2,it-game2,pl-game2,cs-game2,fi-game2,af-game2,sq-game2,am-game2,fr-CA-game2,hy-game2,az-game2,bn-game2,bs-game2,bg-game2,ca-game2,zh-game2,zh-TW-game2,hr-game2,gu-game2,da-game2,fa-AF-game2,nl-game2,et-game2,fa-game2

### 6.create function2 in lambda python3.8, and test all 
Use the same role in step 2, or new one with TranslateFullAccess policy.

[code](https://github.com/shenshaoyong/awssample/blob/master/translate/lambda_function22.py)


## Next action(if possible)
<1. release new code when the feature(one muilti-direction text file) releases on 2021.11.18> had been completed on 2021.11.21.

2. develop a GUI that allowing to edit csv file online.
