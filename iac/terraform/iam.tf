data "aws_iam_policy_document" "apprunner_exec_policy" {
  statement {
    actions = [
      "logs:CreateLogGroup",
      "logs:PutRetentionPolicy"
    ]
    resources = ["arn:aws:logs:*:*:log-group:/aws/apprunner/*"]
    effect    = "Allow"
  }
  statement {
    actions = [
      "logs:CreateLogStream",
      "logs:PutLogEvents",
      "logs:DescribeLogStreams"
    ]
    resources = [
      "arn:aws:logs:*:*:log-group:/aws/apprunner/*:log-stream:*"
    ]
    effect = "Allow"
  }
  statement {
    actions = [
      "events:PutRule",
      "events:PutTargets",
      "events:DeleteRule",
      "events:RemoveTargets",
      "events:DescribeRule",
      "events:EnableRule",
      "events:DisableRule"
    ]
    resources = ["arn:aws:events:*:*:rule/AWSAppRunnerManagedRule*"]
    effect    = "Allow"
  }
}
