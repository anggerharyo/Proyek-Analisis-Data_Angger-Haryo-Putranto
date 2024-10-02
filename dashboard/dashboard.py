import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

# Judul untuk Dashboard
st.title('Dashboard Analisis Penggunaan Sepeda Harian')

# Membaca data (pastikan file df_day.csv ada di direktori yang sama dengan script)
df_day = pd.read_csv("https://raw.githubusercontent.com/anggerharyo/Proyek-Analisis-Data_Angger-Haryo-Putranto/main/dashboard/Sharing Bike Dataset/day.csv")

# Pertanyaan 1: Korelasi cuaca dengan penggunaan sepeda
st.subheader('Korelasi Faktor Cuaca dan Penggunaan Sepeda Harian')
correlation_values = df_day[['temp', 'atemp', 'hum', 'windspeed', 'cnt']].corr()

# Heatmap untuk visualisasi korelasi
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_values, cbar=True, square=True, annot=True, annot_kws={'size': 8}, cmap='Blues')
plt.title('Korelasi Faktor Cuaca dan Penggunaan Sepeda Harian')
st.pyplot(plt)

# Insight
st.write("""
Dari hasil analisis, suhu (temp) memiliki hubungan positif yang kuat dengan jumlah pengguna sepeda.
Kelembapan (hum) dan kecepatan angin (windspeed) memiliki korelasi negatif yang lemah terhadap jumlah pengguna sepeda.
""")

# Pertanyaan 2: Penggunaan sepeda berdasarkan hari kerja dan akhir pekan
st.subheader('Rata-rata Penggunaan Sepeda: Hari Kerja vs Akhir Pekan')
workingday_usage = df_day.groupby('workingday')['cnt'].mean()

# Menampilkan rata-rata penggunaan
st.write(f"Rata-rata penggunaan sepeda pada Hari Kerja: {int(workingday_usage[1])}")
st.write(f"Rata-rata penggunaan sepeda pada Akhir Pekan: {int(workingday_usage[0])}")

# Visualisasi pola penggunaan sepeda hari kerja vs akhir pekan
plt.figure(figsize=(6, 4))
sns.barplot(x=['Akhir Pekan', 'Hari Kerja'], y=workingday_usage.values)
plt.title('Rata-rata Penggunaan Sepeda: Hari Kerja vs Akhir Pekan')
plt.ylabel('Jumlah Pengguna Sepeda')
st.pyplot(plt)

# Analisis Lanjutan: Clustering penggunaan sepeda berdasarkan musim dan hari kerja
st.subheader('Clustering Penggunaan Sepeda Berdasarkan Musim dan Hari Kerja')
usage_summary = df_day.groupby(['season', 'workingday']).agg({'cnt': 'mean'}).reset_index()

# Label musim
season_labels = {1: 'Musim Semi', 2: 'Musim Panas', 3: 'Musim Gugur', 4: 'Musim Dingin'}
usage_summary['season'] = usage_summary['season'].map(season_labels)

# Clustering berdasarkan penggunaan sepeda
usage_summary['Cluster'] = pd.qcut(usage_summary['cnt'], q=3, labels=['Rendah', 'Sedang', 'Tinggi'])
usage_summary['cnt'] = usage_summary['cnt'].round().astype(int)

# Visualisasi hasil clustering
plt.figure(figsize=(12, 6))
sns.scatterplot(data=usage_summary, x='season', y='cnt', hue='Cluster', palette='Set1', s=100)
plt.title('Clustering Penggunaan Sepeda Berdasarkan Musim dan Hari Kerja')
plt.xlabel('Musim')
plt.ylabel('Rata-rata Penggunaan Sepeda')
plt.legend(title='Cluster')
st.pyplot(plt)

# Menampilkan hasil summary
st.write(usage_summary)
