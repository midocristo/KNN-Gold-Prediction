import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from datetime import datetime
import src.features as ft
import src.normalize as norm
import src.knn as knn
import src.evaluation as eval
from datetime import datetime as dt

st.set_page_config(page_title="Prediksi Emas KNN", layout="wide")
st.title("Prediksi Arah Harga Emas Dengan Algoritma KNN")

st.sidebar.header("Atur Parameter")
tanggal_mulai = st.sidebar.date_input("Tanggal Mulai", value=datetime(2020, 1, 1))
tanggal_akhir = st.sidebar.date_input("Tanggal Akhir", value=datetime.today())
K = st.sidebar.slider("Jumlah Tetangga (K)", 1, 15, 5, 2)
tombol = st.sidebar.button("Jalankan Prediksi")

@st.cache_data
def baca_data():
    data = ft.read_data("data/gold_data.csv")
    return data

data_mentah = baca_data()

if tombol:
    start_str = str(tanggal_mulai)
    end_str = str(tanggal_akhir)
    data_filtered = []
    for row in data_mentah:
        if row["Date"] >= start_str and row["Date"] <= end_str:
            data_filtered.append(row)

    if len(data_filtered) == 0:
        st.error("Tidak ada data pada rentang tanggal yang dipilih.")
    else:
        with st.spinner("Menghitung fitur..."):
            return_1 = ft.compute_return_1(data_filtered)
            ma_5_gap = ft.compute_ma_5_gap(data_filtered)
            ma_20_gap = ft.compute_ma_20_gap(data_filtered)
            volatility = ft.compute_volatility(data_filtered)
            rsi_14 = ft.compute_rsi_14(data_filtered)

        features, labels = ft.merge_label(data_filtered, return_1, ma_5_gap, ma_20_gap, volatility, rsi_14)

        if len(features) < 30:
            st.warning("Data yang valid terlalu sedikit (minimal ~30 hari setelah fitur dihitung).")
        else:
            split = int(0.8 * len(features))
            train_features = features[:split]
            train_label = labels[:split]
            test_features = features[split:]
            test_label = labels[split:]

            min_val, max_val = norm.compute_min_max(train_features)
            normalized_train = norm.normalize(train_features, min_val, max_val)
            normalized_test = norm.normalize(test_features, min_val, max_val)

            predictions = knn.knn_predict(normalized_train, train_label, normalized_test, K=K)

            accuracy_p = eval.accuracy(test_label, predictions)
            precision_p = eval.precision(test_label, predictions)
            recall_p = eval.recall(test_label, predictions)

            st.subheader("Metrik Evaluasi")
            kol1, kol2, kol3 = st.columns(3)
            kol1.metric("Akurasi",   f"{accuracy_p  * 100:.1f}%")
            kol2.metric("Precision", f"{precision_p * 100:.1f}%")
            kol3.metric("Recall",    f"{recall_p    * 100:.1f}%")

            awal_test = 20 + split
            akhir_test = awal_test + len(predictions)
            test_tanggal = [dt.strptime(row["Date"], "%Y-%m-%d") for row in data_filtered[awal_test:akhir_test]]
            test_close   = [row["Close"] for row in data_filtered[awal_test:akhir_test]]

            st.subheader("Harga Close & Sinyal Prediksi")
            fig, ax = plt.subplots(figsize=(12, 5))
            ax.plot(test_tanggal, test_close, color="blue", linewidth=1.5, label="Harga Close")

            selisih_harga = max(test_close) - min(test_close)
            offset = selisih_harga * 0.01

            for i, (pred, aktual) in enumerate(zip(predictions, test_label)):
                if pred == 1:
                    warna = "green" if aktual == 1 else "red"
                    simbol = "^"
                    y_pos = test_close[i] + offset
                else:
                    warna = "green" if aktual == 0 else "red"
                    simbol = "v"
                    y_pos = test_close[i] - offset

                ax.scatter(test_tanggal[i], y_pos,
                           color=warna, marker=simbol, s=100,
                           edgecolors="black", linewidth=0.8, zorder=5)

            legenda = [
                Line2D([0], [0], marker="^", color="w", markerfacecolor="green",  markersize=12, label="Naik (benar) ✅"),
                Line2D([0], [0], marker="^", color="w", markerfacecolor="red",    markersize=12, label="Naik (salah) ❌"),
                Line2D([0], [0], marker="v", color="w", markerfacecolor="green",  markersize=12, label="Turun (benar) ✅"),
                Line2D([0], [0], marker="v", color="w", markerfacecolor="red",    markersize=12, label="Turun (salah) ❌"),
                Line2D([0], [0], color="blue", linewidth=2,                                      label="Harga Close"),
            ]
            ax.legend(handles=legenda, loc="upper left")
            ax.set_xlabel("Tanggal")
            ax.set_ylabel("Harga (USD)")
            ax.grid(True, alpha=0.3)
            fig.autofmt_xdate()
            st.pyplot(fig)

else:
    st.info("Silakan atur parameter di sidebar, lalu klik Jalankan Prediksi.")
