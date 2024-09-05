# Variables declared in .tfvars file

# Eventbridge IAM Role
resource "aws_iam_role" "eventbridge_scheduler_role" {
  name = "weather-eventbridge-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Principal = {
          Service = "scheduler.amazonaws.com"
        },
        Action = "sts:AssumeRole"
      }
    ]
  })
}

# Eventbridge Policies
resource "aws_iam_role_policy" "eventbridge_scheduler_policy" {
  name = "weather-eventbridge-lambda-schedule_policy"
  role = aws_iam_role.eventbridge_scheduler_role.id

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect   = "Allow",
        Action   = "lambda:InvokeFunction",
        Resource = aws_lambda_function.tf_local_lambda.arn
      }
    ]
  })
}

# Event bridge scheduler
resource "aws_scheduler_schedule" "tf_local_eventbidge" {
  name       = "weather-lambda-schedule"
  group_name = "default"

  flexible_time_window {
    mode = "OFF"
  }

  schedule_expression = "cron()"   # everyday

  target {
    arn      = aws_lambda_function.tf_local_lambda.arn
    role_arn = aws_iam_role.eventbridge_scheduler_role.arn

    retry_policy {
      maximum_event_age_in_seconds = 3600
      maximum_retry_attempts       = 3
    }
  }
}

# Lambda IAM Role
resource "aws_iam_role" "iam_for_lambda" {
  name               = "weather-iam-lambda-role"
  assume_role_policy = data.aws_iam_policy_document.assume_role.json
}

# Lambda Policies
resource "aws_iam_role_policy" "lambda_basic_execution" {
  name = "weather-lambda-policy"
  role = aws_iam_role.iam_for_lambda.id

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ],
        Resource = "arn:aws:logs:*:*:*"
      },
      {
        # add RDS permissions
      },
      {
        Effect = "Allow",
        Action = [
          "ssm:GetParameter"
        ],
        Resource = "arn:aws:ssm:*:*:parameter/*"
      }
    ]
  })
}

# Lambda Basic Excecution
resource "aws_lambda_function" "tf_local_lambda" {
  # Include a path.module in the filename if the file is not in the current working directory.
  filename      = "/weatherLambdaFunc.zip"
  function_name = "weather-lambda"
  role          = aws_iam_role.iam_for_lambda.arn
  handler       = "lambda_function.lambda_handler"

  # 'data' Defined in datasources.tf file
  source_code_hash = data.archive_file.lambda.output_base64sha256

  runtime = "python3.12"
}

# Parameter Store
variable "openWeatherAPI" {
  description = "open weather map API key"
  type        = string
}
resource "aws_ssm_parameter" "tf_local_parameter_store" {
  name        = "/weather/tf_openWeatherAPI"
  description = "API Key"
  type        = "SecureString"
  value       = var.openWeatherAPI
}