from datetime import datetime
import requests


class GetPoolData:
    def __init__(self):
        self.base_api = "https://api.npoint.io/4dee266f5d8ed29ff27d/pool"

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
        url = '{}/{}'.format(self.base_api, arg)
        data = self.get_api_data(url)

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
        url = '{}/{}/{}'.format(self.base_api, 'poolStats', arg)
        data = self.get_api_data(url)

        # Hashes to Gigahashes
        if arg == "poolHashrate":
            data = str(round((int(data) / 1000000000), 3))

        return data

    def get_payment_processing(self, arg: str):
        # enabled
        # payoutScheme
        # minimumPayment
        url = '{}/{}/{}'.format(self.base_api, 'paymentProcessing', arg)
        data = self.get_api_data(url)

        return data

    def get_network_stats(self, arg: str):
        # blockHeight
        # networkHashrate
        # networkDifficulty
        # lastNetworkBlockTime
        url = '{}/{}/{}'.format(self.base_api, 'networkStats', arg)
        data = self.get_api_data(url)

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
