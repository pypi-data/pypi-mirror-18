from oslo_config import cfg
from neutron.common import config
import oslo_messaging
from oslo_messaging.notify import NotificationFilter
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

class AnyEndpoint(object):
    filter_rule = NotificationFilter(event_type='^.*')

    def __init__(self):
        pass

    def info(self, ctxt, publisher_id, event_type, payload, metadata):
        print '!!! info: ', publisher_id, event_type, metadata, payload, ctxt

config.init(['--config-file=/etc/neutron/neutron.conf',
             '--config-file=/etc/neutron/plugins/ml2/ml2_conf.ini'])
transport = oslo_messaging.get_transport(cfg.CONF)
targets = [ oslo_messaging.Target(topic='topic_test') ]
#targets = [ oslo_messaging.Target(topic='topic_test', exchange='neutron') ]
#targets = [ oslo_messaging.Target(topic='notifications') ]
endpoints = [ AnyEndpoint() ]
server = oslo_messaging.get_notification_listener(transport, targets, endpoints)
#server = oslo_messaging.get_notification_listener(transport, targets, endpoints, pool='networking-bigswitch-l3-pe')

server.start()
server.wait()
