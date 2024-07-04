FROM python:3

WORKDIR /app

COPY node_exporter_optimizer.py /app/

RUN pip install --no-cache-dir requests

ARG URL=--url http://$HOSTNAME:9100

ENTRYPOINT [ "python", "/app/node_exporter_optimizer.py" ]
CMD ["--url", "http://localhost:9100"]