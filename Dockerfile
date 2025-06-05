FROM python:3.11-slim

# Install openssh-server and wget for ngrok
RUN apt-get update && apt-get install -y openssh-server wget && rm -rf /var/lib/apt/lists/*

# Add non-root user
RUN groupadd -g 10001 appuser && useradd -u 10001 -g appuser -s /bin/sh -m appuser

WORKDIR /home/appuser

# Copy application files
COPY --chown=appuser:appuser app.py check_ngrok_log.py sshd_config ngrok /home/appuser/

# Give execution permission to ngrok
RUN chmod +x /home/appuser/ngrok

# Prepare sshd host keys and config
RUN mkdir -p /home/appuser/.ssh && \
    ssh-keygen -A && \
    chown -R appuser:appuser /home/appuser/.ssh

# Switch to non-root user
USER 10001

# Expose SSH port
EXPOSE 2222
EXPOSE 8080

# Run sshd, ngrok, and Flask app with appropriate delays for ngrok logs
CMD /usr/sbin/sshd -f /home/appuser/sshd_config -D & \
    sleep 5 && ./ngrok tcp 2222 --log=stdout > /tmp/ngrok.log 2>&1 & \
    sleep 10 && python3 app.py
