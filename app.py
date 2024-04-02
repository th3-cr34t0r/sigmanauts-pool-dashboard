from flask import Flask, render_template

from get_pool_data import GetPoolData

app = Flask(__name__)

pool_data = GetPoolData()


@app.route("/")
def home():
    return render_template("app.html",
                           pool_hashrate=pool_data.get_pool_stats("poolHashrate"),
                           connected_miners=pool_data.get_pool_stats("connectedMiners"),
                           pool_block_time=pool_data.get_stats("lastPoolBlockTime"),
                           pool_effort=pool_data.get_stats("poolEffort"),
                           payout_scheme=pool_data.get_payment_processing("payoutScheme"),
                           payment_threshold=pool_data.get_payment_processing("minimumPayment"),
                           pool_fee=pool_data.get_stats("poolFeePercent"),
                           pool_address=pool_data.get_stats("address"),
                           network_hashrate=pool_data.get_network_stats("networkHashrate"),
                           network_difficulty=pool_data.get_network_stats("networkDifficulty"),
                           network_block_height=pool_data.get_network_stats("blockHeight"),
                           network_last_block_time=pool_data.get_network_stats("lastNetworkBlockTime"))


@app.route("/wallet/<address>")
def wallet(address):
    return f"{address}"


if __name__ == "__main__":
    app.run(debug=True)
