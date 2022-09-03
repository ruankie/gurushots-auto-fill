FROM selenium/standalone-chrome:105.0-20220831

ENV DEBIAN_FRONTEND=noninteractive

RUN sudo apt update && \
    sudo apt install -y python3.8 && \
    sudo apt install -y python3-pip

RUN sudo mkdir /app

COPY ./requirements.txt /app/requirements.txt
COPY ./auto_fill.py /app/auto_fill.py
COPY ./credentials.py /app/credentials.py

RUN pip3 install --no-cache-dir -r /app/requirements.txt

CMD ["python3", "/app/auto_fill.py"]