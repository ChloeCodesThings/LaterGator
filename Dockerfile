FROM python:onbuild

CMD source env/bin/activate

CMD source bin/secrets.sh

CMD ["python", "server.py", "runserver", "0.0.0.0:3000"]