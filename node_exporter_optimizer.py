import argparse, requests, re
import sys, logging

def format_url(url: str):
    return url if args.url.startswith('http') else 'http://' + url + '/metrics'

def get_failed_collectors(url: str):

    url = format_url(url)
    # Gathering metrics
    try:
        logger.debug(f"Trying to connect to {url}")
        metrics = requests.get(url).text
        logger.debug("Connected")
    except:
        logger.error(f'Cannot connect to {url}')
        exit(1)

    count, node_exporter_arguments = 0, ''
    # Loop on metrics
    for line in metrics.splitlines():
        if line.startswith('node_scrape_collector_success'):
            result = re.findall('"(.*)"', line)
            collector = result[0]
            if ' 0' in line:
                logger.debug(f"Failed collector found: {collector}")
                node_exporter_arguments += f'--no-collector.{collector} '
                count += 1
    
    # Print result
    if count == 0:
        print(f'No failed collectors detected on {url}')
    else:
        print(f'Failed collectors count: {count}')
        print(f'Add following arguments to node_exporter: {node_exporter_arguments}')

 # End of functions

if __name__ == '__main__':

    # Prepare logger
    logger = logging.getLogger("node_exporter_optimizer")
    logging.basicConfig(stream=sys.stdout)

    # Argument management
    parser = argparse.ArgumentParser(
                        prog='node_exporter_optimizer',
                        description='Simple script to optimize node manager based on exposed metrics')
    parser.add_argument('url', type=str, default='http://localhost:9100', help='url of node_exporter to analyze')
    parser.add_argument('--compare', '-c', type=str, nargs=2, help='provide two node_exporter url to compare list of metrics')
    parser.add_argument('--versbose','-v', action='store_true', help='More verbose output')
    args = parser.parse_args()

    if args.debug:
        logger.setLevel(logging.DEBUG)

    if args.url:
        get_failed_collectors(args.url)
