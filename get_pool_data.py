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
            time_obj = datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%S.%fZ')
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