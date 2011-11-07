#!/bin/bash  
# -*- coding: utf-8 -*-
# Copyright (C) 2011 Hugo Lindström <hugolm84@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

#Change to path, ey?
SCRAPER_PATH=/home/charts/tomahawk-contrib/charts/src/scrapers
API_SCRAPER_PATH=$SCRAPER_PATH/apis
LOG_PATH=$SCRAPER_PATH/logs

if [ ! -d "$SCRAPER_PATH" -o ! -d "$API_SCRAPER_PATH" ]; then 
  echo "Some paths does not exist"
  exit
fi

if [ ! -d "$LOG_PATH" ]; then 
  echo "$LOG_PATH does not exist, creating..."
  mkdir $LOG_PATH
  if [ ! -d "$LOG_PATH" ]; then
    echo "Failed to create $LOG_PATH";
    exit
  fi
fi


if [ ! -n "$1" ]
then
  echo "Usage: `basename $0` string:name {optional string:pythonVersion }"
  exit
fi 
 
PYTHONV=${2:-python}

case "$1" in
  "itunes") cd $SCRAPER_PATH && scrapy crawl itunes.com --set FEED_FORMAT=json &> $LOG_PATH/$1.$(date +\%Y\%m\%d).log
;;
  "billboard") cd $SCRAPER_PATH && scrapy crawl billboard.com --set FEED_FORMAT=json &> $LOG_PATH/$1.$(date +\%Y\%m\%d).log
;;
  "rdio") cd $API_SCRAPER_PATH && $PYTHONV $1.py &> $LOG_PATH/$1.$(date +\%Y\%m\%d).log   
;;
  "wah") cd $API_SCRAPER_PATH && $PYTHONV $1.py &> $LOG_PATH/$1.$(date +\%Y\%m\%d).log
;;
esac
