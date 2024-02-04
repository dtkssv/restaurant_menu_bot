
FROM python:3.8-slim

ARG USER=user
ARG UID=1000

# Extend PATH to use pip-installed tools from shell (like alembic)
ENV PATH="${PATH}:/home/$USER/.local/bin"

# Add non-root user
RUN adduser --uid $UID --disabled-password --gecos '' $USER
USER $USER
WORKDIR /home/$USER


# Install requirements
#  (copy isolated from project root, to avoid having to install everything again if something on the project sources changed, but not in requirements)
COPY ./requirements.txt /tmp/requirements.txt
RUN pip install --user --no-cache-dir -r /tmp/requirements.txt

# Copy project files
COPY ./ ./app/
WORKDIR /home/$USER/app

HEALTHCHECK --interval=1m --timeout=10s --retries=3 --start-period=30s CMD python tools/scripts/healthcheck.py
CMD ["python", "-u", "."]
