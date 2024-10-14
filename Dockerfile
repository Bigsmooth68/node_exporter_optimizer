FROM python:3-alpine

WORKDIR /app

RUN adduser runuser --disabled-password
RUN chown -R runuser:runuser /app
USER runuser
ENV PATH="/home/runuser/.local/bin:${PATH}"

RUN pip install --user --no-cache-dir --disable-pip-version-check requests

COPY node_exporter_optimizer.py /app/

ENTRYPOINT [ "python", "/app/node_exporter_optimizer.py" ]
