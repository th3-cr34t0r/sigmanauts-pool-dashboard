import datetime

import requests

base_api = "http://15.204.211.130:4000/api/pools/ErgoSigmanauts"


def get_api_data(url=""):
    if url == "":
        url = base_api

    data = requests.get(url=url)
    data.raise_for_status()
    return data.json()


class GetPoolData:
    def __init__(self):
        self.id = ""

    def time_format(self, data):
        time_str = data
        time_obj = time_str[:21]
        time_obj = datetime.datetime.strptime(time_obj, '%Y-%m-%dT%H:%M:%S.%f')
        return time_obj.strftime('%Y-%m-%d %H:%M:%S')

    def hash_to_petahash(selfs, data):
        return str(round(float(data) / 1e15, 3))

    def hash_to_gigahash(self, data):
        return str(round((float(data) / 1e9), 3))

    def hash_to_megahash(self, data):
        return str(round((float(data) / 1e6), 3))

    def get_stats(self, data_json, arg: str):
        # VALID ARGS:
        # id
        # address
        # totalPaid
        # poolEffort
        # totalBlocks
        # poolFeePercent
        # addressInfoLink
        # lastPoolBlockTime
        # blockRefreshInterval
        # jobRebroadcastTimeout
        # clientConnectionTimeout
        data = data_json['pool'][f'{arg}']

        # Round totalPaid
        if arg == "totalPaid":
            data = str(round(int(data), 2))

        elif arg == "poolEffort":
            data = str(round(float(data) * 100, 2))

        elif arg == "lastPoolBlockTime":
            data = self.time_format(data)

        return data

    def get_pool_stats(self, data_json, arg: str):
        # VALID ARGS:
        # poolHashrate
        # connectedMiners
        # sharesPerSecond
        data = data_json['pool']['poolStats'][f'{arg}']

        # Hashes to Gigahashes
        if arg == "poolHashrate":
            data = self.hash_to_gigahash(data)

        return data

    def get_payment_processing(self, data_json, arg: str):
        # enabled
        # payoutScheme
        # minimumPayment
        data = data_json['pool']['paymentProcessing'][f'{arg}']

        return data

    def get_network_stats(self, data_json, arg: str):
        # blockHeight
        # networkHashrate
        # networkDifficulty
        # lastNetworkBlockTime
        data = data_json['pool']['networkStats'][f'{arg}']

        # Hashes to Terahashes
        if arg == 'networkHashrate':
            data = str(round(float(data) / 1e12, 3))

        # to Peta
        elif arg == 'networkDifficulty':
            data = self.hash_to_petahash(data)

        elif arg == 'lastNetworkBlockTime':
            data = self.time_format(data)

        return data

    def get_miner_performance(self, address):
        url = "{}/{}/{}".format(base_api, "miners", f"{address}")
        miner_data = get_api_data(url)
        miner_hashrate = 0

        #         miner_hashrate:
        for worker in miner_data['performance']['workers']:
            miner_hashrate += float(miner_data['performance']['workers'][f'{worker}']['hashrate'])

        #       hashrate in Gh/s
        miner_hashrate = float(self.hash_to_megahash(miner_hashrate))

        #       miner_avg_hashrate:
        miner_avg_hashrate = "0"

        #       miner_pending_shares:
        miner_penging_shares = str(round(float(miner_data["pendingShares"]), 2))

        #       miner_pending_balance:
        miner_pending_balance = str(round(float(miner_data["pendingBalance"]), 2))

        #       miner_total_paid:
        miner_total_paid = str(round(float(miner_data["totalPaid"]), 2))

        #       pool contribution in %
        data_json = get_api_data()
        miner_contribution = round(
            (miner_hashrate / (float(self.get_pool_stats(data_json, "poolHashrate")) * 1000) * 100), 2)

        miner_data_display = {'miner_hashrate': miner_hashrate,
                              'miner_avg_hashrate': miner_avg_hashrate,
                              'miner_pending_shares': miner_penging_shares,
                              'miner_pending_balance': miner_pending_balance,
                              'miner_total_paid': miner_total_paid,
                              'miner_contribution': miner_contribution
                              }
        return miner_data_display

    def get_wallet_stats(self, address):
        url = '{}/{}'.format(base_api, 'miners')
        data = get_api_data(url)
        miner_list = []
        for sample in data:
            miner_list.append(sample['miner'])

        for miner in miner_list:
            if address == miner:
                return self.get_miner_performance(address)

        return "Miner data not available!"

    def get_last_block_info(self):
        url = "{}/{}".format(base_api, 'blocks')
        block_data = get_api_data(url)

        if block_data[0]['confirmationProgress'] == 0:
            block_effort = 'Calculating...'
        else:
            block_effort = str(round(float(block_data[0]['effort']) * 100, 2))

        block_data_display = {'block_status': block_data[0]['status'],
                              'block_progress': str(round(float(block_data[0]['confirmationProgress']) * 100, 2)),
                              'block_effort': block_effort,
                              'block_last_reward': block_data[0]['reward'],
                              'block_miner': (block_data[0]['miner'])[:10] + '...' + (block_data[0]['miner'])[41:],
                              'block_time': self.time_format(block_data[0]['created'])
                              }
        return block_data_display

    def get_workers_stats(self, address):
        url = '{}/{}/{}'.format(base_api, 'miners', f'{address}')
        data = get_api_data(url)

        miner_stats = []

        for worker in data['performance']['workers']:
            worker_stats = {'name': worker,
                            'hashrate': self.hash_to_megahash(data['performance']['workers'][f'{worker}']['hashrate']),
                            'sharesPerSecond': data['performance']['workers'][f'{worker}']['sharesPerSecond']
                            }
            miner_stats.append(worker_stats)
        return miner_stats

    def calculate_time_to_find_block(self, network_hashrate, pool_hashrate, block_time=120):
        # network hashrate from terahashes to hashes
        network_hashrate = float(network_hashrate) * 1e12
        # pool hashrate from gigahashes to hashes
        pool_hashrate = float(pool_hashrate) * 1e9
        #                                                                 m    s
        return round(((network_hashrate / pool_hashrate) * block_time) / (60 * 60))
