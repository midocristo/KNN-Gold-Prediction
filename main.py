import src.fetch as fetch
import src.features as ft
import src.normalize as norm
import src.knn as knn
import src.evaluation as eval

#Buat data CSV dari harga gold yang berisi tanggal, open, high, low dan close
fetch.fetch_data()

#Membaca data CSV yang kita punya dan menyimpan dalam variabel data
data = ft.read_data()

#Disini kita menghitung semua fitur yang akan digunakan dengan memanggil fungsi yang berada dalam features.py
return_1 = ft.compute_return_1(data) #Fitur 1: Return 1 hari. Fitur ini mengandung nilai dari harga close hari ini terhadap harga close kemarin.
ma_5_gap = ft.compute_ma_5_gap(data) #Fitur 2: 5 Moving Average. Fitur ini berisi selisih harga pergerakan rata-rata dalam 5 hari dengan harga pada hari ini.
ma_20_gap = ft.compute_ma_20_gap(data) #Fitur 3: 20 Moving Average Gap. Sama seperti ma5, bedanya dia 20 hari terakhir.and
volatility = ft.compute_volatility(data) #Fitur 4: Volatility. Fitur ini ngukur seberapa besar tingkat volatil dari market pada tiap harinya.
rsi_14 = ft.compute_rsi_14(data) #Fitur 5: RSI 14. Fitur ini berisi mengindikasikan apakah emas dalam kondisi overbought/oversold dalam perubahan harga selama 14 hari.

#Menggabungkan fitur menjadi satu dictionary dan memberikan label. 1 Jika ada kenaikan harga esok hari, 0 jika tidak.
features, labels = ft.merge_label(data, return_1, ma_5_gap, ma_20_gap, volatility, rsi_14)

#Membuat data training dan data test dengan pembagian 80/20
split = int(0.8 * len(features))
train_features = features[:split]
train_label = labels[:split]
test_features = features[split:]
test_label = labels[split:]

#Disini kita melakukan proses normalisasi nilai min-max
min_val, max_val = norm.compute_min_max(train_features)
normalized_train = norm.normalize(train_features, min_val, max_val)
normalized_test = norm.normalize(test_features, min_val, max_val)

#Part utama dalam program ini. Menjalankan algoritma KNN untuk memprediksi hasil pada data test_features
predictions = knn.knn_predict(normalized_train, train_label, normalized_test, K=5)

#Evaluasi hasil
eval.print_result(test_label, predictions)
