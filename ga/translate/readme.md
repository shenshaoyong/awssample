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
https://raw.githubusercontent.com/khanakia/aws_lambda_python_packages/master/pandas_numpy/python%203.8/python.zip

### 2.create function1 in lambda

### 3.create bucket, folder, event notification

### 4.create/edit/upload csv file with 30 languages to the folder

### 5.create function2 in lambda, and test all 

## Next action(if possible)
未来考虑1:不分源目标的术语表发布后，上述代码调整一下即可适用。
未来考虑2:开发部署GUI在线编辑csv。
