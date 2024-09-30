# Event-Driven AWS Lambda Function with Transcribe and Bedrock

This project contains an AWS Lambda function that is triggered by an S3 event. When an `mp3` file is uploaded to the specified S3 bucket, the Lambda function:
- Transcribes the audio file using **AWS Transcribe**.
- Summarizes the transcription using **Amazon Bedrock**.
- Stores the summary back in an S3 bucket.

## Features
- **AWS Lambda**: Serverless function handling audio transcription and summarization.
- **AWS Transcribe**: Converts uploaded `.mp3` files into text with speaker identification.
- **Amazon Bedrock**: Generates a summary of the transcribed text.
- **S3 Integration**: Automatically listens for file uploads and stores outputs.

## Project Structure
```
├── helpers/              # Helper scripts for Lambda and S3 operations
├── lambda_function.py    # Main AWS Lambda function
├── prompt_template.txt   # Template for text summarization prompt
├── requirements.txt      # Python dependencies
├── README.md             # This readme file
└── notebook.ipynb        # Jupyter notebook for local testing and demo
```

## Setup Instructions

1. **Install dependencies**:
   Make sure you have the following dependencies installed by running:
   ```bash
   pip install -r requirements.txt
   ```

2. **Deploy Lambda Function**:
   - Deploy the Lambda function using AWS SDK or from your AWS Management Console.
   - Ensure that the Lambda role has necessary permissions (S3, Transcribe, Bedrock).

3. **S3 Buckets**:
   - Create two S3 buckets: 
     - One for uploading `mp3` files.
     - One for storing the transcription results.

4. **Run the Notebook**:
   Use the provided Jupyter notebook (`notebook.ipynb`) for testing the workflow locally.

## License
MIT License
