#!/bin/bash
 
message=$1

git add .
git commit -am "$message"
git push heroku master
heroku logs --tail
