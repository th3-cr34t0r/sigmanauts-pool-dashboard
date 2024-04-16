import requests
import get_pool_data


class NetworkStats:
    def __init__(self):
        self.get_blockchain_height_url = 'https://ergo-sig-mining.net/blockchain/indexedHeight'
        self.get_block_headers_url = 'https://ergo-sig-mining.net'
        self.get_block_info_url = 'https://ergo-sig-mining.net/blocks'
        self.get_limited_network_data_url = 'https://api.ergoplatform.com/info'

    def network_hashrate(self):
        data = requests.get(self.get_limited_network_data_url)
        data.raise_for_status()
        data = data.json()

        return float(get_pool_data.GetPoolData.hash_to_terahash(get_pool_data.GetPoolData, data['hashRate']))
