import json
import urllib.parse
import boto3
import csv
import pandas as pd
import logging


from io import BytesIO

print('Loading function')

s3 = boto3.client('s3')
translate = boto3.client('translate')
df = pd.DataFrame()
original_csv = '/tmp/original.csv'
def lambda_handler(event, context):
    #print("Received event: " + json.dumps(event, indent=2))
    print(event)

    # Get the object from the event and show its content type
    bucket = event['Records'][0]['s3']['bucket']['name']
    
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    try:
        #response = s3.get_object(Bucket=bucket, Key=key)
        #print("key: " + key)
        
        s3.download_file(bucket, key, '/tmp/original.csv')
        
        df = pd.read_csv(original_csv)
        
        #print(df)

        languages = df.columns.values
        
        print(languages)
        
        languagesG1 = languages[0:10]
        languagesG2 = languages[10:20]
        languagesG3 = languages[20:30]
        df_G1 = df.drop(df.iloc[:,10:30],axis = 1) 
        df_G2 = df.drop(df.iloc[:,20:30],axis = 1) 
        df_G2 = df_G2.drop(df.iloc[:,0:10],axis = 1)
        df_G3 = df.drop(df.iloc[:,0:20],axis = 1)
        
        languagesG1 = languagesG1[::-1]
        for language in languagesG1:
            cols = list(df_G1.columns)
            cols = [cols[-1]] + cols[:-1]
            df_G1 = df_G1[cols]
            df_G1.to_csv(path_or_buf='/tmp/{}1.csv'.format(language),index=False)
            
            df_G2_tmp = df_G2.copy(deep=True)
            df_G2_tmp.insert(loc=0, column=language, value=df_G1[language])
            df_G2_tmp.to_csv(path_or_buf='/tmp/{}2.csv'.format(language),index=False)
            
            df_G3_tmp = df_G3.copy(deep=True)
            df_G3_tmp.insert(loc=0, column=language, value=df_G1[language])
            df_G3_tmp.to_csv(path_or_buf='/tmp/{}3.csv'.format(language),index=False)
            #break
        languagesG2 = languagesG2[::-1]    
        for language in languagesG2:
            cols = list(df_G2.columns)
            cols = [cols[-1]] + cols[:-1]
            df_G2 = df_G2[cols]
            df_G2.to_csv(path_or_buf='/tmp/{}2.csv'.format(language),index=False)
            
            df_G1_tmp = df_G1.copy(deep=True)
            df_G1_tmp.insert(loc=0, column=language, value=df_G2[language])
            df_G1_tmp.to_csv(path_or_buf='/tmp/{}1.csv'.format(language),index=False)
            
            df_G3_tmp = df_G3.copy(deep=True)
            df_G3_tmp.insert(loc=0, column=language, value=df_G2[language])
            df_G3_tmp.to_csv(path_or_buf='/tmp/{}3.csv'.format(language),index=False)
            #break
        languagesG3 = languagesG3[::-1]
        for language in languagesG3:
            cols = list(df_G3.columns)
            cols = [cols[-1]] + cols[:-1]
            df_G3 = df_G3[cols]
            df_G3.to_csv(path_or_buf='/tmp/{}3.csv'.format(language),index=False)
            
            df_G1_tmp = df_G1.copy(deep=True)
            df_G1_tmp.insert(loc=0, column=language, value=df_G3[language])
            df_G1_tmp.to_csv(path_or_buf='/tmp/{}1.csv'.format(language),index=False)
           
            df_G2_tmp = df_G2.copy(deep=True)
            df_G2_tmp.insert(loc=0, column=language, value=df_G3[language])
            df_G2_tmp.to_csv(path_or_buf='/tmp/{}2.csv'.format(language),index=False)
            #break
        
        #create custom terminology in all supported regions
        regions = ['us-east-1','us-east-2','us-west-1','us-west-2','ap-east-1','ap-south-1','ap-northeast-2','ap-southeast-1','ap-southeast-2','ap-northeast-1','ca-central-1','eu-central-1','eu-west-1','eu-west-2','eu-west-3','eu-north-1']
        for region in regions:
            translate = boto3.client(service_name='translate', region_name=region, use_ssl=True)
            print('import_terminology in  region: {}'.format(region))
        
            for language in languages:
                for i in [1,2,3]:
                    # Read the terminology from a local file
                    with open('/tmp/{}{}.csv'.format(language,i), 'rb') as f:
                        data = f.read()
                     
                    file_data = bytearray(data)
                    response = translate.import_terminology(
                        Name='{}{}'.format(language,i),
                        MergeStrategy='OVERWRITE',
                        Description='{}{}'.format(language,i),
                        TerminologyData={
                            'File': file_data,
                            'Format': 'CSV'
                        }
                    )
        
        try:
            for language in languages:
                response = s3.upload_file('/tmp/{}1.csv'.format(language), bucket,'{}1.csv'.format(language))
                response = s3.upload_file('/tmp/{}2.csv'.format(language), bucket,'{}2.csv'.format(language))
                response = s3.upload_file('/tmp/{}3.csv'.format(language), bucket,'{}3.csv'.format(language))
        except Exception as e:
            logging.error(e)
            return False
        return True
        
        #for line in lines:
        #    #print complete line
        #    print(line)
        #    #print index wise
        #    print(line[0], line[1])
    
    
        return response['ContentType']
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e

    