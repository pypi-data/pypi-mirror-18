"""WSGI middleware that loads auth0 config from dynamodb.

fThe table name is configured with the `clients_config_table` settings
key.  Records are selected based on the `clients_config_service` key.
"""
import logging

from .exception import Error

log = logging.getLogger(__name__)

clients_config_table_key = 'clients_config_table'
clients_config_service_key = 'clients_config_service'


def has_dynamodb_config(config):
    return clients_config_table_key in config


def config_dynamodb(config):
    import boto3
    log.info('wsgiauth0 dynamodb configuration')
    dynamodb = boto3.resource('dynamodb')
    if has_dynamodb_config(config):
        clients = client_settings_from_dynamodb(config, dynamodb)
        log.debug('dynamodb configured clients: %s', clients)
        return clients
    else:
        return {}


def client_settings_from_dynamodb(config, dynamodb):
    """Read a client dict from key value pairs in dynamodb."""
    try:
        table_name = config[clients_config_table_key]
    except KeyError:
        raise Error(
            'missing_config',
            '"%s" key not found in config' % clients_config_table_key,
        )

    try:
        service = config[clients_config_service_key]
    except KeyError:
        raise Error(
            'missing_config',
            '"%s" key not found in config' % clients_config_service_key,
        )

    log.debug(
        'Loading auth0 config from dynamodb table %s with service %s',
        table_name, service,
    )
    records = get_records(dynamodb, table_name, service)
    return parse_clients(records)


def get_records(dynamodb, table_name, service):
    """Read all records from dynamodb with the specified service."""
    from boto3.dynamodb.conditions import Key
    table = dynamodb.Table(table_name)
    try:
        result = table.query(
            KeyConditionExpression=Key('service').eq(service)
        )
    except:
        log.exception(
            'table.scan table=%s',
            table_name,
            extra={
                "table_name": table_name,
            }
        )
        raise Error(
            'missing_config',
            'key field could not be found in DynamoDB table %s' % table_name
        )

    return result['Items']


def parse_clients(items):
    """Parse a list of items into a clients dict."""
    return {item['id']: item for item in items}
