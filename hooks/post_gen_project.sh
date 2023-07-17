#!/bin/zsh
#a=$(pwd)
#echo "Current working directory is : $a"
pipenv install
cdktf get
#pipenv shell
# cdktf deploy s3tfstatestack
pip install --target=/opt/homebrew/lib/python3.11/site-packages -r requirements.txt
aws s3api create-bucket --bucket {{ cookiecutter.tenant_name }}-{{ cookiecutter.environment }}-dops-tf-state --region {{ cookiecutter.region }}
aws s3api put-object --bucket {{ cookiecutter.tenant_name }}-{{ cookiecutter.environment }}-dops-tf-state --key sample-database/
aws s3api put-object --bucket {{ cookiecutter.tenant_name }}-{{ cookiecutter.environment }}-dops-tf-state --key data-migration/