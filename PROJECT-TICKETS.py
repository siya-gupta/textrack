####Building a RESTful service that extracts expense date from a receipt by using python language########
###importing libraries###
from time import gmtime, strftime
import re
import time
from string import digits
import json
import pandas as pd
import numpy as np
import boto3
import io
from io import BytesIO
import sys
from dateutil import parser
import os
import matplotlib.pyplot as plt
%matplotlib inline
from matplotlib.pyplot import imshow
import matplotlib
matplotlib.style.use('ggplot')
from PIL import Image, ImageDraw, ImageFont
print(os.getcwd())
os.chdir("C:\Data Science\Spyder")

#####Creating method to process receipt####
def receipt_process(document, 
                    bucket = 'date-textract', 
                    display=False, upload=True, printout=False):
                      
    s3_bucket = boto3.resource('s3').Object(bucket, document)
    s3_response = s3_bucket.get()
    stream = io.BytesIO(s3_response['Body'].read())
    bucket_location = boto3.client('s3').get_bucket_location(Bucket=bucket)
    text = boto3.client('textract')
    image_binary = stream.getvalue()
    response = text.detect_document_text(Document={'Bytes': image_binary})
    dates = []
    
    for i, block in enumerate(response["Blocks"]):
        if block["BlockType"] == "LINE":
            date = re.search("[0-3]?[0-9]/[0-3]?[0-9]/(?:[0-9]{2})?[0-9]{2}", block["Text"])

            
            if date is not None: 
                dates.append(date.group())


    try :
        date = list(set(dates))[0]
        dt = parser.parse(date)
        date = dt.strftime("%Y-%m-%d")
    except :
        date = None
        
   
    if display: 
        image = Image.open(stream)
        fig, ax = plt.subplots(figsize=(5,10))
        ax.imshow(image)
        plt.show()
        
    if printout:
        print ("Document: ",document,"Date: ",date)
    
    #SAVING JSON WITH SENTIMENT TO S3
    content = {            
            'receipt' : "https://date-textract.s3-ap-southeast-1.amazonaws.com/",
            'submitted_on' : strftime("%Y-%m-%d %H:%M:%S GMT", gmtime()),
            'date' : date,
           
    }
    
    if upload: 
        boto3.client('s3').put_object(Body=json.dumps(content), Bucket=bucket, Key="textract-key"+document.replace("jpeg", "json"));
    
    return


receipt_process('receipt55.jpeg', display=True, upload=False, printout=True)


s3 = boto3.resource('s3')
bucket = s3.Bucket('date-textract')

for i, receipt in enumerate(bucket.objects.filter()):
    if ".jpeg" in receipt.key:
        if i % 1 == 0:
            receipt_process(receipt.key, printout=True, display=True)
        else:
            receipt_process(receipt.key, printout=True)
        time.sleep(2)
        
s3 = boto3.resource('s3')
content_object = s3.Object('date-textract', 'textract-keyreceipt55.json')
file_content = content_object.get()['Body'].read().decode('utf-8')
json_content = json.loads(file_content)
print(json.dumps(json_content, indent=2))

jsons = []
for extract in bucket.objects.filter():
    if ".json" in extract.key:
        content_object = s3.Object(extract.bucket_name, extract.key)
        file_content = content_object.get()['Body'].read().decode('utf-8')
        jsons.append(json.loads(file_content))
        
        
textracted-df = pd.concat([pd.DataFrame(j, index=[0]) for j in jsons], ignore_index=True)

date-col = expenses["date"]
nulls = dt.isnull().sum()

accuracy = ((513-null/))









