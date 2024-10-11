# Node Exporter Optimizer

It is a simple script to optimize node manager startup options based on exposed metrics. By disabling failed or not applicable collectors, this will reduce the amount of data gathered, processed and stored in [Time Series Database](https://en.wikipedia.org/wiki/Time_series_database) like Prometheus or VictoriaMetrics.

# Usage

## Optimizer

```bash
python node_exporter_optimizer.py --url <url>
```
`url` can be formatted like `hostname:port` or `http://hostname:port`. Default value is `http://localhost:9100`.

Output will be a list of arguments to add to node_exporter command or none.

## Compare

```bash
python node_exporter_optimizer.py --compare <url1> <url2>
```

