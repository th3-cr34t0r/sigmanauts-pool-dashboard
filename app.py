import pandas as pd
from flask import Flask, redirect, url_for, render_template, request

app = Flask(__name__)

from get_pool_data import GetPoolData, get_api_data
from network_data import NetworkStats
pool_data = GetPoolData()
network_data = NetworkStats()

#save last 100 block infos to csv:
last_100_block_data = network_data.get_block_data(5)


@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        user_address = request.form["address"]
        if len(user_address) == 51:
            return redirect(url_for("wallet", address=user_address))
        else:
            return redirect(url_for("home"))
    else:

        data_json = get_api_data()
        return render_template("app.html",
                               display_page="main.html",
                               pool_hashrate=pool_data.get_pool_stats(data_json, "poolHashrate"),
                               connected_miners=pool_data.get_pool_stats(data_json, "connectedMiners"),
                               pool_block_time=pool_data.get_stats(data_json, "lastPoolBlockTime"),
                               pool_effort=pool_data.get_stats(data_json, "poolEffort"),
                               payout_scheme=pool_data.get_payment_processing(data_json, "payoutScheme"),
                               payment_threshold=pool_data.get_payment_processing(data_json, "minimumPayment"),
                               pool_fee=pool_data.get_stats(data_json, "poolFeePercent"),
                               pool_address=pool_data.get_stats(data_json, "address"),
                               network_hashrate=pool_data.get_network_stats(data_json, "networkHashrate"),
                               network_difficulty=pool_data.get_network_stats(data_json, "networkDifficulty"),
                               network_block_height=pool_data.get_network_stats(data_json, "blockHeight"),
                               network_last_block_time=pool_data.get_network_stats(data_json, "lastNetworkBlockTime"))


@app.route("/wallet/<address>")
def wallet(address):
    miner_data = pool_data.get_wallet_stats(address)

    if miner_data != "Miner data not available!":

        data_json = get_api_data()
        block_info = pool_data.get_last_block_info()
        workers_data = pool_data.get_workers_stats(address)

        labels = ["11511", "11512", "11513", "11514", "11515", "11516", "11517", "11518"]
        hashrate_values = [13.52, 13.6, 14.1, 13.63, 14.5, 14.7, 14.6, 15]
        diff_values = [1.5, 1.5, 1.67, 1.67, 1.74, 1.74, 1.73, 1.8]

        return render_template("app.html",
                               display_page="session.html",
                               miner_address=address,
                               network_hashrate=pool_data.get_network_stats(data_json, "networkHashrate"),
                               network_difficulty=pool_data.get_network_stats(data_json, "networkDifficulty"),
                               block_reward="Work in progress",
                               block_reduction_time="Work in progress",
                               erg_price_usd="Work in progress",
                               pool_hashrate=pool_data.get_pool_stats(data_json, "poolHashrate"),
                               pool_miners=pool_data.get_pool_stats(data_json, "connectedMiners"),
                               block_found_time=pool_data.calculate_time_to_find_block(pool_data.get_network_stats(data_json, "networkHashrate"), pool_data.get_pool_stats(data_json, "poolHashrate")),
                               pool_effort=pool_data.get_stats(data_json, "poolEffort"),
                               pool_total_blocks=pool_data.get_stats(data_json, "totalBlocks"),
                               block_progress=block_info["block_progress"],
                               block_effort=block_info["block_effort"],
                               block_last_reward=block_info["block_last_reward"],
                               block_miner=block_info["block_miner"],
                               block_time=block_info["block_time"],
                               miner_hashrate=miner_data["miner_hashrate"],
                               miner_avg_hashrate="Work in progress",
                               miner_pending_shares=miner_data["miner_pending_shares"],
                               miner_pending_balance=miner_data["miner_pending_balance"],
                               miner_total_paid=miner_data["miner_total_paid"],
                               miner_contribution=miner_data["miner_contribution"],
                               workers_data=workers_data,
                               labels=labels,
                               hashrate_values=hashrate_values,
                               diff_values=diff_values
                               )
    else:
        return redirect(url_for("home"))


@app.route("/faq")
def faq():
    return render_template("app.html", display_page="faq.html")


@app.route("/get-started")
def get_started():
    return render_template("app.html", display_page="get-started.html")


if __name__ == "__main__":
    app.run(debug=True)
