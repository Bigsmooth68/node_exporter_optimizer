FROM python:3

WORKDIR /app

RUN useradd -m runuser
RUN chown -R runuser:runuser /app
USER runuser
ENV PATH="/home/runuser/.local/bin:${PATH}"

RUN pip install --user --no-cache-dir --disable-pip-version-check requests

COPY node_exporter_optimizer.py /app/

ARG URL=--url http://$HOSTNAME:9100

ENTRYPOINT [ "python", "/app/node_exporter_optimizer.py" ]
CMD ["--url", "http://localhost:9100"]