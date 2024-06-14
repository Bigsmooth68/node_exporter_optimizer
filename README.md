# Node Exporter Optimizer

It is a simple script to optimize node manager startup options based on exposed metrics.

# Usage

```bash
python node_exporter_optimizer.py <url>
```
`url` can be formatted like `hostname:port` or `http://hostname:port`.

Output will be a list of arguments to add to node_exporter command.