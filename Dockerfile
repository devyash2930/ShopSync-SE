# syntax=docker/dockerfile:1

FROM python:3.9-slim-buster

WORKDIR /ShopSync

COPY requirements_docker.txt requirements_docker.txt
RUN pip3 install -r requirements_docker.txt

COPY . .

EXPOSE 8501

ENV NAME venv

CMD ["streamlit", "run", "slash_user_interface.py"]