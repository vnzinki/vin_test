FROM python:3.9-slim

COPY . /app
WORKDIR /app
RUN apt update -y && apt install -y build-essential
RUN pip install pydantic pydantic[email] fastapi uvicorn[standard] sqlalchemy psycopg2-binary logzero pyjwt python-decouple passlib[bcrypt]
RUN pip install python-dotenv
EXPOSE 8000
CMD uvicorn --host 0.0.0.0 --log-level warning main:app
