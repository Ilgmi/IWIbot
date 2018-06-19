#!/bin/bash
#
# Copyright 2017 IBM Corp. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the “License”);
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#  https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an “AS IS” BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Load configuration variables
source local.env

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

function usage() {
  echo -e "Usage: $0 [--info,--install,--uninstall,--env]"
}

function info() {
  # Exit if any command fails
  set -e
  echo -e "\n"
  echo -e "URL for Action 'Joke':"
  bx wsk action get Joke --url
  echo -e "\n"
  echo -e "URL for Action 'Meal':"
  bx wsk action get Meal --url
  echo -e "\n"
  echo -e "URL for Action 'Router':"
  bx wsk action get Router --url
  echo -e "\n"
  echo -e "URL for Action 'Timetables':"
  bx wsk action get Timetable --url
  echo -e "\n"
  echo -e "URL for Action 'Weather':"
  bx wsk action get Weather --url
  echo -e "\n"
  echo -e "URL for Action 'Login':"
  bx wsk action get Login --url
  echo -e "\n"
  echo -e "URL for Action 'Semester':"
  bx wsk action get Semester --url
  echo -e "\n"
}

function install() {
  # Exit if any command fails
  echo -e "${BLUE}"
  echo "===================================================================================================="
  echo "                                        Updating Actions                                           "
  echo "===================================================================================================="
  echo -e "${NC}"
  set -e
  : '
  echo -e "Updating OpenWhisk actions, triggers, and rules for IWIBot"

  echo -e "${BLUE}"
  echo "~~~~~~~~~~~~~~~~~~~~~~~~~~ 1/8) Update Joke Action with HTTP-VERB GET ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
  echo -e "${NC}"
  cd openwhisk/joke
  bash deploy.sh
  cd ../..

  echo -e "${BLUE}"
  echo "~~~~~~~~~~~~~~~~~~~~~~~~~~ 2/8) Update Meal Action with HTTP-VERB GET ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
  echo -e "${NC}"
  cd openwhisk/meal
  bash deploy.sh
  cd ../..
  
  echo -e "${BLUE}"
  echo "~~~~~~~~~~~~~~~~~~~~~~~~~~ 3/8) Update Navigation Action with HTTP-VERB GET ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
  echo -e "${NC}"
  cd openwhisk/navigation
  #bash deploy.sh
  cd ../..

  echo -e "${BLUE}"
  echo "~~~~~~~~~~~~~~~~~~~~~~~~ 4/8) Update Router Action with HTTP-VERB POST ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
  echo -e "${NC}"
  cd openwhisk/router
  bash deploy.sh
  bx wsk api create -n "iwibot API" $API_PATH /router post Router --response-type http
  cd ../..

  echo -e "${BLUE}"
  echo "~~~~~~~~~~~~~~~~~~~~~~ 5/8) Update Timetable Action with HTTP-VERB POST ~~~~~~~~~~~~~~~~~~~~~~~~~~~"
  echo -e "${NC}"
  cd openwhisk/timetable
  bash deploy.sh
  cd ../..
  '
  echo -e "${BLUE}"
  echo "~~~~~~~~~~~~~~~~~~~~~~~ 6/8) Update Weather Action with HTTP-VERB POST ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
  echo -e "${NC}"
  cd openwhisk/weather
  bash deploy.sh
  cd ../..

  echo -e "${BLUE}"
  echo "~~~~~~~~~~~~~~~~~~~~~~~ 7/8) Update Login Action with HTTP-VERB GET ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
  echo -e "${NC}"
  cd openwhisk/login
  bash deploy.sh
  cd ../..


  echo -e "${BLUE}"
  echo "~~~~~~~~~~~~~~~~~~~~~~~ 8/8) Update Semester Action with HTTP-VERB GET ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
  echo -e "${NC}"
  cd openwhisk/semester
  bash deploy.sh
  cd ../..

  echo -e "${GREEN}"
  echo -e "Updating Complete!"
  echo -e "${NC}"
}

function uninstall() {
  echo -e "${BLUE}"
  echo "===================================================================================================="
  echo "                                       Undeploying Actions                                          "
  echo "===================================================================================================="
  echo -e "${NC}"

  echo "Removing API actions..."
  bx wsk api delete $API_PATH

  echo "Removing actions..."
  bx wsk action delete Joke
  bx wsk action delete Meal
  bx wsk action delete Navigation
  bx wsk action delete Router
  bx wsk action delete Timetable
  bx wsk action delete Weather
  bx wsk action delete Login
  bx wsk action delete Semester

  echo -e "${GREEN}"
  echo -e "Undeployment Complete"
  echo -e "${NC}"
}

function showenv() {
  echo -e API_PATH="$API_PATH"
  echo -e API_ENDPOINT="$API_ENDPOINT"
  echo -e API_KEY="$API_KEY"
  echo -e BLUEMIX_ACCOUNT_ID="$BLUEMIX_ACCOUNT_ID"
  echo -e BLUEMIX_ORGANIZATION="$BLUEMIX_ORGANIZATION"
  echo -e BLUEMIX_SPACE="$BLUEMIX_SPACE"
}

case "$1" in
"--info" )
info
;;
"--install" )
install
;;
"--uninstall" )
uninstall
;;
"--env" )
showenv
;;
* )
usage
;;
esac
