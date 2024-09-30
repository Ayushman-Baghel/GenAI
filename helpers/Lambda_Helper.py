import boto3

class Lambda_Helper:
    def __init__(self):
        self.client = boto3.client('lambda')
        self.lambda_environ_variables = {}

    def deploy_function(self, files, function_name):
        with open(files[0], 'r') as f:
            function_code = f.read()
        self.client.create_function(
            FunctionName=function_name,
            Runtime='python3.9',
            Role='<YOUR-IAM-ROLE-ARN>',
            Handler='lambda_function.lambda_handler',
            Code={'ZipFile': function_code},
            Environment={'Variables': self.lambda_environ_variables}
        )
