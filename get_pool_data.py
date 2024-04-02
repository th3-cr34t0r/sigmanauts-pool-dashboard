import requests
from datetime import datetime


class GetPoolData:
    def __init__(self):
        self.base_api = "http://15.204.211.130:4000/api/pools/ErgoSigmanauts"

    def get_api_data(self, api_url):
        data = requests.get(url=api_url)
        data.raise_for_status()
        return data.json()

    def get_stats(self, arg: str):
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
        data = self.get_api_data(self.base_api)['pool'][f'{arg}']

        # Round totalPaid
        if arg == "totalPaid":
            data = str(round(int(data), 2))

        elif arg == "poolEffort":
            data = str(round(float(data) * 100, 2))

        elif arg == "lastPoolBlockTime":
            time_str = data
            time_obj = time_str[:26] + 'Z'  # Truncate to 6 digits for microseconds
            time_obj = datetime.strptime(time_obj, '%Y-%m-%dT%H:%M:%S.%fZ')
            data = time_obj.strftime('%Y-%m-%d %H:%M:%S')

        return data

    def get_pool_stats(self, arg: str):
        # VALID ARGS:
        # poolHashrate
        # connectedMiners
        # sharesPerSecond
        data = self.get_api_data(self.base_api)['pool']['poolStats'][f'{arg}']

        # Hashes to Gigahashes
        if arg == "poolHashrate":
            data = str(round((int(data) / 1000000000), 3))

        return data

    def get_payment_processing(self, arg: str):
        # enabled
        # payoutScheme
        # minimumPayment
        data = self.get_api_data(self.base_api)['pool']['paymentProcessing'][f'{arg}']

        return data

    def get_network_stats(self, arg: str):
        # blockHeight
        # networkHashrate
        # networkDifficulty
        # lastNetworkBlockTime
        data = self.get_api_data(self.base_api)['pool']['networkStats'][f'{arg}']

        # Hashes to Terahashes
        if arg == 'networkHashrate':
            data = str(round(float(data) / 1000000000000, 3))

        # to Peta
        elif arg == 'networkDifficulty':
            data = str(round(float(data) / 1000000000000000, 3))

        elif arg == 'lastNetworkBlockTime':
            time_str = data
            time_obj = time_str[:26] + 'Z'  # Truncate to 6 digits for microseconds
            time_obj = datetime.strptime(time_obj, '%Y-%m-%dT%H:%M:%S.%fZ')
            data = time_obj.strftime('%Y-%m-%d %H:%M:%S')

        return data
