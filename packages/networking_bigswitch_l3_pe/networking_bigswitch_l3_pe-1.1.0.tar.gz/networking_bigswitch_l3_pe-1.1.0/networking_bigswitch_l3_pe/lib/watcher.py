#!/usr/bin/env python

import logging
from oslo_config import cfg
from neutron.common import config
import keystoneclient.middleware.auth_token
import bsnstacklib.plugins.bigswitch.config
import networking_bigswitch_l3_pe.lib.config
from networking_bigswitch_l3_pe.lib.event import EventWatcher

LOG = logging.getLogger('networking_bigswitch_l3_pe.lib.event')


def enable_stdout_log(logger):
    import sys
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)


def setup_config():
    bsnstacklib.plugins.bigswitch.config.register_config()
    networking_bigswitch_l3_pe.lib.config.register_config()
    config.init(['--config-file=/etc/neutron/neutron.conf',
                 '--config-file=/etc/neutron/plugins/ml2/ml2_conf.ini'])


def main():
    enable_stdout_log(LOG)
    # XXX: No handlers could be found for logger "oslo_config.cfg"
    setup_config()

    watcher = EventWatcher()
    watcher.watch()

if __name__ == '__main__':
    main()
