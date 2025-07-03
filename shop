import streamlit as st
from PIL import Image
from pyzbar.pyzbar import decode
import pandas as pd
from io import BytesIO

st.title("📷 Shopkeeper Barcode Scanner")

# Initialize session state
if "data" not in st.session_state:
    st.session_state.data = []

st.header("📸 Capture Barcode or Upload Image")

# Option to choose camera or upload
input_method = st.radio("Choose input method:", ["Camera", "Upload Image"])

image = None
if input_method == "Camera":
    picture = st.camera_input("Take a picture")
    if picture:
        image = Image.open(picture)
elif input_method == "Upload Image":
    uploaded_file = st.file_uploader("Upload Barcode Image (PNG/JPG)", type=["png", "jpg", "jpeg"])
    if uploaded_file:
        image = Image.open(uploaded_file)

# Proceed only if we have an image
if image:
    st.image(image, caption="Scanned Image", use_column_width=True)

    decoded_objects = decode(image)

    if decoded_objects:
        barcode_data = decoded_objects[0].data.decode("utf-8")
        st.success(f"✅ Barcode Detected: `{barcode_data}`")

        # Simulated product details (replace with DB lookup if needed)
        product = {
            "Barcode": barcode_data,
            "Item Name": f"Item {barcode_data[-4:]}",
            "Price": float(f"1{barcode_data[-2:]}"),
            "Quantity": 1
        }

        # Form to edit details
        with st.form("edit_form"):
            product["Item Name"] = st.text_input("Item Name", value=product["Item Name"])
            product["Price"] = st.number_input("Price", value=product["Price"], format="%.2f")
            product["Quantity"] = st.number_input("Quantity", min_value=1, value=product["Quantity"], step=1)
            submitted = st.form_submit_button("Add to Excel List")

        if submitted:
            st.session_state.data.append(product)
            st.success("📦 Item added to Excel list")
    else:
        st.warning("❌ No barcode found in image")

# Show scanned items
if st.session_state.data:
    df = pd.DataFrame(st.session_state.data)
    st.subheader("🧾 Scanned Items")
    st.dataframe(df)

    # Excel download
    def to_excel(data):
        output = BytesIO()
        pd.DataFrame(data).to_excel(output, index=False, engine='openpyxl')
        output.seek(0)
        return output

    st.download_button(
        label="📥 Download Excel File",
        data=to_excel(st.session_state.data),
        file_name="scanned_items.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
