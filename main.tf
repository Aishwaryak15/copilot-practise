provider "aws" {
  region = "us-east-1"
}

resource "aws_instance" "flask_app" {
  ami           = "ami-0c02fb55956c7d316" # Amazon Linux 2 AMI (update as needed)
  instance_type = "t2.micro"

  tags = {
    Name = "FlaskAppInstance"
  }
}
