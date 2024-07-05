import argparse, requests, re

if __name__ == '__main__':
    # Argument management
    parser = argparse.ArgumentParser(
                        prog='node_exporter_optimizer',
                        description='Simple script to optimize node manager startup options based on exposed metrics')
    parser.add_argument('--url', type=str, default='http://localhost:9100')
    args = parser.parse_args()

    # Add http if missing
    url = args.url if args.url.startswith('http') else 'http://' + args.url + '/metrics'

    # Gathering metrics
    try:
        metrics = requests.get(url).text
    except:
        print(f'Cannot connect to {url}')
        exit(1)

    count, node_exporter_arguments = 0, ''
    # Loop on metrics
    for line in metrics.splitlines():
        if line.startswith('node_scrape_collector_success'):
            result = re.findall('"(.*)"', line)
            collector = result[0]
            if ' 0' in line:   
                node_exporter_arguments += f'--no-collector.{collector} '
                count += 1
    
    # Print result
    if count == 0:
        print(f'No failed collectors detected on {url}')
    else:
        print(f'Failed collectors count: {count}')
        print(f'Add following arguments to node_exporter: {node_exporter_arguments}')