from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

debug = True

if debug:
    @app.route("/", methods=["POST", "GET"])
    def home():
        if request.method == "POST":
            user_address = request.form["address"]
            if user_address != "":
                return redirect(url_for("wallet", address=user_address))
            else:
                return redirect(url_for("home"))
        else:
            return render_template("app.html",
                                   pool_hashrate="poolHashrate",
                                   display_page="main.html",
                                   connected_miners="connectedMiners",
                                   pool_block_time="lastPoolBlockTime",
                                   pool_effort="poolEffort",
                                   payout_scheme="payoutScheme",
                                   payment_threshold="minimumPayment",
                                   pool_fee="poolFeePercent",
                                   pool_address="address",
                                   network_hashrate="networkHashrate",
                                   network_difficulty="networkDifficulty",
                                   network_block_height="blockHeight",
                                   network_last_block_time="lastNetworkBlockTime")

else:
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
                                   network_last_block_time=pool_data.get_network_stats(data_json,
                                                                                       "lastNetworkBlockTime"))


@app.route("/wallet/<address>")
def wallet(address):
    return render_template("app.html",
                           display_page="session.html",
                           address=address)


if __name__ == "__main__":
    app.run(debug=True)
