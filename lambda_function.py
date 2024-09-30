import json
import boto3
import uuid
import os
from jinja2 import Template

s3_client = boto3.client('s3')
transcribe_client = boto3.client('transcribe', region_name='us-west-2')
bedrock_runtime = boto3.client('bedrock-runtime', 'us-west-2')


def lambda_handler(event, context):
    # Extract bucket and object information from the event
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    # Ensure the file is not recursive and is the correct file
    if key != "dialog.mp3": 
        print("This demo only works with dialog.mp3.")
        return

    try:
        # Start the transcription job
        job_name = 'transcription-job-' + str(uuid.uuid4())
        response = transcribe_client.start_transcription_job(
            TranscriptionJobName=job_name,
            Media={'MediaFileUri': f's3://{bucket}/{key}'},
            MediaFormat='mp3',
            LanguageCode='en-US',
            OutputBucketName=os.environ['S3BUCKETNAMETEXT'],
            OutputKey=f'{job_name}-transcript.json',
            Settings={'ShowSpeakerLabels': True, 'MaxSpeakerLabels': 2}
        )
    except Exception as e:
        print(f"Error occurred during transcription: {e}")
        return {'statusCode': 500, 'body': json.dumps(f"Error: {e}")}

    return {
        'statusCode': 200,
        'body': json.dumps(f"Submitted transcription job for {key} from bucket {bucket}.")
    }


def process_transcript(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    if "-transcript.json" not in key:
        print("This demo only works with *-transcript.json.")
        return

    try:
        response = s3_client.get_object(Bucket=bucket, Key=key)
        file_content = response['Body'].read().decode('utf-8')
        transcript = extract_transcript(file_content)

        summary = bedrock_summarisation(transcript)
        s3_client.put_object(
            Bucket=bucket,
            Key='results.txt',
            Body=summary,
            ContentType='text/plain'
        )
    except Exception as e:
        print(f"Error occurred: {e}")
        return {'statusCode': 500, 'body': json.dumps(f"Error occurred: {e}")}

    return {
        'statusCode': 200,
        'body': json.dumps(f"Summary created for {key} and saved to results.txt")
    }


def extract_transcript(file_content):
    transcript_json = json.loads(file_content)
    output_text = ""
    current_speaker = None

    items = transcript_json['results']['items']
    for item in items:
        speaker_label = item.get('speaker_label', None)
        content = item['alternatives'][0]['content']
        if speaker_label and speaker_label != current_speaker:
            current_speaker = speaker_label
            output_text += f"\n{current_speaker}: "
        output_text += f"{content} "
    return output_text


def bedrock_summarisation(transcript):
    with open('prompt_template.txt', "r") as file:
        template_string = file.read()

    data = {'transcript': transcript, 'topics': ['charges', 'location', 'availability']}
    template = Template(template_string)
    prompt = template.render(data)

    response = bedrock_runtime.invoke_model(
        modelId="amazon.titan-text-express-v1",
        contentType="application/json",
        accept="*/*",
        body=json.dumps({"inputText": prompt})
    )

    summary = json.loads(response.get('body').read())['results'][0]['outputText']
    return summary
