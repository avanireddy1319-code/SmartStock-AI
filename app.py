import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
import hashlib

from smartstock_theme import inject_theme, hero
# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="SmartStock AI",
    page_icon="📦",
    layout="wide"
)

inject_theme()
# ==================================================
# DATABASE CONNECTION
# ==================================================

conn = sqlite3.connect(
    "smartstock.db",
    check_same_thread=False
)

cursor = conn.cursor()

# ==================================================
# USER TABLE
# ==================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age INTEGER,
    password TEXT
)
""")

# ==================================================
# INVENTORY TABLE
# ==================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS inventory(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    owner TEXT,
    product_name TEXT,
    category TEXT,
    cost_price REAL,
    selling_price REAL,
    quantity INTEGER,
    supplier TEXT
)
""")

conn.commit()

# ==================================================
# PASSWORD HASHING
# ==================================================

def hash_password(password):
    return hashlib.sha256(
        password.encode()
    ).hexdigest()

# ==================================================
# USER FUNCTIONS
# ==================================================

def register_user(name, age, password):

    hashed = hash_password(password)

    cursor.execute("""
    INSERT INTO users
    (name, age, password)
    VALUES (?, ?, ?)
    """,
    (name, age, hashed))

    conn.commit()

def login_user(name, password):

    hashed = hash_password(password)

    cursor.execute("""
    SELECT * FROM users
    WHERE name=? AND password=?
    """,
    (name, hashed))

    return cursor.fetchone()

# ==================================================
# INVENTORY FUNCTIONS
# ==================================================
def get_products():

    return pd.read_sql_query(
        """
        SELECT *
        FROM inventory
        WHERE owner = ?
        """,
        conn,
        params=(
            st.session_state.username,
        )
    )

def add_product(
    name,
    category,
    cost,
    selling,
    qty,
    supplier
):

    cursor.execute("""
    INSERT INTO inventory
    (
    owner,
    product_name,
    category,
    cost_price,
    selling_price,
    quantity,
    supplier
    )
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """,
    (
        st.session_state.username,
        name,
        category,
        cost,
        selling,
        qty,
        supplier
    ))

    conn.commit()

def update_stock(product_id, qty):

    cursor.execute("""
    UPDATE inventory
    SET quantity=?
    WHERE id=?
    """,
    (qty, product_id))

    conn.commit()

def delete_product(product_id):

    cursor.execute(
        """
        DELETE FROM inventory
        WHERE id = ?
        """,
        (product_id,)
    )

    conn.commit()
    

# ==================================================
# SESSION STATE
# ==================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""
   
# ==================================================
# LOGIN / REGISTRATION PAGE
# ==================================================

if not st.session_state.logged_in:

    st.title("🔐 SmartStock AI")

    option = st.radio(
        "Choose Option",
        ["Login", "Register"]
    )

    # --------------------------
    # REGISTER
    # --------------------------

    if option == "Register":

        st.subheader("Create Account")

        name = st.text_input(
            "Name"
        )

        age = st.number_input(
            "Age",
            min_value=10,
            max_value=100
        )

        password = st.text_input(
            "Password",
            type="password"
        )

        confirm = st.text_input(
            "Confirm Password",
            type="password"
        )

        if st.button("Register"):

            if password != confirm:
                st.error(
                    "Passwords do not match"
                )

            else:

                register_user(
                    name,
                    age,
                    password
                )

                st.success(
                    "Registration Successful"
                )

    # --------------------------
    # LOGIN
    # --------------------------

    else:

        st.subheader("Login")

        username = st.text_input(
            "Username"
        )

        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button("Login"):

            user = login_user(
                username,
                password
            )

            if user:

                st.session_state.logged_in = True
                st.session_state.username = username

                st.success(
                    "Login Successful"
                )

                st.rerun()

            else:
                st.error(
                    "Invalid Credentials"
                )

# ==================================================
# MAIN APPLICATION
# ==================================================

else:

    st.sidebar.success(
        f"Welcome {st.session_state.username}"
    )

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    page = st.sidebar.radio(
        "Navigation",
        [
            "Dashboard",
            "Manage Products",
            "Sales",
            "Analytics"
        ]
    )

    # =============================================
    # DASHBOARD
    # =============================================

    if page == "Dashboard":

        hero(
    "Inventory Dashboard",
    "Monitor stock levels and business insights",
    "📦"
)

        df = get_products()

        total_products = len(df)

        total_stock = (
            df["quantity"].sum()
            if not df.empty else 0
        )

        inventory_value = (
            (df["cost_price"] *
             df["quantity"]).sum()
            if not df.empty else 0
        )

        low_stock = (
            len(df[df["quantity"] < 10])
            if not df.empty else 0
        )

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(
            "Products",
            total_products
        )

        c2.metric(
            "Stock Units",
            total_stock
        )

        c3.metric(
            "Inventory Value",
            f"₹{inventory_value:,.2f}"
        )

        c4.metric(
            "Low Stock",
            low_stock
        )

        if not df.empty:

            search = st.text_input(
                "Search Product"
            )

            if search:
                df = df[
                    df["product_name"]
                    .str.contains(
                        search,
                        case=False
                    )
                ]

            st.dataframe(
                df,
                use_container_width=True
            )

    # =============================================
    # MANAGE PRODUCTS
    # =============================================

    elif page == "Manage Products":

        hero(
    "Manage Products",
    "Add, edit and control your inventory",
    "📦"
)

        with st.form("product_form"):

            name = st.text_input(
                "Product Name"
            )

            category = st.text_input(
                "Category"
            )

            supplier = st.text_input(
                "Supplier"
            )

            cost = st.number_input(
                "Cost Price"
            )

            selling = st.number_input(
                "Selling Price"
            )

            qty = st.number_input(
                "Quantity",
                min_value=0
            )

            submit = st.form_submit_button(
                "Add Product"
            )

            if submit:

                add_product(
                    name,
                    category,
                    cost,
                    selling,
                    qty,
                    supplier
                )

                st.success(
                    "Product Added"
                )

        df = get_products()

        if not df.empty:

            st.dataframe(df)

            product = st.selectbox(
                "Select Product",
                df["product_name"]
            )

            selected = df[
                df["product_name"] ==
                product
            ].iloc[0]

            qty_update = st.number_input(
                "Update Quantity",
                value=int(
                    selected["quantity"]
                )
            )

            col1, col2 = st.columns(2)

            with col1:
                if st.button(
                    "Update Stock"
                ):
                    update_stock(
                        selected["id"],
                        qty_update
                    )
                    st.success(
                        "Updated"
                    )
            with col2:
                if st.button(
                    "Delete Product"
                ):

                    delete_product(
                        int(selected["id"])
                    )

                    st.success(
                        f"{selected['product_name']} deleted successfully!"
                    )

                    st.rerun()
            

    # =============================================
    # SALES
    # =============================================

    elif page == "Sales":

        hero(
    "Record Sale",
    "Process transactions and update stock",
    "💰"
)

        df = get_products()

        if df.empty:
            st.warning(
                "No Products Available"
            )

        else:

            product = st.selectbox(
                "Product",
                df["product_name"]
            )

            item = df[
                df["product_name"] ==
                product
            ].iloc[0]

            sold = st.number_input(
                "Quantity Sold",
                min_value=1
            )

            if st.button(
                "Record Sale"
            ):

                if sold > item["quantity"]:

                    st.error(
                        "Not Enough Stock"
                    )

                else:

                    remaining = (
                        item["quantity"]
                        - sold
                    )

                    update_stock(
                        item["id"],
                        remaining
                    )

                    revenue = (
                        sold *
                        item[
                            "selling_price"
                        ]
                    )

                    st.success(
                        f"Revenue Generated: ${revenue:.2f}"
                    )

    # =============================================
    # ANALYTICS
    # =============================================

    elif page == "Analytics":

        hero(
    "Analytics",
    "Visualize your inventory performance",
    "📈"
)

        df = get_products()

        if not df.empty:

            fig = px.bar(
                df,
                x="product_name",
                y="quantity",
                color="category",
                title="Stock Levels"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

            pie = px.pie(
                df,
                names="category",
                values="quantity",
                title="Inventory Distribution"
            )

            st.plotly_chart(
                pie,
                use_container_width=True
            )

            csv = df.to_csv(
                index=False
            )

            st.download_button(
                "Download Report",
                csv,
                "inventory_report.csv",
                "text/csv"
            )
            
 
       