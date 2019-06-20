#!/bin/bash
 
message='add audio emplate'

git add .
git commit -am "$message"
git push heroku master
heroku logs --tail
