#!/bin/sh
git init 
git remote add origin 'https://github.com/Jaimin1312/Code-Submision-Jobe-Django.git'
git pull origin master
git status 
git add -A
git commit -a -m "first commit"
git log
git branch 'Code-Submission'
git checkout 'Code-Submission'
git status
git push origin 'Code-Submission'
