#!/bin/bash
 
message='fix if only have single message of alert '

git add .
git commit -am "$message"
git push heroku master
heroku logs --tail
