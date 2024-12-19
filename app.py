import streamlit as st
import pandas as pd
from scrap import Scrap

st.set_page_config(page_title="📱 Tech Price Comparison", page_icon="💻", layout="wide")

def display_data(header, data):
    st.subheader(header)
    if data:
        st.table(pd.DataFrame(data))
    else:
        st.write("🚫 No Product Found")

scrap = Scrap()
startech, techland, ryans, globalbrand = [], [], [], []

st.title("🔍 Compare Prices of Tech Products in Bangladesh")
st.write("💡 Enter a product name to compare prices across popular Bangladeshi tech stores.")
query = st.text_input("🛒 Product Name")

if st.button("Search 🔎"):
    if query:
        startech = scrap.startech(query) or []
        techland = scrap.techland(query) or []
        ryans = scrap.ryans_(query) or []
        globalbrand = scrap.globalbrand(query) or []
        
        display_data("⭐ Star Tech", startech)
        display_data("💼 Tech Land", techland)
        display_data("🏢 Ryans", ryans)
        display_data("🌐 Global Brand", globalbrand)
    else:
        st.write("⚠️ Please enter a product name to search.")

product_prices = {}
for source, data in zip(
    ["Star Tech", "Tech Land", "Ryans", "Global Brand"],
    [startech, techland, ryans, globalbrand],
):
    for item in data:
        name = item["name"]
        price = item["price"]
        if name not in product_prices:
            product_prices[name] = {"Star Tech": 0, "Tech Land": 0, "Ryans": 0, "Global Brand": 0}
        product_prices[name][source] = price

st.write("📊 **Price Comparison Chart**")
df = pd.DataFrame.from_dict(product_prices, orient="index")
if not df.empty:
    st.bar_chart(df.fillna(0))
else:
    st.write("📭 No data available for chart")

# Add footer
st.markdown("<footer style='text-align: center;'>Made With ❤️ by Minhajul Islam</footer>", unsafe_allow_html=True)
