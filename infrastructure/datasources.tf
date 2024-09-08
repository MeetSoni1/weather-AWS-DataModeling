data "archive_file" "lambda" {
  type        = "zip"
  source_dir  = "Y:/projects/weather/lambda_func/weatherLambdaFunc"
  output_path = "Y:/projects/weather/lambda_func/weatherLambdaFunc.zip"
}

data "aws_iam_policy_document" "assume_role" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

data "aws_vpc" "default" {
  default = true
}