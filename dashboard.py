import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv("SALARY_bersih.csv")

# Sidebar untuk navigasi
app_mode = st.sidebar.selectbox("Select Page", ["Home", "About", "Gaji UMP", "Top 10 Provinsi"])

if app_mode == "Home":
    st.title("Home")
    st.image("jakarta.jpg", use_container_width=True)
    st.write("""
    Selamat datang di web Analisis Gaji UMP di Indonesia.
    Situs ini dirancang untuk menyediakan informasi dan analisis mendalam mengenai Upah Minimum Provinsi (UMP) di Indonesia, mencakup berbagai provinsi dan tren perubahannya dari tahun ke tahun. 
    Dengan memanfaatkan teknologi analisis data terkini, kami berusaha memberikan gambaran yang jelas dan akurat tentang situasi upah di Indonesia. 
    Melalui platform ini, kami berharap dapat mendukung upaya peningkatan kesejahteraan pekerja dan kebijakan publik yang lebih baik berdasarkan data yang valid dan terpercaya.
    Terima kasih telah mengunjungi web Analisis Gaji UMP di Indonesia.
    Kami berharap situs ini dapat menjadi sumber informasi yang berharga dan alat yang efektif dalam upaya meningkatkan kualitas hidup masyarakat Indonesia.
    """)

elif app_mode == "About":
    st.title("About")
    st.write("""
    Aplikasi ini dibuat untuk menganalisis data Gaji UMP di Indonesia pada tahun 1997-2025 berdasarkan berbagai provinsi.
    Dengan menggunakan web ini, pengguna dapat memperoleh wawasan mendalam mengenai perkembangan Gaji UMP yang paling signifikan dan distribusinya di berbagai wilayah di Indonesia.
    Web ini dirancang untuk memudahkan analisis data melalui visualisasi data interaktif dan kemampuan untuk menyaring data berdasarkan kategori tahun dan provinsi.
    Selain itu, web ini juga membantu mengidentifikasi tren dan pola dalam perubahan Gaji UMP, sehingga dapat mendukung pengambilan keputusan yang lebih baik dalam upaya meningkatkan kesejahteraan pekerja.
    Dengan demikian, aplikasi ini berperan penting dalam membantu memahami dan menangani isu-isu ekonomi terkait upah yang mempengaruhi masyarakat Indonesia.

    """)

elif app_mode == "Gaji UMP":
    # Sidebar - Province selection
    provinces = df['PROVINCE'].unique()
    selected_province = st.sidebar.selectbox("Pilih Provinsi", sorted(provinces))

    # Filter data by province
    province_data = df[df['PROVINCE'] == selected_province].sort_values('YEAR')

    # Sidebar - Time range selection (5, 10, Full)
    time_range = st.sidebar.selectbox("Pilih Rentang Waktu", [5, 10, 'Seluruh'])

    # Filter data based on selected time range
    if time_range == 'Seluruh':
        filtered_data = province_data
    else:
        max_year = province_data['YEAR'].max()
        min_year = max_year - time_range
        filtered_data = province_data[province_data['YEAR'] >= min_year]

    # Sidebar - Chart type selection
    chart_type = st.sidebar.radio("Pilih Jenis Diagram", ["Diagram Garis", "Diagram Batang"])

    # Plotting
    st.title("Visualisasi UMP di Indonesia")
    st.subheader(f"Provinsi: {selected_province}")

    fig, ax = plt.subplots(figsize=(10, 6))
    if chart_type == "Diagram Garis":
        ax.plot(filtered_data['YEAR'], filtered_data['SALARY'], marker='o', linestyle='-')
    else:  # Diagram Batang
        ax.bar(filtered_data['YEAR'], filtered_data['SALARY'])

    ax.set_xlabel("Tahun")
    ax.set_ylabel("UMP")
    ax.set_title(f"UMP - {selected_province} ({time_range} Tahun Terakhir)" if time_range != 'Seluruh' else f"UMP - {selected_province} (Full Data)")
    st.pyplot(fig)

    if st.checkbox("Tampilkan data aktual"):
        st.write(filtered_data.reset_index(drop=True))

elif app_mode == "Top 10 Provinsi":
    # Sidebar - Year selection (similar to province)
    available_years = sorted(df['YEAR'].unique())
    selected_year = st.sidebar.selectbox("Pilih Tahun", available_years)

    # Filter data for the selected year
    year_data = df[df['YEAR'] == selected_year]

    # Get top 10 provinces with the highest UMP for the selected year
    top_10 = year_data.sort_values(by='SALARY', ascending=False).head(10)

    # Visualization for top 10 provinces by UMP in the selected year
    st.title(f"10 Provinsi dengan UMP Tertinggi Tahun {selected_year}")
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    ax2.barh(top_10['PROVINCE'], top_10['SALARY'], color='skyblue')
    ax2.invert_yaxis()  # Largest values at the top
    ax2.set_xlabel("UMP")
    ax2.set_title(f"10 Provinsi dengan UMP Tertinggi Tahun {selected_year}")
    st.pyplot(fig2)

    if st.checkbox("Tampilkan data 10 UMP tertinggi"):
        st.write(top_10[['PROVINCE', 'SALARY']].reset_index(drop=True))