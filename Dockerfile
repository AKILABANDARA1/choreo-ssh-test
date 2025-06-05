FROM ubuntu:22.04

# Install dependencies
RUN apt-get update && \
    apt-get install -y openssh-server curl unzip python3 python3-pip && \
    mkdir /var/run/sshd

# Create appuser with UID/GID 10001
RUN groupadd -g 10001 appuser && \
    useradd -u 10001 -g appuser -s /bin/sh -m appuser && \
    echo 'appuser:choreo123' | chpasswd && \
    mkdir -p /home/appuser/.ssh && \
    chown -R appuser:appuser /home/appuser/.ssh

# Create sshd_config inline
RUN echo "\
Port 2222\n\
PermitRootLogin no\n\
PasswordAuthentication yes\n\
ChallengeResponseAuthentication no\n\
UsePAM no\n\
AuthorizedKeysFile .ssh/authorized_keys\n\
" > /home/appuser/.ssh/sshd_config && \
    chown appuser:appuser /home/appuser/.ssh/sshd_config

# Download and install Ngrok
RUN curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null && \
    echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | tee /etc/apt/sources.list.d/ngrok.list && \
    apt-get update && apt-get install -y ngrok

# Add Flask for web interface
RUN pip3 install flask

# Copy the app
COPY app.py /home/appuser/app.py

# Expose ports
EXPOSE 2222 8080

# Set workdir
WORKDIR /home/appuser

# Set non-root user
USER 10001

# Start SSHD, Ngrok, and Flask app together
CMD /usr/sbin/sshd -f /home/appuser/.ssh/sshd_config -D & \
    ngrok tcp 2222 > ngrok.log & \
    python3 app.py
