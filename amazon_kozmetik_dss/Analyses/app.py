import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px


st.set_page_config(
    page_title="Kozmetik Karar Destek Sistemi",
    page_icon="💄",
    layout="wide"
)

st.title("💄 Kozmetik Ürün Analiz ve Karar Destek Sistemi")



@st.cache_data
def load_data():
    df = pd.read_csv("kozmetik_dataset_preprocessing_end.csv")
    return df

df = load_data()



df["fiyat_performans_skoru"] = (
    df["rating"]
    * np.log1p(df["review_count"])
    * np.log1p(df["sales_last_month"])
) / df["price"]



menu = st.sidebar.radio(
    "Analiz Seçiniz",
    [
        "Genel Analizler",
        "Kategori Analizleri",
        "Marka Analizleri",
        "Kategori Bazlı Öneri Sistemi"
    ]
)

if menu == "Genel Analizler":

    st.header("📊 Genel Analizler")

    
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Toplam Ürün", len(df))
    col2.metric("Marka Sayısı", df["brand_extracted"].nunique())
    col3.metric("Kategori Sayısı", df["category"].nunique())
    col4.metric("Ortalama Puan", round(df["rating"].mean(), 2))

    st.divider()

    
    st.subheader("🏆 En Çok Satan Markalar")

    top_brand_sales = (
        df.groupby("brand_extracted")["sales_last_month"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig = px.bar(
        top_brand_sales,
        x="brand_extracted",
        y="sales_last_month",
        text_auto=True
    )

    st.plotly_chart(fig, use_container_width=True)

    
    st.subheader("⭐ En İyi Fiyat-Performans Ürünleri")

    best_products = (
        df.sort_values("fiyat_performans_skoru", ascending=False)
        .head(10)
    )

    best_display = best_products[[
        "clean_title",
        "brand_extracted",
        "price",
        "rating",
        "review_count"
    ]].copy()

    best_display.columns = [
        "Ürün Adı",
        "Marka",
        "Fiyat (TL)",
        "Puan",
        "Yorum Sayısı"
    ]

    st.dataframe(best_display, use_container_width=True)

 
    st.subheader("📊 Korelasyon Analizi")

    numeric_cols = [
        "price",
        "old_price",
        "rating",
        "review_count",
        "sales_last_month",
        "discount_rate"
    ]

    corr = df[numeric_cols].corr()

    fig = px.imshow(
        corr,
        text_auto=".2f",
        color_continuous_scale="RdBu_r"
    )

    st.plotly_chart(fig, use_container_width=True)


elif menu == "Kategori Analizleri":

    st.header("📦 Kategori Analizleri")

    secim = st.selectbox(
        "Analiz Türü",
        [
            "En Çok Satan Kategoriler",
            "En Çok İndirim Yapılan Kategoriler",
            "En Yüksek Skorlu Kategoriler",
            "Yorum Sayısı ve Skor İlişkisi"
        ]
    )

    if secim == "En Çok Satan Kategoriler":

        result = (
            df.groupby("category")["sales_last_month"]
            .sum()
            .sort_values(ascending=False)
            .head(5)
            .reset_index()
        )

        fig = px.bar(result, x="category", y="sales_last_month", text_auto=True)
        st.plotly_chart(fig, use_container_width=True)

    elif secim == "En Çok İndirim Yapılan Kategoriler":

        result = (
            df.groupby("category")["discount_rate"]
            .mean()
            .sort_values()
            .head(5)
            .reset_index()
        )

        fig = px.bar(result, x="category", y="discount_rate", text_auto=True)
        st.plotly_chart(fig, use_container_width=True)

    elif secim == "En Yüksek Skorlu Kategoriler":

        result = (
            df.groupby("category")["rating"]
            .mean()
            .sort_values(ascending=False)
            .head(5)
            .reset_index()
        )

        fig = px.bar(result, x="category", y="rating", text_auto=True)
        st.plotly_chart(fig, use_container_width=True)

    elif secim == "Yorum Sayısı ve Skor İlişkisi":

        result = (
            df.groupby("category")
            .agg(
                Ortalama_Yorum=("review_count", "mean"),
                Ortalama_Skor=("rating", "mean")
            )
            .reset_index()
        )

        fig = px.scatter(
            result,
            x="Ortalama_Yorum",
            y="Ortalama_Skor",
            hover_name="category"
        )

        st.plotly_chart(fig, use_container_width=True)


elif menu == "Marka Analizleri":

    st.header("🏷️ Marka Analizleri")

    secim = st.selectbox(
        "Analiz Türü",
        [
            "En Çok Satan Markalar",
            "En Çok İndirim Yapan Markalar",
            "En Yüksek Skorlu Markalar",
            "Yorum Sayısı ve Skor İlişkisi",
            "Marka-Kategori Tercihi"
        ]
    )

    if secim == "En Çok Satan Markalar":

        result = (
            df.groupby("brand_extracted")["sales_last_month"]
            .sum()
            .sort_values(ascending=False)
            .head(10)
            .reset_index()
        )

        fig = px.bar(result, x="brand_extracted", y="sales_last_month", text_auto=True)
        st.plotly_chart(fig, use_container_width=True)

    elif secim == "En Çok İndirim Yapan Markalar":

        result = (
            df.groupby("brand_extracted")["discount_rate"]
            .mean()
            .sort_values()
            .head(10)
            .reset_index()
        )

        fig = px.bar(result, x="brand_extracted", y="discount_rate", text_auto=True)
        st.plotly_chart(fig, use_container_width=True)

    elif secim == "En Yüksek Skorlu Markalar":

        result = (
            df.groupby("brand_extracted")["rating"]
            .mean()
            .sort_values(ascending=False)
            .head(10)
            .reset_index()
        )

        fig = px.bar(result, x="brand_extracted", y="rating", text_auto=True)
        st.plotly_chart(fig, use_container_width=True)

    elif secim == "Yorum Sayısı ve Skor İlişkisi":

        result = (
            df.groupby("brand_extracted")
            .agg(
                Ortalama_Yorum=("review_count", "mean"),
                Ortalama_Skor=("rating", "mean")
            )
            .reset_index()
        )

        fig = px.scatter(
            result,
            x="Ortalama_Yorum",
            y="Ortalama_Skor",
            hover_name="brand_extracted"
        )

        st.plotly_chart(fig, use_container_width=True)

    elif secim == "Marka-Kategori Tercihi":
    
        pivot = pd.pivot_table(
            df,
            index="brand_extracted",
            columns="category",
            values="sales_last_month",
            aggfunc="count",
            fill_value=0
        )

        pivot = pivot.astype(int)

        st.dataframe(pivot)

        st.subheader("🏆 Kategoride En Çok Satış Yapan Markalar (Top 4)")

        top4 = (
            df.groupby("brand_extracted")["sales_last_month"]
            .sum()
            .sort_values(ascending=False)
            .head(4)
            .reset_index()
        )

        top4.columns = ["Marka", "Toplam Satış"]

        st.dataframe(top4)

elif menu == "Kategori Bazlı Öneri Sistemi":

    st.header("🎯 Kategori Bazlı Öneriler")

    kategori = st.selectbox(
        "Kategori Seçiniz",
        sorted(df["category"].dropna().unique())
    )

    temp = df[df["category"] == kategori]

    st.subheader("🏆 En Çok Tercih Edilen Markalar (Top 4)")

    top4 = (
        temp["brand_extracted"]
        .value_counts()
        .head(4)
        .reset_index()
    )

    top4.columns = ["Marka", "Ürün Sayısı"]

    st.dataframe(top4)

    st.subheader("⭐ Fiyat Performans Ürünleri")

    best = (
        temp.sort_values("fiyat_performans_skoru", ascending=False)
        .head(10)
    )

    best_display = best[[
        "clean_title",
        "brand_extracted",
        "price",
        "rating",
        "discount_rate"
    ]].copy()

    best_display.columns = [
        "Ürün Adı",
        "Marka",
        "Fiyat (TL)",
        "Puan",
        "İndirim (TL)"
    ]

    st.dataframe(best_display, use_container_width=True)

    st.subheader("📉 Kategori İçindeki İndirimler")

    fig = px.bar(
        temp.sort_values("discount_rate").head(10),
        x="brand_extracted",
        y="discount_rate"
    )

    st.plotly_chart(fig, use_container_width=True)