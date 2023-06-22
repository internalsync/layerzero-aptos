# -*- coding: utf-8 -*-
import logging
import pprint
import os
import csv

import json
import random
import time

from layerzero.filereader import CsvFileReader
from layerzero.logger import setup_color_logging, setup_file_logging
from layerzero.api import Node, Account, Contract

from web3 import Web3


class CsvFileReaderWithCheck(CsvFileReader):
    def check(self, res) -> list:
        for item in res:
            acc = Web3().eth.account.from_key(item['private_key'])  # checking private key
            item['address'] = acc.address
        return res


class LayerzeroTrader:
    CONFIG_FILENAME = os.environ.get('CONFIG_FILENAME', 'config.json')

    def __init__(self):
        with open(self.CONFIG_FILENAME) as f:
            self.config = json.load(f)

        self.logger = logging.getLogger('layerzero')
        self.logger.setLevel(logging.DEBUG)
        setup_file_logging(self.logger, self.config['log_file'])
        setup_color_logging(self.logger)

        network_name = self.config['network']
        self.node = Node(rpc_url=self.config['networks'][network_name]['rpc'],
                         explorer_url=self.config['networks'][network_name]['explorer'])

    @staticmethod
    def load_wallets(filename):
        res = []
        with open(filename) as f:
            reader = csv.reader(f)
            for row in reader:
                res.append(row)  # todo: check
        return res

    def run(self):
        try:
            wallets = CsvFileReaderWithCheck(self.config['wallets_file']).load()
        except Exception as ex:
            self.logger.error(ex)
            return
        for wallet in wallets:
            self.logger.info(wallet['address'])
            self.logger.debug(self.node.get_explorer_address_url(wallet['address']))

    def random_delay(self, min_sec, max_sec):
        random_sec = random.randint(min_sec, max_sec)
        self.logger.debug(f'delay for {random_sec} sec')
        time.sleep(random_sec)
