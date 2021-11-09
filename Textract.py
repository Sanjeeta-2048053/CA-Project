import boto3
import time
import sys

## Textract APIs used - "start_document_text_detection", "get_document_text_detection"
def InvokeTextDetectJob(s3BucketName, objectName):
    response = None
    client = boto3.client(service_name='textract', region_name='us-east-1', use_ssl=True)
    response = client.start_document_text_detection(
            DocumentLocation={
                      'S3Object': {
                                    'Bucket': s3BucketName,
                                    'Name': objectName
                                }
           })
    return response["JobId"]

def CheckJobComplete(jobId):
    time.sleep(5)
    client = boto3.client(service_name='textract', region_name='us-east-1', use_ssl=True)
    response = client.get_document_text_detection(JobId=jobId)
    status = response["JobStatus"]
    print("Job status: {}".format(status))
    while(status == "IN_PROGRESS"):
        time.sleep(5)
        response = client.get_document_text_detection(JobId=jobId)
        status = response["JobStatus"]
        print("Job status: {}".format(status))
    return status

def JobResults(jobId):
    pages = []
    client = boto3.client(service_name='textract',  region_name='us-east-1', use_ssl=True)
    response = client.get_document_text_detection(JobId=jobId)
 
    pages.append(response)
    print("Resultset page recieved: {}".format(len(pages)))
    nextToken = None
    if('NextToken' in response):
        nextToken = response['NextToken']
        while(nextToken):
            response = client.get_document_text_detection(JobId=jobId, NextToken=nextToken)
            pages.append(response)
            print("Resultset page recieved: {}".format(len(pages)))
            nextToken = None
            if('NextToken' in response):
                nextToken = response['NextToken']
    return pages

# S3 Document Data
s3BucketName = "project-textract"
documentName = "article.pdf"

# Function invokes
jobId = InvokeTextDetectJob(s3BucketName, documentName)
print("Started job with id: {}".format(jobId))
if(CheckJobComplete(jobId)):
    response = JobResults(jobId)
    f = open("output1.txt", "w")
    for resultPage in response:
        for item in resultPage["Blocks"]:
            if item["BlockType"] == "LINE":
                print ('' + item["Text"] + '')
f.close()

time.sleep(5)



#polly

def polly_service():
	polly = boto3.client(service_name='polly',region_name='us-east-1',  use_ssl=True)

	print('Starting the Polly Service')

	f = open("output.txt", "r")

	text = f.read(100)

	response = polly.synthesize_speech(OutputFormat='mp3', VoiceId='Brian',
	             Text= text)

	file = open('speech.mp3', 'wb')
	file.write(response['AudioStream'].read())
	file.close()
	print("Polly's output stored !")

polly_service()
