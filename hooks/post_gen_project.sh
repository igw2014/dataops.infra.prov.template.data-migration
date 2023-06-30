#!/bin/zsh
#a=$(pwd)
#echo "Current working directory is : $a"
pipenv install
cdktf get
#pipenv shell
# cdktf deploy s3tfstatestack