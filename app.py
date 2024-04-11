from flask import Flask, redirect, url_for, render_template, request

app = Flask(__name__)

from get_pool_data import GetPoolData, get_api_data

pool_data = GetPoolData()


@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        user_address = request.form["address"]
        if user_address != "":
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
    pool_data = GetPoolData()

    data_json = get_api_data()
    block_info = pool_data.get_last_block_info()
    miner_data = pool_data.get_wallet_stats(address)
    workers_data = pool_data.get_workers_stats(address)

    if miner_data != "Miner data not available!":
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
                               workers_data=workers_data
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
