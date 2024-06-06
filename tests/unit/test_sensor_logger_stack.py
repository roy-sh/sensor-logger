import aws_cdk as core
import aws_cdk.assertions as assertions

from sensor_logger.sensor_logger_stack import SensorLoggerStack

def test_sqs_queue_created():
    app = core.App()
    stack = SensorLoggerStack(app, "sensor-logger")
    template = assertions.Template.from_stack(stack)

