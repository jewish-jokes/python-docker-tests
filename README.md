# Python Task 1

Given program uses cli commands to create 2 databases, load data into those tables and execute sql queries on loaded set of json data.

## Prerequisites
* docker => 20.10.22
* docker-compose => 2.15.1
* python => 3.11

## Installation

Download the source code from the repository and run following command:

```bash
docker-compose up -d --build
```

To enter the app container

```bash
docker exec -it app bash
```

## Usage

All the following commands should be executed inside the container

```bash
# loads json files into database
python main.py load students_file_path rooms_file_path

# if no arguments provided loads default students.json and rooms.json files from ./data/raw/ directory
python main.py load

# executes sql queries and writes output(./data/output/) in either json or xml files, if no arguments provided uses 
# json as a default file type
python main.py execute-queries json
python main.py execute-queries xml

#to run unit tests
pytest
```