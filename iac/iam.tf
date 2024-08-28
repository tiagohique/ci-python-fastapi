resource "aws_iam_role" "app-runner-role" {
  name = "app-runner-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "tasks.apprunner.amazonaws.com" # Ajustado para o serviço correto do App Runner
        }
        Action = "sts:AssumeRole"
      }
    ]
  })

  managed_policy_arns = [
    "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"
  ]

  tags = {
    IAC = "True"
  }
}

resource "aws_iam_role" "ecr-role" {
  name = "ecr-role"

  assume_role_policy = jsonencode({
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "sts:AssumeRoleWithWebIdentity",
            "Principal": {
                "Federated": "arn:aws:iam::288786226667:oidc-provider/token.actions.githubusercontent.com"
            },
            "Condition": {
                "StringEquals": {
                    "token.actions.githubusercontent.com:aud": [
                        "sts.amazonaws.com"
                    ],
                    "token.actions.githubusercontent.com:sub": [
                        "repo:tiagohique/ci-python-fastapi:ref:refs/heads/main"
                    ]
                }
            }
        },
        {
            "Effect": "Allow",
            "Principal": {
                "Service": [
                    "build.apprunner.amazonaws.com",
                    "tasks.apprunner.amazonaws.com"
                ]
            },
            "Action": "sts:AssumeRole"
        }
    ]
  })

  inline_policy {
    name = "ecr-app-permission"

    policy = jsonencode({
      Version = "2012-10-17"
      Statement = [
        {
          Sid = "Statement1",
          Action = "apprunner:*",
          Effect = "Allow",
          Resource = "*"
        },
        {
          Sid     = "Statement2",
          Action  = [
            "iam:PassRole",
            "iam:CreateServiceLinkedRole"
          ],
          Effect  = "Allow",
          Resource = "*"
        },
        {
          Sid = "Statement3",
          Action = [
            "ecr:GetDownloadUrlForLayer",
            "ecr:BatchGetImage",
            "ecr:BatchCheckLayerAvailability",
            "ecr:PutImage",
            "ecr:InitiateLayerUpload",
            "ecr:UploadLayerPart",
            "ecr:CompleteLayerUpload",
            "ecr:GetAuthorizationToken"
          ],
          Effect = "Allow",
          Resource = "*"
        }
      ]
    })
  }

  tags = {
    IAC = "True"
  }
}