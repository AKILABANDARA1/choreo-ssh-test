FROM ubuntu:22.04

RUN apt-get update && \
    apt-get install -y openssh-server python3 python3-pip curl unzip && \
    mkdir /var/run/sshd && \
    ssh-keygen -A

RUN groupadd -g 10001 appuser && \
    useradd -u 10001 -g appuser -s /bin/sh -m appuser && \
    echo 'appuser:choreo123' | chpasswd && \
    mkdir -p /home/appuser/.ssh && \
    chown -R appuser:appuser /home/appuser/.ssh

RUN echo "\
Port 2222\n\
PermitRootLogin no\n\
PasswordAuthentication yes\n\
ChallengeResponseAuthentication no\n\
UsePAM no\n\
AuthorizedKeysFile .ssh/authorized_keys\n\
" > /home/appuser/.ssh/sshd_config && \
    chown appuser:appuser /home/appuser/.ssh/sshd_config

RUN curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null && \
    echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | tee /etc/apt/sources.list.d/ngrok.list && \
    apt-get update && apt-get install -y ngrok

COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY app.py /home/appuser/app.py

WORKDIR /home/appuser
USER 10001

EXPOSE 2222 8080

CMD /usr/sbin/sshd -f /home/appuser/.ssh/sshd_config -D & \
    sleep 5 && ngrok tcp 2222 > /tmp/ngrok.log & \
    sleep 5 && python3 app.py
