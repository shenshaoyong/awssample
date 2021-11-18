import boto3
import json
import datetime
group = 'g'
def lambda_handler(event, context):
    # TODO implement
    my_session = boto3.session.Session()
    region = my_session.region_name

    comprehend = boto3.client(service_name='comprehend', region_name=region)
    translate = boto3.client(service_name='translate', region_name=region, use_ssl=True)
    #English
    text10 = "I love you"
    text50 = "en-game45 It is raining today in Seattle .Really?50"
    text100 = "en-game45 It is raining today in Seattle .Really? en-game45 It is raining today in Seattle .Really?100"
    #German
    #text10 = "Wirklich? "
    #text50 = "de-game45 Heute regnet es in Seattle. Wirklich? 50"
    #text100 = "de-game45 Heute regnet es in Seattle. Wirklich? de-game45 Heute regnet es in Seattle. Wirklich? 100"
    languages = ['en','de','tr','pt','ar','ru','fr','it','pl','cs','fi','af','sq','am','fr-CA','hy','az','bn','bs','bg','ca','zh','zh-TW','hr','gu','da','fa-AF','nl','et','fa']

    languagesG1 = languages[0:10]
    languagesG2 = languages[10:20]
    languagesG3 = languages[20:30]
        
    loop1 = 100
    for text in [text10,text50,text100]:
        t1 = datetime.datetime.now()
        for l in range(loop1):
            languageCode = comprehend.detect_dominant_language(Text = text).get('Languages')[0].get('LanguageCode')
            if languageCode not in languages:
                print('languageCode:{} doesnot support,changed to default en'.format(languageCode))
                languageCode = 'en'
        t2 = datetime.datetime.now()
        targetLanguageCode = 'fr'
        if {languageCode,targetLanguageCode}.issubset(languagesG1):
            terminologyName = '{}1'.format(group)
        elif {languageCode,targetLanguageCode}.issubset(languagesG2):
            terminologyName = '{}2'.format(group)
        elif {languageCode,targetLanguageCode}.issubset(languagesG3):
            terminologyName = '{}3'.format(group)
        elif targetLanguageCode in languagesG1:
            terminologyName = '{}1'.format(languageCode)
        elif targetLanguageCode in languagesG2:
            terminologyName = '{}2'.format(languageCode)
        elif targetLanguageCode in languagesG3:
            terminologyName = '{}3'.format(languageCode)
        else:
            terminologyName = '{}1'.format(languageCode)
            print('targetLanguageCode:{} doesnot support'.format(targetLanguageCode))
        print('terminologyName:{} '.format(terminologyName))
        for l in range(loop1):
            result = translate.translate_text(Text=text, TerminologyNames=[terminologyName],
                    SourceLanguageCode=languageCode, TargetLanguageCode=targetLanguageCode).get('TranslatedText')
        t3 = datetime.datetime.now()
        print(text)
        print("t2-t1:",(t2 - t1)/loop1)
        print("t3-t2:",(t3 - t2)/loop1)
        print("t3-t1:",(t3 - t1)/loop1)
        print('----------------')
    return {
        'statusCode': 200,
        'body': json.dumps(result)
    }
