import argparse
import requests
from prometheus_client.parser import text_string_to_metric_families


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
                        prog='node_exporter_optimizer',
                        description='Simple script to optimize node manager startup options based on exposed metrics')
    parser.add_argument('url')
    args = parser.parse_args()

    # Add http if missing
    url = args.url if args.url.startswith('http') else 'http://' + args.url

    metrics = requests.get(url + '/metrics').text

    for family in text_string_to_metric_families(metrics):
        for sample in family.samples:
            print("Name: {0} Labels: {1} Value: {2}".format(*sample))
