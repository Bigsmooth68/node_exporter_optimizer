import argparse, requests, re
import sys, logging

def format_url(url: str):
    return url if url.startswith('http') else 'http://' + url + '/metrics'

def get_metrics(url: str):
    url = format_url(url)
    try:
        logger.debug(f"Trying to connect to {url}")
        metrics = requests.get(url).text
        logger.debug("Connected")
    except Exception as err:
        logger.error(f'Cannot connect to {url}')
        logger.error(err)
        exit(1)
    return metrics

def get_failed_collectors(url: str):

    # Gathering metrics
    metrics = get_metrics(url)

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

def filter_metrics_comments(metrics: str):
    pattern = r'^#.*$'
    
    # Trouve toutes les correspondances dans le texte multilignes
    matches = re.findall(pattern, metrics, re.MULTILINE)
    
    # Retourne les correspondances sous forme de liste
    return matches

def compare_metrics(url1: str, url2: str):
    metrics1 = get_metrics(url1)
    metrics2 = get_metrics(url2)

    f_metrics1 = filter_metrics_comments(metrics1)
    f_metrics2 = filter_metrics_comments(metrics2)

    diff = set(f_metrics1) ^ set(f_metrics2)
    logger.debug(f"Length: {len(f_metrics1)} {len(f_metrics2)}")

    for element in diff:
        print(element)

 # End of functions

if __name__ == '__main__':

    # Prepare logger
    logger = logging.getLogger("node_exporter_optimizer")
    logging.basicConfig(stream=sys.stdout)

    # Argument management
    parser = argparse.ArgumentParser(
                        prog='node_exporter_optimizer',
                        description='Simple script to optimize node manager based on exposed metrics')
    parser.add_argument('url', type=str, nargs='+', default='http://localhost:9100', help='url of node_exporter to analyze')
    parser.add_argument('--verbose','-v', action='store_true', help='More verbose output')
    args = parser.parse_args()

    if args.verbose:
        logger.setLevel(logging.DEBUG)
    
    logger.debug(f"Arguments: {args}")

    if len(args.url) == 1:
        logger.debug("Running in optimizer mode")
        get_failed_collectors(args.url[0])
    elif len(args.url) == 2:
        logger.debug("Running in compare mode")
        logger.debug(args.url)
        compare_metrics(args.url[0], args.url[1])
    
    logger.debug("Script terminated")
