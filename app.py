from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_iam as iam,
    aws_dynamodb as dynamodb,
    aws_lambda as _lambda, 
    App
)
from constructs import Construct

class SensorLoggerStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # DynamoDB Table
        table = dynamodb.Table(
            self, "SensorDataTable",
            partition_key={"name": "id", "type": dynamodb.AttributeType.STRING}
        )

        # Lambda Function
        lambda_function = _lambda.Function(
            self, "SensorDataProcessor",
            runtime=_lambda.Runtime.PYTHON_3_8,
            handler="lambda_handler.main",
            code=_lambda.Code.from_asset("lambda")
        )

        # Grant Lambda permission to write to the DynamoDB table
        table.grant_write_data(lambda_function)

        # EC2 Instance
        vpc = ec2.Vpc(self, "MyVpc", max_azs=2)
        instance = ec2.Instance(self, "Instance",
                                instance_type=ec2.InstanceType("t2.micro"),
                                machine_image=ec2.MachineImage.latest_amazon_linux(),
                                vpc=vpc,
                                key_name="crypto_stream")

        # User Data to install required software on the EC2 instance
        instance.user_data.add_commands(
            "sudo yum update -y",
            "sudo yum install -y nginx",
            "sudo service nginx start",
            "sudo chkconfig nginx on",
            # Add commands to install and configure your application
        )

app = App()
SensorLoggerStack(app, "SensorLoggerStack")
app.synth()

