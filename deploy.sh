#!/bin/bash
 
message='make it better '

git add .
git commit -am "$message"
git push heroku master
heroku logs --tail
