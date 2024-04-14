import requests
import pandas as pd
import get_pool_data
import datetime

class NetworkStats:
    def __init__(self):
        self.get_blockchain_height_url = 'https://ergo-sig-mining.net/blockchain/indexedHeight'
        self.get_block_headers_url = 'https://ergo-sig-mining.net'
        self.get_block_info_url = 'https://ergo-sig-mining.net/blocks'

    def get_block_headers(self, limit, offset):
        url = '{}/blocks?limit={}&offset={}'.format(self.get_block_headers_url, limit, offset)
        data = requests.get(url=url).json()
        print(data)

        return data

    def get_block_data(self, block_lenght):
        offset = str(int(requests.get(url=self.get_blockchain_height_url).json()['indexedHeight']) - block_lenght)
        block_headers = self.get_block_headers(block_lenght, offset)

        block_data = []
        for header in block_headers:
            url = '{}/{}'.format(self.get_block_info_url, header)
            data = requests.get(url=url)
            data.raise_for_status()

            data = data.json()

            print(data['header']['timestamp'])

            timestamp = datetime.datetime.fromtimestamp(data['header']['timestamp'] / 1e3)
            timestamp = timestamp.strftime('%Y-%m-%d %H:%M:%S')

            block_data.append({'difficulty': get_pool_data.GetPoolData.hash_to_petahash(get_pool_data.GetPoolData, data['header']['difficulty']),
                               'timestamp': timestamp,
                               })

        return block_data
