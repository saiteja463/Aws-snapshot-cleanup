resource "aws_lambda_function" "snapshot_cleanup" {
  function_name = "snapshot-cleanup"

  role    = aws_iam_role.lambda_role.arn
  handler = "cleanup_snapshots.lambda_handler"
  runtime = "python3.11"

  filename         = "../lambda/function.zip"
  source_code_hash = filebase64sha256("../lambda/function.zip")

  timeout = 60

  vpc_config {
    subnet_ids         = [aws_subnet.private.id]
    security_group_ids = [aws_security_group.lambda_sg.id]
  }

  environment {
    variables = {
      RETENTION_DAYS = "365"
    }
  }

  depends_on = [
    aws_iam_role_policy_attachment.lambda_attach
  ]
}
