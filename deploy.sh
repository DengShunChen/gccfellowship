#!/bin/bash

git add .
git commit -am "randon select for golden verse"
git push heroku master
heroku logs --tail
