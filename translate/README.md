# An automonous solution for importing/updating Amazon Translate Custom Terminology in all supported regions

## Requirements
There are two hard limits in Amazon Translate Custom Terminology Limits till 2021.11.3.:
1.Maximum number of target languages per custom terminology file is 10. 
2.A single source text(csv|tmx) is used for each term, but there can be multiple target terms, one for each language, as long as the target and source language can be used. 

Some customers want more than 10 languages, and only one single text covering all languages instead of multiple source text files. 

## Solution debrief
This solution decreases the burden of managing multiple source text files of Amazon Translate Custom Terminology by using autonomous processing all afterward jobs when uploading only one csv file composed of more than 10 languages columns.
In this example, there are 30 columns.

Chinese introduction: 客户上传一个包含30列（语言）的术语表csv文件，通过trigger触发lambda开始读取处理这个文件，分拆成为30*3个文件，然后导入到各个translate 所在region的术语表，最后使用调用代码动态根据识别出的源语言调用相对应的术语表。客户对术语表csv更改后再进行上传即可再次启动这个自动化流程。

## Step by step
Note: All stepps are executed successfully in us-east-1 region. If you want to run it in other regions, please adjust according to your destination.

### 1.create layer in lambda
Down this zip file from 
[https://raw.githubusercontent.com/khanakia/aws_lambda_python_packages/master/pandas_numpy/python%203.8/python.zip] Thanks to khanakia
create a layer named pandas in lambda
### 2.create function1 in lambda
reference to pandas layer
create a new role, adding TranslateFullAccess and AmazonS3FullAccess policies.
[code]()

### 3.create bucket, folder, event notification
for example, bucket name: translate-xxxx
create a directroy named original
create a event notification: Event types：All object create events； Filters：original/, original.csv） trigger to function1

### 4.create/edit/upload csv file with utf-8 with 30 languages to the folder
such as [original.csv]()
en,de,tr,pt,ar,ru,fr,it,pl,cs,fi,af,sq,am,fr-CA,hy,az,bn,bs,bg,ca,zh,zh-TW,hr,gu,da,fa-AF,nl,et,fa
en-game1,de-game1,tr-game1,pt-game1,ar-game1,ru-game1,fr-game1,it-game1,pl-game1,cs-game1,fi-game1,af-game1,sq-game1,am-game1,fr-CA-game1,hy-game1,az-game1,bn-game1,bs-game1,bg-game1,ca-game1,zh-game1,zh-TW-game1,hr-game1,gu-game1,da-game1,fa-AF-game1,nl-game1,et-game1,fa-game1
en-game2,de-game2,tr-game2,pt-game2,ar-game2,ru-game2,fr-game2,it-game2,pl-game2,cs-game2,fi-game2,af-game2,sq-game2,am-game2,fr-CA-game2,hy-game2,az-game2,bn-game2,bs-game2,bg-game2,ca-game2,zh-game2,zh-TW-game2,hr-game2,gu-game2,da-game2,fa-AF-game2,nl-game2,et-game2,fa-game2

### 5.create function2 in lambda, and test all 
[code]()

## Next action(if possible)
1. release new code when the feature(one muilti-direction text file) releases
2. develop a GUI that allowing to edit csv file online.
