FROM python:onbuild

CMD ["python", "server.py", "runserver", "0.0.0.0:8000"]