# from aws_cdk import App, assertions
# from infra.infra_stack import MentorMatchStack
#
#
# def get_template():
#     app = App()
#     stack = MentorMatchStack(app, "infra")
#     return assertions.Template.from_stack(stack)
#
#
# def test_sqs_queue_created():
#     assert "AWS::SQS::Queue" in get_template()
#
#
# def test_sns_topic_created():
#     assert "AWS::SNS::Topic" in get_template()
