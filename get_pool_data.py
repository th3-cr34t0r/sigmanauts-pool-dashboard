import requests
from datetime import datetime

base_api = "http://15.204.211.130:4000/api/pools/ErgoSigmanauts"


def get_api_data():
    data = requests.get(url=base_api)
    data.raise_for_status()
    return data.json()


class GetPoolData:
    def __init__(self):
        self.id = ""

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
            time_str = data
            time_obj = time_str[:21]
            time_obj = datetime.strptime(time_obj, '%Y-%m-%dT%H:%M:%S.%f')
            data = time_obj.strftime('%Y-%m-%d %H:%M:%S')

        return data

    def get_pool_stats(self, data_json, arg: str):
        # VALID ARGS:
        # poolHashrate
        # connectedMiners
        # sharesPerSecond
        data = data_json['pool']['poolStats'][f'{arg}']

        # Hashes to Gigahashes
        if arg == "poolHashrate":
            data = str(round((int(data) / 1000000000), 3))

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
            data = str(round(float(data) / 1000000000000, 3))

        # to Peta
        elif arg == 'networkDifficulty':
            data = str(round(float(data) / 1000000000000000, 3))

        elif arg == 'lastNetworkBlockTime':
            time_str = data
            time_obj = time_str[:21]
            time_obj = datetime.strptime(time_obj, '%Y-%m-%dT%H:%M:%S.%f')
            data = time_obj.strftime('%Y-%m-%d %H:%M:%S')

        return data
