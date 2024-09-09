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
  name = "weather-eventbridge-policy"
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

  schedule_expression = "cron(0 9 * * ? *)" # everyday

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
        Effect = "Allow"
        Action = [
          "rds:DescribeDBInstances",
          "rds:Connect"
        ]
        Resource = "arn:aws:rds:*:*:*:*"
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
  filename      = "/weatherLambdaFunc.zip"
  function_name = "weather-lambda"
  role          = aws_iam_role.iam_for_lambda.arn
  handler       = "lambda_function.lambda_handler"

  # 'data' Defined in datasources.tf file
  source_code_hash = data.archive_file.lambda.output_base64sha256

  runtime = "python3.12"
}

# Parameter Store

variable "openWeatherApiKey" {
  description = "open weather map API key"
  type        = string
}

resource "aws_ssm_parameter" "tf_local_parameter_store" {
  name        = "/weather/tf_openWeatherAPI"
  description = "API Key"
  type        = "SecureString"
  value       = var.openWeatherApiKey
}

# RDS
variable "rds_db_username" {
  type = string
}

variable "rds_db_password" {
  type = string
}

resource "aws_db_instance" "mytrialdb" {
  identifier                      = "weatherdb-id"
  allocated_storage               = 20
  storage_type                    = "gp2"
  backup_retention_period         = 1
  db_name                         = "***"
  engine                          = "mysql"
  engine_version                  = "8.0.39"
  instance_class                  = "db.t3.micro"
  username                        = var.rds_db_username
  password                        = var.rds_db_password
  parameter_group_name            = "default.mysql8.0"
  publicly_accessible             = false
  skip_final_snapshot             = true
  enabled_cloudwatch_logs_exports = ["error", "general"]

  # Adding VPC Security Group to allow access
  vpc_security_group_ids = [aws_security_group.rds_sg.id]
}


# Create a Security Group for RDS Access
resource "aws_security_group" "rds_sg" {
  name        = "rds_sg"
  description = "Allow access to MySQL RDS instance"
  vpc_id      = data.aws_vpc.default.id # Update with your VPC ID

  ingress {
    from_port   = 3306
    to_port     = 3306
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # limited access to specific IP ranges while provisioning
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Quicksight Permissions

resource "aws_quicksight_data_source" "rds_mysql" {
  data_source_id = "rds-mysql-weatherdatasource"
  name           = "RDS Weather Data Source"
  type           = "RDS"

  data_source_parameters {
    rds_instance_id = aws_db_instance.mytrialdb.id
    database        = "***"
  }

  credentials {
    username = "***"
    password = "***"
  }

  permissions {
    principal = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/service-role/aws-quicksight-service-role-v0" # QuickSight Role ARN
    actions   = ["quicksight:DescribeDataSource"]
  }
}