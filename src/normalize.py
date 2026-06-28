def compute_min_max(trains_feature):
    min_value = {
        "min_return": trains_feature[0][0],
        "min_ma_5_gap": trains_feature[0][1],
        "min_ma_20_gap": trains_feature[0][2],
        "min_volatility": trains_feature[0][3],
        "min_rsi": trains_feature[0][4],
    }
    max_value = {
        "max_return": trains_feature[0][0],
        "max_ma_5_gap": trains_feature[0][1],
        "max_ma_20_gap": trains_feature[0][2],
        "max_volatility": trains_feature[0][3],
        "max_rsi": trains_feature[0][4],
    }

    for row in trains_feature:
        if row[0] < min_value["min_return"]:
            min_value["min_return"] = row[0]
        if row[0] > max_value["max_return"]:
            max_value["max_return"] = row[0]

        if row[1] < min_value["min_ma_5_gap"]:
            min_value["min_ma_5_gap"] = row[1]
        if row[1] > max_value["max_ma_5_gap"]:
            max_value["max_ma_5_gap"] = row[1]

        if row[2] < min_value["min_ma_20_gap"]:
            min_value["min_ma_20_gap"] = row[2]
        if row[2] > max_value["max_ma_20_gap"]:
            max_value["max_ma_20_gap"] = row[2]

        if row[3] < min_value["min_volatility"]:
            min_value["min_volatility"] = row[3]
        if row[3] > max_value["max_volatility"]:
            max_value["max_volatility"] = row[3]

        if row[4] < min_value["min_rsi"]:
            min_value["min_rsi"] = row[4]
        if row[4] > max_value["max_rsi"]:
            max_value["max_rsi"] = row[4]

    return min_value, max_value

def normalize(features, min_value, max_value):
    normalized = []
    for row in features:
        normalized_row = [
            (row[0] - min_value["min_return"])     / (max_value["max_return"]     - min_value["min_return"]),
            (row[1] - min_value["min_ma_5_gap"])    / (max_value["max_ma_5_gap"]    - min_value["min_ma_5_gap"]),
            (row[2] - min_value["min_ma_20_gap"])   / (max_value["max_ma_20_gap"]   - min_value["min_ma_20_gap"]),
            (row[3] - min_value["min_volatility"]) / (max_value["max_volatility"] - min_value["min_volatility"]),
            (row[4] - min_value["min_rsi"])        / (max_value["max_rsi"]        - min_value["min_rsi"])
        ]
        normalized.append(normalized_row)
    return normalized
