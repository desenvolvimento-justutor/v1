#!/usr/bin/env bash
echo "Matando processo....."
pkill /home/justutorial/projects/django/justutorial/manage.py
echo "Levantando server..."
/home/justutorial/run/bin/python /home/justutorial/projects/django/justutorial/manage.py runfcgi protocol=scgi host=127.0.0.1 port=3309
echo "*** concluído ***"