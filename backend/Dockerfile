FROM python:3.11
WORKDIR /backend
ENV PYTHONWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN pip install --upgrade pip
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . .