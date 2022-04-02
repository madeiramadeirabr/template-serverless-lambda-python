"""
AWS Opensearch Module
Version: 1.0.1
"""
import os
from elasticsearch import Elasticsearch
from elasticsearch.transport import Transport

from flambda_app.helper import get_protocol


def elk_is_https():
    result = False
    if 'ELASTIC_HTTPS' in os.environ and str(os.getenv('ELASTIC_HTTPS')).lower() == 'true':
        result = True
    return result


def get_elasticsearch_client(with_params=False):
    host = os.environ["ELASTIC_URL"] if "ELASTIC_URL" in os.environ else "localhost"
    port = os.environ["ELASTIC_PORT"] if "ELASTIC_PORT" in os.environ else 9200

    if with_params:
        return CustomElasticsearch([host],
                                   use_ssl=elk_is_https(),
                                   verify_certs=True,
                                   scheme=get_protocol(),
                                   port=port,
                                   timeout=30
                                   )
    else:
        return CustomElasticsearch([host],
                                   use_ssl=elk_is_https(),
                                   timeout=30
                                   )


class CustomElasticsearch(Elasticsearch):
    def ignore_verification(self):
        # force true to ignore ES validation of the server
        self.transport._verified_elasticsearch = True

    def __init__(self, hosts=None, transport_class=Transport, **kwargs):
        super().__init__(hosts, transport_class, **kwargs)
        self.ignore_verification()
