import json
from oslo_config import cfg
from neutron.common import config
from neutron.common import rpc as n_rpc
import oslo_messaging
from oslo_messaging.notify import NotificationFilter
import inspect
import logging

def enable_stdout_log(logger):
    import sys
    ch = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(ch)

enable_stdout_log(logging.getLogger('oslo_messaging'))

config.init(['--config-file=/etc/neutron/neutron.conf',
             '--config-file=/etc/neutron/plugins/ml2/ml2_conf.ini'])
transport = oslo_messaging.get_transport(cfg.CONF)
#print("transport=%s", inspect.getmembers(transport))
notifier = oslo_messaging.Notifier(transport, driver='messaging', publisher_id='oslo_test', topic='topic_test')
notifier.info({'some': 'context'}, 'just.testing', {'heavy': 'payload'})
