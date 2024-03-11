import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def load_data(file_path):
    df = pd.read_csv(file_path)
    return df


def main():
    st.set_page_config(
        page_title="E-commerce Data Dashboard", page_icon=":chart_with_upwards_trend:"
    )

    # Load the data
    file_path = "./e_commerce.csv"
    df = load_data(file_path)

    # Sidebar to select the tab
    tab = st.sidebar.radio(
        "JUMP TO 🚀🚀:",
        [
            "EDA Awal :calendar:",
            "Analisis 10 Produk Teratas :bar_chart:",
            "Analisis Metode Pembayaran💳",
            "Analisis Pelanggan 🧐",
            "Korelasi Antar Kolom/ Faktor",
            "Covariance",
            "Q&A Section",
        ],
    )

    if tab == "EDA Awal :calendar:":
        eda_awal(df)
    elif tab == "Analisis 10 Produk Teratas :bar_chart:":
        analisis_10_produk_teratas(df)
    elif tab == "Analisis Metode Pembayaran💳":
        analisis_payment(df)
    elif tab == "Analisis Pelanggan 🧐":
        analisis_customers(df)
    elif tab == "Korelasi Antar Kolom/ Faktor":
        korelasi(df)
    elif tab == "Covariance":
        covariance(df)
    elif tab == "Q&A Section":
        q_and_a_section(df)


def eda_awal(df):
    st.header("E-Commerce Public Dataset EDA")

    # EDA: Evolution of E-commerce Over Time
    st.subheader("Evolusi E-Commerce dari Waktu ke Waktu")
    df["order_purchase_timestamp"] = pd.to_datetime(df["order_purchase_timestamp"])
    df["Year"] = df["order_purchase_timestamp"].dt.year
    year_counts = df["Year"].value_counts().sort_index()
    st.bar_chart(year_counts)
    st.line_chart(year_counts)
    st.write(
        """
    Grafik batang dan garis di atas menunjukkan evolusi e-commerce dari tahun 2016 hingga 2018 di Brasil. 
    Terlihat ada lonjakan yang signifikan dari 2016 ke 2017, namun pertumbuhan dari 2017 ke 2018 relatif stabil.
    """
    )

    # EDA: Online Purchases per Month
    st.subheader("Pembelian Online per Bulan")
    df["Month"] = df["order_purchase_timestamp"].dt.month_name()
    month_counts = df["Month"].value_counts().sort_index()
    st.bar_chart(month_counts)
    st.write(
        """
    Grafik batang di atas menampilkan pembelian online per bulan di Brasil. Diharapkan bahwa November (Black Friday) 
    atau Desember (Natal) memiliki nilai tertinggi karena peristiwa musiman atau promosi. Analisis lebih lanjut 
    dapat dilakukan untuk memahami perilaku belanja selama periode ini.
    """
    )

    # EDA: Online Purchases per Month-Year
    st.subheader("Pembelian Online per Bulan-Tahun")
    df["MonthY"] = df["order_purchase_timestamp"].dt.strftime("%b%Y")
    month_year_counts = df["MonthY"].value_counts().sort_index()
    st.bar_chart(month_year_counts)
    st.write(
        """
    Grafik batang di atas menggabungkan bulan dan tahun untuk mengamati tren dari waktu ke waktu. 
    Ini dapat berguna untuk menganalisis distribusi pembelian dari waktu ke waktu.
    """
    )

    # EDA: Online Purchases per Day of the Week
    st.subheader("Pembelian Online per Hari dalam Seminggu")
    df["Day"] = df["order_purchase_timestamp"].dt.day_name()
    day_counts = df["Day"].value_counts().sort_index()
    st.bar_chart(day_counts)
    st.write(
        """
    Grafik batang di atas menunjukkan pembelian online per hari dalam seminggu di Brasil. 
    Diamati bahwa lebih banyak belanja online terjadi pada hari kerja dibandingkan dengan akhir pekan.
    """
    )


def analisis_10_produk_teratas(df):
    st.header("Analisis 10 Produk Teratas")

    # Analisis Kategori Produk Teratas
    st.subheader("Kategori Produk Teratas")
    top_10_category = (
        df["product_category_name_english"]
        .value_counts()
        .sort_values(ascending=False)[:10]
    )
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.barplot(y=top_10_category.index, x=top_10_category.values)
    plt.title("Top 10 Kategori Produk", fontsize=20)
    st.pyplot(fig)
    st.write(
        """
    Di bawah ini diperoleh 10 kategori populer teratas berdasarkan data e-commerce di Brasil.
    """
    )

    # Analisis Harga Rata-rata pada Setiap Kategori
    st.subheader("Harga Rata-rata pada Setiap Kategori")
    average_price = (
        df.groupby("product_category_name_english")["price"].mean().sort_values()
    )
    fig, ax = plt.subplots(figsize=(12, 10))
    sns.barplot(y=average_price.index, x=average_price.values)
    plt.title("Harga Rata-rata", fontsize=20)
    st.pyplot(fig)
    st.write(
        """
    Grafik batang di atas menampilkan harga rata-rata pada setiap kategori produk. Harga rata-rata untuk 
    beberapa kategori produk dapat dilihat di bawah ini.
    """
    )

    # Analisis Harga Rata-rata dari 'Kategori 10 Teratas'
    st.subheader("Harga Rata-rata produk Kategori 10 Teratas")
    top_category = df[df["product_category_name_english"].isin(top_10_category.index)]
    price_top_category = round(
        top_category.groupby("product_category_name_english")["price"]
        .mean()
        .sort_values(ascending=False),
        2,
    )
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.barplot(y=price_top_category.index, x=price_top_category.values)
    plt.title("Harga Rata-rata Kategori Teratas", fontsize=20)
    st.pyplot(fig)
    st.write(
        """
    Grafik batang di atas menampilkan harga rata-rata dari 'Kategori 10 Teratas'. 
    Ini membantu memahami harga rata-rata produk yang paling diminati oleh pelanggan.
    """
    )

    # Boxplot Harga Rata-rata
    st.subheader("Boxplot Harga Rata-rata")
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.boxplot(x=average_price)
    plt.title("Harga Rata-rata", fontsize=20)
    st.pyplot(fig)
    st.write(
        """
    Boxplot di atas menampilkan distribusi harga rata-rata produk di seluruh kategori.
    """
    )

    # Boxplot Harga Rata-rata 'Kategori 10 Teratas'
    st.subheader("Boxplot Harga Rata-rata Kategori Teratas")
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.boxplot(x=price_top_category)
    plt.title("Harga Rata-rata Kategori Teratas", fontsize=20)
    st.pyplot(fig)
    st.write(
        """
    Boxplot di atas menampilkan distribusi harga rata-rata produk dari 'Kategori 10 Teratas'.
    """
    )


def analisis_payment(df):
    st.header("Analisis Metode Pembayaran")

    # Sample dari kolom payment_type
    st.subheader("Sample Metode Pembayaran")
    st.write(df.payment_type.sample(15))

    # Jumlah metode pembayaran unik
    st.subheader("Jumlah Metode Pembayaran Unik")
    st.write("Jumlah metode pembayaran: {}".format(df.payment_type.nunique()))

    # Metode pembayaran unik
    st.subheader("Metode Pembayaran Unik")
    st.write("Berikut metode pembayarannya: {}".format(df.payment_type.unique()))

    # Pie chart untuk metode pembayaran
    st.subheader("Diagram Lingkaran Metode Pembayaran yang Paling Sering Digunakan")
    payment_counts = df["payment_type"].value_counts()
    fig, ax = plt.subplots(figsize=(10, 8))
    plt.pie(
        payment_counts,
        labels=payment_counts.index,
        autopct="%1.1f%%",
        startangle=140,
        shadow=True,
    )
    plt.title("Metode Pembayaran yang Paling Sering Digunakan", fontsize=20)
    plt.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle.
    st.pyplot(fig)
    st.write(
        """
    Diagram lingkaran di atas menampilkan persentase penggunaan metode pembayaran yang berbeda.
    """
    )

    # Bar chart untuk metode pembayaran per tahun
    st.subheader("Metode Pembayaran per Tahun")
    payment_per_year = df.groupby("Year")["payment_type"].value_counts().unstack()
    fig, ax = plt.subplots(figsize=(12, 8))
    payment_per_year.plot(kind="bar", ax=ax)
    plt.title("Metode Pembayaran per Tahun", fontsize=20)
    plt.xlabel("Tahun")
    plt.ylabel("Jumlah Transaksi")
    st.pyplot(fig)
    st.write(
        """
    Grafik batang di atas menunjukkan jumlah transaksi untuk setiap metode pembayaran per tahun.
    """
    )


def analisis_customers(df):
    st.header("Analisis Pelanggan 🧐")

    # Tampilkan gambar peta Brazil
    st.subheader("Peta Pembagian Wilayah Brazil")
    st.image(
        "https://st4.depositphotos.com/1374738/23094/v/950/depositphotos_230940566-stock-illustration-map-brazil-divisions-states.jpg",
        use_column_width=True,
    )
    st.write(
        """
    Gambar di atas menunjukkan pembagian wilayah di Brazil.
    """
    )

    # Analisis pelanggan berdasarkan negara bagian
    st.subheader("Analisis Pelanggan berdasarkan Negara Bagian")
    top_states = df["customer_state"].value_counts()
    fig, ax = plt.subplots(figsize=(16, 10))
    sns.barplot(y=top_states.index, x=top_states.values)
    plt.title("Negara Bagian", fontsize=20)
    st.pyplot(fig)
    st.write(
        """
    Sebagian besar pelanggan berasal dari Sao Paulo, diikuti oleh Rio de Janeiro.
    """
    )

    # Analisis waktu pengiriman per negara bagian
    st.subheader("Analisis Waktu Pengiriman per Negara Bagian")
    df["order_delivered_customer_date"] = pd.to_datetime(
        df["order_delivered_customer_date"]
    )
    df["order_purchase_timestamp"] = pd.to_datetime(df["order_purchase_timestamp"])
    df["delivery_time"] = (
        df["order_delivered_customer_date"] - df["order_purchase_timestamp"]
    ).dt.days
    delivery_per_state = df.groupby("customer_state")["delivery_time"].mean()
    fig, ax = plt.subplots(figsize=(10, 7))
    delivery_per_state.plot(kind="bar")
    plt.title("Waktu Pengiriman per Negara Bagian", fontsize=20)
    plt.xlabel("Negara Bagian")
    plt.ylabel("Waktu Pengiriman (hari)")
    st.pyplot(fig)
    st.write(
        """
    Waktu pengiriman paling lama adalah milik Negara bagian Paraiba. Kami tidak memiliki set data penjual di sini untuk membandingkan jarak antara asal (lokasi penjual) dan tujuan (lokasi pembeli).
    """
    )


def korelasi(df):
    st.header("Korelasi Antar Kolom/ Faktor")

    # Fungsi untuk memberikan warna pada nilai korelasi
    def adding_colour(val):
        if val < 0:
            color = "red"
        elif val < 1:
            color = "green"
        else:
            color = "black"
        return "color: %s" % color

    # Korelasi antar kolom numerik
    st.subheader("Korelasi Antar Kolom Numerik")
    numeric_df = df.select_dtypes(include=["number"])
    corr = numeric_df.corr()
    styled_corr = corr.style.applymap(adding_colour)
    st.dataframe(styled_corr)
    st.write(
        """
    Korelasi menunjukkan adanya saling ketergantungan antara dua variabel atau lebih. Nilai korelasi terletak antara -1 dan 1 (korelasi bukan berarti sebab-akibat).
    """
    )

    # Scatter plot untuk korelasi antara harga dan ongkos kirim
    st.subheader("Korelasi antara Harga dan Ongkos Kirim")
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.scatterplot(data=df, x="price", y="freight_value")
    plt.title("Korelasi antara Harga dan Ongkos Kirim", fontsize=20)
    st.pyplot(fig)
    st.write(
        """
    Scatter plot di atas menampilkan korelasi antara harga barang dan ongkos kirim. Anda dapat melihat distribusi titik data untuk memahami hubungan antara kedua variabel.
    """
    )

    # Scatter plot untuk korelasi antara berat barang dan ongkos kirim
    st.subheader("Korelasi antara Berat Barang dan Ongkos Kirim")
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.scatterplot(data=df, x="product_weight_g", y="freight_value")
    plt.title("Korelasi antara Berat Barang dan Ongkos Kirim", fontsize=20)
    st.pyplot(fig)
    st.write(
        """
    Scatter plot di atas menampilkan korelasi antara berat barang dan ongkos kirim. Anda dapat melihat distribusi titik data untuk memahami hubungan antara kedua variabel.
    """
    )


def covariance(df):
    st.header("Covariance")

    # Fungsi untuk memberikan warna pada nilai covariance
    def add_colour(val):
        if val < 0:
            color = "red"
        elif val < 1:
            color = "green"
        else:
            color = "black"
        return "color: %s" % color

    numeric_df = df.select_dtypes(include=["number"])
    cov = numeric_df.cov()
    st.write("Covariance Matrix:")
    st.dataframe(cov.style.applymap(add_colour))

    st.subheader("Covariance antara Harga dan Ongkos Kirim")
    cov_price_freight = df["freight_value"].cov(df["price"])
    st.write(f"Covariance antara Harga dan Ongkos Kirim: {cov_price_freight:.2f}")

    st.subheader("Covariance antara Berat Barang dan Ongkos Kirim")
    cov_weight_freight = df["freight_value"].cov(df["product_weight_g"])
    st.write(
        f"Covariance antara Berat Barang dan Ongkos Kirim: {cov_weight_freight:.2f}"
    )


def q_and_a_section(df):
    st.header("Q&A Section")

    st.subheader(
        "Pertanyaan 1: Pada hari apa saja dalam seminggu konsumen Brasil cenderung melakukan belanja online? Dan pada hari apa penjual harus melakukan penambahan?"
    )
    st.write("Jawab:")
    st.write(
        "Pelanggan Brasil cenderung aktif dari Senin hingga Jumat. Penjual harus melakukan penambahan dan promosi pada hari kerja daripada akhir pekan."
    )

    # Visualisasi untuk hari belanja online
    day = df.groupby("Day", observed=False).size().sort_values()
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.barplot(y=day.index, x=day.values, ax=ax)
    plt.title("Days", fontsize=20)
    st.pyplot(fig)

    st.write("Kesimpulan:")
    st.markdown(
        "1. **Hari-hari Populer untuk Belanja Online**: Konsumen di Brasil cenderung lebih sering melakukan belanja online pada hari kerja dibandingkan dengan akhir pekan. Hal ini menunjukkan bahwa aktivitas belanja online lebih tinggi pada hari Senin hingga Jumat."
    )
    st.markdown(
        "2. **Diskon pada Hari Kerja**: Mengingat aktivitas belanja online yang tinggi pada hari kerja, penjual harus mempertimbangkan untuk mengadakan diskon atau promosi khusus pada hari-hari tersebut."
    )
    st.markdown(
        "3. **Penambahan Barang**: Pada hari-hari tersibuk dalam seminggu, yaitu pada hari kerja (Senin hingga Jumat), penjual harus mempertimbangkan untuk menambah stok atau meningkatkan ketersediaan stok."
    )

    st.subheader(
        "Pertanyaan 2: Apa saja kategori produk yang paling diminati customer Brazil?"
    )
    st.write("Jawab:")
    st.write(
        "Berdasarkan data yang tersedia, kami dapat menyimpulkan 10 kategori produk teratas di sektor e-commerce di Brasil. Berikut daftarnya:"
    )

    # Visualisasi untuk kategori produk teratas
    top_10_category = (
        df["product_category_name_english"]
        .value_counts()
        .sort_values(ascending=False)[:10]
    )
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.barplot(y=top_10_category.index, x=top_10_category.values, ax=ax, dodge=False)
    plt.title("Top 10 Product Categories", fontsize=20)
    plt.xlabel("Number of Products", fontsize=14)
    plt.ylabel("Product Category", fontsize=14)
    plt.tight_layout()
    st.pyplot(fig)

    st.subheader(
        "Pertanyaan 3: Apa metode pembayaran paling favorit dan paling sedikit?"
    )
    st.write("Jawab:")
    st.write(
        "Metode pembayaran paling favorit adalah **credit_card**, dan yang paling sedikit digunakan adalah **debit_card**."
    )

    # Visualisasi untuk metode pembayaran
    payment_counts = df["payment_type"].value_counts()
    fig, ax = plt.subplots(figsize=(10, 8))
    plt.pie(
        payment_counts,
        labels=payment_counts.index,
        autopct="%1.1f%%",
        startangle=140,
        shadow=True,
    )
    plt.title("The Most Frequent Payment Type", fontsize=20)
    plt.axis("equal")
    st.pyplot(fig)

    st.write("Melihat perkembangan metode pembayaran setiap tahunnya:")
    payment_per_year = df.groupby(["Year", "payment_type"]).size().unstack(fill_value=0)
    fig, ax = plt.subplots(figsize=(10, 8))
    payment_per_year.plot(kind="bar", stacked=True, ax=ax)
    plt.title("Payment Types per Year", fontsize=20)
    plt.xlabel("Year", fontsize=14)
    plt.ylabel("Number of Payments", fontsize=14)
    plt.tight_layout()
    st.pyplot(fig)


if __name__ == "__main__":
    main()
