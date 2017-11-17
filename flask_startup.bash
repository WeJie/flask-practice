#! /bin/bash
mkdir app
mkdir app/{templates,static,main}
mkdir migrations
mkdir tests
touch app/{__init__,email,models}.py
touch app/main/{__init__,errors,forms,views}.py
touch tests/{__init__,test}.py
touch {config,manage}.py

