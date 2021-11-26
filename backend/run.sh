#!/bin/bash

#echo STARTINGD RUN.SH FOR STARTING DJANGO SERVER PORT IS $PORT
#
#echo ENVIRONMENT VAIRABLES IN RUN.SH
#printenv 

if [ -z "$VCAP_APP_PORT" ];
then SERVER_PORT=5000;
else SERVER_PORT="$VCAP_APP_PORT";
fi

echo [$0] port is------------------- $SERVER_PORT
python manage.py makemigrations
python manage.py migrate

echo [$0] Starting Django Server...
python manage.py runserver 0.0.0.0:$SERVER_PORT --noreload
