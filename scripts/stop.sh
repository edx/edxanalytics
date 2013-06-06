#!/bin/bash
ps -ef | grep runserver | grep -v grep | awk '{print $2}' | xargs kill -9

