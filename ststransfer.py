# app.py
import streamlit as st
import pandas as pd

# Dummy data
inventory_data = pd.DataFrame({
    'SKU': ['000123456', '000123457', '000123458'],
    'Product': ['Ultraboost', 'Samba', 'Superstar'],
    'Stock Qty': [45, 67, 34],
    'Status': ['Received', 'Pending', 'In Transit']
})

# Session state for login
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# Login Screen
def login():
    st.title("Adidas Store-to-Store Transfers")
    st.subheader("Inventory Optimization for Regional Redistribution")

    email = st.text_input("Email", placeholder="example@adidas.com")
    password = st.text_input("Password", type="password")
    if st.button("Sign In"):
        if email and password:
            st.session_state.logged_in = True
        else:
            st.error("Enter valid credentials.")

# Sidebar navigation
def sidebar():
    with st.sidebar:
        st.image("https://upload.wikimedia.org/wikipedia/commons/2/20/Adidas_Logo.svg", width=120)
        st.markdown("### Proteek Tyagi\nStore A")
        return st.radio("Navigate", ["Dashboard", "Manage Inventory", "Submit Transfer", "Approvals", "Receive Inventory"])

# Dashboard Screen
def dashboard():
    st.subheader("Dashboard")
    st.write("### Inventory vs Sales Chart")
    st.metric("Current Week", "64%")
    st.metric("Inventory", "40%")
    st.metric("Last Month", "90%")
    st.write("### Inventory List")
    st.dataframe(inventory_data[['Product', 'Stock Qty']])
    st.write("### Transfer Status")
    st.write("Pending → Store B, In Transit → Store A, Completed → Store C")

# Manage Inventory
def manage_inventory():
    st.subheader("Manage Inventory")
    st.write("### Inventory Snapshot")
    st.dataframe(inventory_data)

    st.write("### Transfer Suggestions")
    st.write("- Ultraboost: 12 Units")
    st.write("- Samba: 10 Units")
    st.write("- Bounce: 8 Units")

# Transfer Request Form
def submit_transfer():
    st.subheader("Submit Transfer Request")

    sku = st.text_input("SKU", "000123456")
    available_qty = st.number_input("Available Qty", value=200)
    location_from = st.text_input("From Location", "A1")
    location_to = st.text_input("To Location", "B1")
    qty = st.slider("Transfer Quantity", 1, 50, 10)

    if st.button("Submit Transfer"):
        st.success(f"Transfer of {qty} units submitted from {location_from} to {location_to}.")

# Approvals Page
def approvals():
    st.subheader("Transfer Approvals")
    approvals_data = [
        {"Name": "John Doe", "Status": "Pending"},
        {"Name": "Alex Carry", "Status": "Pending"},
        {"Name": "Santi Lal", "Status": "Pending"},
        {"Name": "Ashwini", "Status": "Pending"}
    ]
    for person in approvals_data:
        st.markdown(f"**{person['Name']}**")
        col1, col2 = st.columns(2)
        with col1:
            if st.button(f"Approve {person['Name']}"):
                st.success(f"{person['Name']} approved")
        with col2:
            if st.button(f"Deny {person['Name']}"):
                st.error(f"{person['Name']} denied")
        st.divider()

# Receive Inventory
def receive_inventory():
    st.subheader("Receive Inventory Transfer")
    st.dataframe(inventory_data)
    if st.button("Update Status"):
        st.success("Inventory statuses updated.")

# Main Logic
if not st.session_state.logged_in:
    login()
else:
    page = sidebar()
    if page == "Dashboard":
        dashboard()
    elif page == "Manage Inventory":
        manage_inventory()
    elif page == "Submit Transfer":
        submit_transfer()
    elif page == "Approvals":
        approvals()
    elif page == "Receive Inventory":
        receive_inventory()
