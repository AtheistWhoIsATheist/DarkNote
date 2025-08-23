#!/bin/bash
cd /home/ubuntu/professor_nihil_backend
source venv/bin/activate
cd src
gunicorn -w 4 -b 0.0.0.0:5000 main:app
