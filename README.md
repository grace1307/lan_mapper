# Lan Mapper
A flask based report generator service for nmap-format data. 
This is originally written for a nmap scanner on my lan for a course work on network security, so it is not optimized, but it had been a fun project, maybe I can revisit some day. The service is to be run on a small raspberry pi or a linux machine

![Screenshot](http://gracex.tech/assets/lan_mapper.png)

# Dev
1. `pipenv install && pipenv shell`
2. `python3 ./manage.py run` (you will need the database set up first, I used alembic for migration, so just create the database "lan_mapper" and run the migration command, see flask_script)
3. `http://localhost:5000`
