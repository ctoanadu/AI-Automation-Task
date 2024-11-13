ARG PORT = 443
FROM cypress/browsers:latest
RUN echo apt-get $(python3 -m site --user-base)
COPY requirements.txt .
RUN apt-get update && apt-get install -y python3-pip && pip install -r rewuirements
COPY . .
CMD unicorn main:app --host 0.0.0.0 --port $PORT
