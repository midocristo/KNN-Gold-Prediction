import csv

def read_data(destination="data/gold_data.csv"):
    data = []
    with open(destination) as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append({
                "Date": row["Date"],
                "Open": float(row["Open"]),
                "High": float(row["High"]),
                "Low": float(row["Low"]),
                "Close": float(row["Close"])
            })
    return data


def compute_return_1(data):
    return_1 = []
    return_1.append(0)
    for i in range(1, len(data)):
        return_1.append((data[i]["Close"] - data[i-1]["Close"]) / data[i-1]["Close"])
    return return_1

def compute_ma_5_gap(data):
    last_5_days_close = 0
    list_ma_5_gap = []
    for i in range(len(data)):
        if i < 4:
            last_5_days_close += data[i]["Close"]
            list_ma_5_gap.append(0)
        elif i == 4:
            last_5_days_close += data[i]["Close"]
            ma5 = last_5_days_close / 5
            list_ma_5_gap.append((data[i]["Close"] - ma5) / ma5)
        else:
            last_5_days_close = last_5_days_close + data[i]["Close"] - data[i-5]["Close"]
            ma5 = last_5_days_close / 5
            list_ma_5_gap.append((data[i]["Close"] - ma5) / ma5)

    return list_ma_5_gap

def compute_ma_20_gap(data):
    last_20_days_close = 0
    list_ma_20_gap = []
    for i in range(len(data)):
        if i < 19:
            last_20_days_close += data[i]["Close"]
            list_ma_20_gap.append(0)
        elif i == 19:
            last_20_days_close += data[i]["Close"]
            ma20 = last_20_days_close / 20
            list_ma_20_gap.append((data[i]["Close"] - ma20) / ma20)
        else:
            last_20_days_close = last_20_days_close + data[i]["Close"] - data[i-20]["Close"]
            ma20 = last_20_days_close / 20
            list_ma_20_gap.append((data[i]["Close"] - ma20) / ma20)

    return list_ma_20_gap

def compute_volatility(data):
    list_volatility = []
    for i in range(len(data)):
        volatility = (data[i]["High"] - data[i]["Low"]) / data[i]["Close"]
        list_volatility.append(volatility)
    return list_volatility

def compute_rsi_14(data):
    list_gain = []
    list_loss = []
    list_rsi = [0] * 14

    for i in range(1, 15):
        change = data[i]["Close"] - data[i-1]["Close"]
        if change > 0:
            list_gain.append(change)
            list_loss.append(0)
        elif change < 0:
            list_gain.append(0)
            list_loss.append(abs(change))
        else:
            list_gain.append(0)
            list_loss.append(0)

    avg_gain = sum(list_gain) / 14
    avg_loss = sum(list_loss) / 14

    if avg_loss == 0:
        list_rsi.append(100)
    else:
        rs = avg_gain / avg_loss
        list_rsi.append(100 - (100 / (1 + rs)))

    for i in range(15, len(data)):
        change = data[i]["Close"] - data[i-1]["Close"]
        if change > 0:
            gain = change
            loss = 0
        elif change < 0:
            gain = 0
            loss = abs(change)
        else:
            gain = 0
            loss = 0

        avg_gain = (avg_gain * 13 + gain) / 14
        avg_loss = (avg_loss * 13 + loss) / 14

        if avg_loss == 0:
            list_rsi.append(100)
        else:
            rs = avg_gain / avg_loss
            list_rsi.append(100 - (100 / (1 + rs)))

    return list_rsi

def merge_label(data, return_1, ma_5_gap, ma_20_gap, volatility, rsi_14):
    features = []
    labels = []
    label = 0

    start = 20
    end = len(data) - 2

    for i in range(start, end + 1):
        f1 = return_1[i]
        f2 = ma_5_gap[i]
        f3 = ma_20_gap[i]
        f4 = volatility[i]
        f5 = rsi_14[i]

        if data[i+1]["Close"] > data[i]["Close"]:
            label = 1
        else:
            label = 0

        features.append([f1, f2, f3, f4, f5])
        labels.append(label)

    return features, labels
