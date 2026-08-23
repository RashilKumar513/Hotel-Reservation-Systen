import streamlit as st
import pandas as pd
from datetime import datetime
import random

import database as db
import pdf_generator as pdf_gen

# ============================================================
# RESTAURANT & HOTEL MANAGEMENT SYSTEM - 5 STAR EDITION
# ============================================================

st.set_page_config(
    page_title="5 Star Restaurant | Management & Billing POS",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Initialize SQLite database
db.init_db()

# ----------------------------- CONSTANTS & EMOJIS --------------------------

CATEGORY_ICONS = {
    "All": "🍽️",
    "Starters": "🥗",
    "Main Course": "🍛",
    "Snacks": "🍜",
    "Beverages": "🥤",
    "Desserts": "🍨"
}

EMOJIS = {
    "Samosa": "🥟", "Paneer Tikka": "🍢", "Chicken Tikka": "🍗",
    "Vegetable Pakora": "🥦", "Papdi Chaat": "🥗", "Tomato Soup": "🍅",
    "Masala Papad": "🫓", "Butter Chicken": "🍛", "Pasta": "🍝",
    "Basmati Rice": "🍚", "Paneer Masala": "🧀", "Palak Paneer": "🥬",
    "Dal Makhani": "🍲", "Chole Bhature": "🫓", "Noodles": "🍜",
    "Aloo Tikki Chaat": "🥔", "Dahi Vada": "🥣", "Pav Bhaji": "🍞",
    "Bhel Puri": "🥗", "Spring Roll": "🥖", "Fresh Lime Soda": "🥤",
    "Cold Coffee": "🧋", "Mango Juice": "🥭", "Masala Tea": "☕",
    "Mineral Water": "🍼", "Gulab Jamun": "🍡", "Ice Cream": "🍨",
    "Sizzling Brownie": "🍰", "Fruit Salad": "🍉"
}

def get_item_emoji(item_name):
    return EMOJIS.get(item_name, "🍽️")

# ----------------------------- CUSTOM CSS STYLING --------------------------

st.markdown("""
<style>
    /* ================= GLOBAL LIGHT CANVAS ================= */
    .stApp, [data-testid="stAppViewContainer"], .main {
        background: linear-gradient(135deg, #faf7ff 0%, #f3e8ff 100%) !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Main Content Area Typography (High Contrast Dark Text) */
    [data-testid="stMain"] *, 
    [data-testid="stMain"] p, 
    [data-testid="stMain"] span, 
    [data-testid="stMain"] label, 
    [data-testid="stMain"] li, 
    [data-testid="stMain"] ul, 
    [data-testid="stMain"] ol,
    [data-testid="stMain"] h1, 
    [data-testid="stMain"] h2, 
    [data-testid="stMain"] h3, 
    [data-testid="stMain"] h4, 
    [data-testid="stMain"] h5, 
    [data-testid="stMain"] h6,
    div[data-testid="stMarkdownContainer"] * {
        color: #1e1b4b;
    }

    /* Header Banner Text Overrides */
    .main-header {
        background: linear-gradient(135deg, #4c1d95 0%, #6d28d9 100%);
        padding: 24px 30px;
        border-radius: 20px;
        box-shadow: 0 10px 25px -5px rgba(76, 29, 149, 0.25);
        margin-bottom: 24px;
    }
    .main-header *, .main-title {
        color: #ffffff !important;
    }
    .subtitle {
        color: #ddd6fe !important;
        font-size: 0.95rem;
        margin-top: 4px;
        margin-bottom: 0;
    }
    .main-title {
        font-size: 2.2rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: -0.5px;
    }
    
    /* Card Styles */
    .food-card {
        background: #ffffff !important;
        border-radius: 16px;
        padding: 16px;
        border: 1px solid #f3e8ff;
        box-shadow: 0 4px 14px rgba(76, 29, 149, 0.05);
        transition: all 0.2s ease-in-out;
        margin-bottom: 12px;
    }
    .food-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(76, 29, 149, 0.12);
        border-color: #c4b5fd;
    }
    .food-name {
        font-weight: 700;
        font-size: 1.05rem;
        color: #1e1b4b !important;
    }
    .food-price {
        color: #6d28d9 !important;
        font-weight: 800;
        font-size: 1.1rem;
    }
    .stock-badge {
        font-size: 0.75rem;
        padding: 2px 8px;
        border-radius: 12px;
        font-weight: 600;
        display: inline-block;
    }
    .stock-ok { background: #dcfce7 !important; color: #166534 !important; }
    .stock-low { background: #fef3c7 !important; color: #92400e !important; }
    .stock-out { background: #fee2e2 !important; color: #991b1b !important; }
    
    /* Bill Summary Banner */
    .bill-total-card {
        background: linear-gradient(135deg, #4c1d95 0%, #7e22ce 100%);
        padding: 20px;
        border-radius: 18px;
        text-align: center;
        box-shadow: 0 8px 20px rgba(76, 29, 149, 0.2);
        margin: 16px 0;
    }
    .bill-total-card *, .bill-total-card p, .bill-total-card small {
        color: #ffffff !important;
    }
    .bill-total-amount {
        font-size: 2.2rem;
        font-weight: 900;
        color: #fef08a !important;
        margin: 0;
    }
    
    /* Table Card */
    .table-box {
        background: #ffffff !important;
        border-radius: 16px;
        padding: 20px;
        text-align: center;
        border: 2px solid #e5e7eb;
        box-shadow: 0 4px 12px rgba(0,0,0,0.03);
    }
    .table-box h3, .table-box p {
        color: #1f2937 !important;
    }
    .table-avail { border-color: #22c55e !important; background: #f0fdf4 !important; }
    .table-occ { border-color: #ef4444 !important; background: #fef2f2 !important; }
    .table-res { border-color: #f59e0b !important; background: #fffbeb !important; }

    /* Custom Metric Cards */
    div[data-testid="stMetric"] {
        background: #ffffff !important;
        border-radius: 16px;
        padding: 16px;
        border: 1px solid #f3e8ff;
        box-shadow: 0 4px 12px rgba(0,0,0,0.04);
    }
    [data-testid="stMetricValue"] * {
        color: #4c1d95 !important;
        font-weight: 800 !important;
    }
    [data-testid="stMetricLabel"] * {
        color: #4b5563 !important;
        font-weight: 600 !important;
    }

    /* Expander & Tabs */
    [data-testid="stExpander"] summary *,
    button[data-baseweb="tab"] * {
        color: #1e1b4b !important;
        font-weight: 700 !important;
    }

    /* Inputs, Dataframes & Selectboxes in Main Area */
    [data-testid="stMain"] .stTextInput input, 
    [data-testid="stMain"] .stNumberInput input, 
    [data-testid="stMain"] .stSelectbox select, 
    [data-testid="stMain"] div[data-baseweb="select"] * {
        color: #1e1b4b !important;
        background-color: #ffffff !important;
    }
    [data-testid="stTable"] *, [data-testid="stDataFrame"] * {
        color: #1e1b4b !important;
    }

    /* ================= SIDEBAR LUXURY STYLING ================= */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #2e1065 0%, #3b0764 100%) !important;
        border-right: 1px solid #581c87;
    }

    /* Sidebar Text, Headers, Radio Buttons, Captions */
    [data-testid="stSidebar"] *, 
    [data-testid="stSidebar"] p, 
    [data-testid="stSidebar"] span, 
    [data-testid="stSidebar"] label, 
    [data-testid="stSidebar"] div,
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] div[role="radiogroup"] * {
        color: #f3e8ff !important;
    }

    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3, 
    [data-testid="stSidebar"] strong {
        color: #ffffff !important;
        font-weight: 800 !important;
    }

    [data-testid="stSidebar"] .stCaption, 
    [data-testid="stSidebar"] small {
        color: #c4b5fd !important;
    }

    /* Sidebar Radio item hover and active state */
    [data-testid="stSidebar"] div[role="radiogroup"] label {
        padding: 8px 12px !important;
        border-radius: 10px !important;
        transition: background 0.2s ease !important;
    }
    [data-testid="stSidebar"] div[role="radiogroup"] label:hover {
        background: rgba(255, 255, 255, 0.1) !important;
    }

    /* Sidebar Number input & controls */
    [data-testid="stSidebar"] input {
        background-color: #4c1d95 !important;
        color: #ffffff !important;
        border: 1px solid #7e22ce !important;
        border-radius: 8px !important;
    }
    [data-testid="stSidebar"] button {
        background-color: #581c87 !important;
        color: #ffffff !important;
        border-color: #7e22ce !important;
    }
</style>
""", unsafe_allow_html=True)

# ----------------------------- STATE MANAGEMENT --------------------------

def new_bill_number():
    return f"INV-{datetime.now():%Y%m%d}-{random.randint(1000, 9999)}"

if "cart" not in st.session_state:
    st.session_state.cart = {}
if "bill_no" not in st.session_state:
    st.session_state.bill_no = new_bill_number()
if "last_pdf" not in st.session_state:
    st.session_state.last_pdf = None
if "selected_table" not in st.session_state:
    st.session_state.selected_table = ""
if "table_status" not in st.session_state:
    st.session_state.table_status = {f"T-{i}": "Available" for i in range(1, 13)}
    st.session_state.table_status["T-2"] = "Occupied"
    st.session_state.table_status["T-5"] = "Reserved"

# Helper functions for cart
def add_to_cart(item, qty=1):
    st.session_state.cart[item] = st.session_state.cart.get(item, 0) + qty

def remove_from_cart(item):
    st.session_state.cart.pop(item, None)

def update_cart_qty(item, qty):
    if qty <= 0:
        st.session_state.cart.pop(item, None)
    else:
        st.session_state.cart[item] = qty

def clear_cart():
    st.session_state.cart = {}
    st.session_state.bill_no = new_bill_number()
    st.session_state.last_pdf = None

# Calculate bill amounts
def calculate_bill_amounts(menu_df, discount_pct=0.0, tax_pct=18.0):
    rows = []
    subtotal = 0.0
    menu_map = menu_df.set_index("item").to_dict(orient="index")
    
    for item, qty in st.session_state.cart.items():
        if item in menu_map and qty > 0:
            price = menu_map[item]["price"]
            category = menu_map[item]["category"]
            amount = qty * price
            subtotal += amount
            rows.append({
                "Category": category,
                "Item": item,
                "Qty": qty,
                "Unit Price": price,
                "Amount": amount
            })

    discount = subtotal * (discount_pct / 100.0)
    taxable = max(subtotal - discount, 0.0)
    tax = taxable * (tax_pct / 100.0)
    grand_total = taxable + tax
    return rows, subtotal, discount, tax, grand_total

# ----------------------------- SIDEBAR ------------------------

with st.sidebar:
    st.markdown("## 🍽️ 5 STAR POS")
    st.caption("Restaurant & Hotel Management System")
    st.divider()

    page = st.radio(
        "Navigation",
        [
            "🧾 New Bill",
            "🪑 Table View",
            "🍴 Menu Manager",
            "👥 Customers",
            "📊 Analytics",
            "📜 Bill History",
            "ℹ️ About"
        ],
    )

    st.divider()
    st.markdown("### ⚙️ Tax Settings")
    tax_pct = st.number_input(
        "GST / Tax Rate (%)",
        min_value=0.0,
        max_value=50.0,
        value=18.0,
        step=1.0,
        help="CGST (9%) + SGST (9%) default = 18%. Adjustable for special rates.",
    )

    st.caption("Powered by SQLite Persistence & ReportLab PDF Generator.")

# Fetch active menu items from DB
all_menu_df = db.get_all_menu(active_only=False)
active_menu_df = all_menu_df[all_menu_df["active"] == 1] if not all_menu_df.empty else pd.DataFrame()

# ==============================================================================
# PAGE 1: NEW BILL (POS BILLING)
# ==============================================================================

if page == "🧾 New Bill":
    st.markdown("""
    <div class="main-header">
        <h1 class="main-title">🍽️ Point of Sale (POS)</h1>
        <p class="subtitle">Quick menu ordering, customer management & instant invoice generation</p>
    </div>
    """, unsafe_allow_html=True)

    col_left, col_right = st.columns([1.6, 1.2])

    with col_left:
        # Customer Details Expander
        with st.expander("👤 Customer & Order Information", expanded=True):
            c1, c2 = st.columns(2)
            phone_input = c1.text_input("Contact Phone Number", placeholder="10-digit mobile number", key="cust_phone")
            
            # Lookup customer if phone entered
            existing_cust = None
            if phone_input and len(phone_input.strip()) >= 3:
                existing_cust = db.find_customer_by_phone(phone_input.strip())
            
            default_cust_name = existing_cust["name"] if existing_cust else ""
            customer_name = c2.text_input("Customer Name", value=default_cust_name, placeholder="Enter full name", key="cust_name")

            if existing_cust:
                st.info(f"⭐ Returning Customer: **{existing_cust['name']}** | Visits: {existing_cust['visits']} | Total Spent: ₹{existing_cust['total_spent']:,.2f}")

            c3, c4 = st.columns(2)
            order_type = c3.selectbox("Order Type", ["Dine In", "Takeaway", "Delivery"])
            
            default_table = st.session_state.selected_table if st.session_state.selected_table else "T-1"
            table_no = c4.text_input("Table / Order No.", value=default_table if order_type == "Dine In" else "-")

        # Menu Section
        st.markdown("### 🍴 Menu Catalog")
        
        m_search, m_cat = st.columns([2, 1])
        search_query = m_search.text_input("🔎 Search Dishes...", placeholder="Search Samosa, Pasta, Coffee...")
        
        categories = ["All"] + sorted(list(active_menu_df["category"].unique())) if not active_menu_df.empty else ["All"]
        selected_category = m_cat.selectbox(
            "Category Filter",
            categories,
            format_func=lambda x: f"{CATEGORY_ICONS.get(x, '🍽️')} {x}"
        )

        filtered_df = active_menu_df.copy()
        if selected_category != "All":
            filtered_df = filtered_df[filtered_df["category"] == selected_category]
        if search_query.strip():
            filtered_df = filtered_df[filtered_df["item"].str.contains(search_query.strip(), case=False, na=False)]

        if filtered_df.empty:
            st.warning("No items found matching your criteria.")
        else:
            # Display dishes in a 2-column grid
            food_cols = st.columns(2)
            for idx, row in filtered_df.reset_index(drop=True).iterrows():
                item = row["item"]
                price = row["price"]
                stock = row["stock"]
                category = row["category"]
                
                stock_class = "stock-ok" if stock > 10 else ("stock-low" if stock > 0 else "stock-out")
                stock_text = f"Stock: {stock}" if stock > 0 else "Out of Stock"

                with food_cols[idx % 2]:
                    st.markdown(f"""
                    <div class="food-card">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <div class="food-name">{get_item_emoji(item)} {item}</div>
                            <span class="stock-badge {stock_class}">{stock_text}</span>
                        </div>
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-top:8px;">
                            <div class="food-price">₹{price:,.2f}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    btn_c1, btn_c2 = st.columns([1, 1])
                    current_qty_in_cart = st.session_state.cart.get(item, 0)
                    
                    if btn_c1.button("➕ Add", key=f"add_btn_{item}", disabled=(stock <= 0), use_container_width=True):
                        add_to_cart(item, 1)
                        st.rerun()
                        
                    if current_qty_in_cart > 0:
                        btn_c2.markdown(f"<div style='text-align:center; padding-top:4px;'><b>In Cart: {current_qty_in_cart}</b></div>", unsafe_allow_html=True)

    with col_right:
        st.markdown("### 🛒 Order Cart")

        cart_rows, subtotal, discount_default, tax_amount, grand_total = calculate_bill_amounts(active_menu_df, 0.0, tax_pct)

        if not cart_rows:
            st.info("🛒 Your cart is currently empty. Click **➕ Add** on menu items to begin.")
        else:
            # Cart Item List
            for r in cart_rows:
                item_name = r["Item"]
                item_qty = r["Qty"]
                item_price = r["Unit Price"]
                item_amount = r["Amount"]

                ic1, ic2, ic3, ic4 = st.columns([2.5, 1.2, 1.2, 0.8])
                ic1.markdown(f"**{get_item_emoji(item_name)} {item_name}**<br/><small style='color:#6b7280;'>₹{item_price:,.2f} each</small>", unsafe_allow_html=True)
                
                new_q = ic2.number_input("qty", min_value=1, max_value=99, value=item_qty, key=f"cart_qty_{item_name}", label_visibility="collapsed")
                if new_q != item_qty:
                    update_cart_qty(item_name, new_q)
                    st.rerun()

                ic3.markdown(f"<div style='text-align:right; font-weight:700; padding-top:6px;'>₹{item_amount:,.2f}</div>", unsafe_allow_html=True)
                
                if ic4.button("❌", key=f"del_{item_name}"):
                    remove_from_cart(item_name)
                    st.rerun()

            st.divider()

            # Bill options
            disc_col, pay_col = st.columns(2)
            discount_pct = disc_col.number_input("Discount (%)", min_value=0.0, max_value=100.0, value=0.0, step=1.0)
            payment_method = pay_col.selectbox("Payment Method", ["UPI", "Cash", "Card", "Net Banking"])

            order_notes = st.text_input("Order Notes (Optional)", placeholder="Less spicy, extra cutlery, etc.")

            # Recalculate with discount & tax
            cart_rows, subtotal, discount_amount, tax_amount, grand_total = calculate_bill_amounts(
                active_menu_df, discount_pct, tax_pct
            )

            # Bill Summary Banner
            st.markdown(f"""
            <div class="bill-total-card">
                <p style="margin:0; font-size:0.9rem; text-transform:uppercase; letter-spacing:1px;">Bill #{st.session_state.bill_no}</p>
                <h2 class="bill-total-amount">₹{grand_total:,.2f}</h2>
                <small style="color:#e9d5ff;">Subtotal: ₹{subtotal:,.2f} | Discount: ₹{discount_amount:,.2f} | GST ({tax_pct:.0f}%): ₹{tax_amount:,.2f}</small>
            </div>
            """, unsafe_allow_html=True)

            action_c1, action_c2 = st.columns(2)

            if action_c1.button("⚡ Complete & Save Bill", type="primary", use_container_width=True):
                cust_final = customer_name.strip() if customer_name.strip() else "Guest Customer"
                phone_final = phone_input.strip() if phone_input.strip() else ""

                if phone_final and (not phone_final.isdigit() or len(phone_final) != 10):
                    st.error("⚠️ Please enter a valid 10-digit mobile number or leave blank.")
                else:
                    success, msg = db.save_bill(
                        bill_no=st.session_state.bill_no,
                        customer=cust_final,
                        phone=phone_final,
                        order_type=order_type,
                        table_no=table_no,
                        payment=payment_method,
                        subtotal=subtotal,
                        discount=discount_amount,
                        tax=tax_amount,
                        total=grand_total,
                        notes=order_notes,
                        items=cart_rows
                    )

                    if success:
                        # Update visual table status if dine-in
                        if order_type == "Dine In" and table_no in st.session_state.table_status:
                            st.session_state.table_status[table_no] = "Occupied"

                        # Generate PDF Invoice
                        pdf_bytes = pdf_gen.generate_pdf_invoice(
                            bill_no=st.session_state.bill_no,
                            customer=cust_final,
                            phone=phone_final,
                            order_type=order_type,
                            table_no=table_no,
                            payment=payment_method,
                            notes=order_notes,
                            rows=cart_rows,
                            subtotal=subtotal,
                            discount=discount_amount,
                            tax_pct=tax_pct,
                            tax_amount=tax_amount,
                            grand_total=grand_total
                        )
                        st.session_state.last_pdf = pdf_bytes
                        st.success(f"🎉 {msg}")
                        st.balloons()
                    else:
                        st.error(f"❌ {msg}")

            if action_c2.button("🔄 New Order", use_container_width=True):
                clear_cart()
                st.rerun()

            if st.session_state.last_pdf:
                st.download_button(
                    label="📥 Download Official PDF Receipt",
                    data=st.session_state.last_pdf,
                    file_name=f"{st.session_state.bill_no}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )

# ==============================================================================
# PAGE 2: TABLE VIEW
# ==============================================================================

elif page == "🪑 Table View":
    st.markdown("""
    <div class="main-header">
        <h1 class="main-title">🪑 Table Management</h1>
        <p class="subtitle">Live interactive restaurant floor plan & table reservation status</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Floor Plan Summary")
    t_status = st.session_state.table_status
    avail_count = sum(1 for s in t_status.values() if s == "Available")
    occ_count = sum(1 for s in t_status.values() if s == "Occupied")
    res_count = sum(1 for s in t_status.values() if s == "Reserved")

    tm1, tm2, tm3 = st.columns(3)
    tm1.metric("🟩 Available Tables", avail_count)
    tm2.metric("🟥 Occupied Tables", occ_count)
    tm3.metric("🟨 Reserved Tables", res_count)

    st.divider()
    st.markdown("### Interactive Floor Grid")

    table_keys = list(t_status.keys())
    grid_cols = st.columns(4)

    for i, t_name in enumerate(table_keys):
        status = t_status[t_name]
        css_class = "table-avail" if status == "Available" else ("table-occ" if status == "Occupied" else "table-res")
        badge_icon = "🟩" if status == "Available" else ("🟥" if status == "Occupied" else "🟨")

        with grid_cols[i % 4]:
            st.markdown(f"""
            <div class="table-box {css_class}">
                <h3 style="margin:0; color:#1f2937;">{t_name}</h3>
                <p style="margin:4px 0 12px 0; font-weight:700;">{badge_icon} {status}</p>
            </div>
            """, unsafe_allow_html=True)

            sc1, sc2 = st.columns(2)
            if sc1.button("Select", key=f"sel_tbl_{t_name}", use_container_width=True):
                st.session_state.selected_table = t_name
                st.toast(f"Selected {t_name} for Billing", icon="✅")
                
            new_status = sc2.selectbox("Status", ["Available", "Occupied", "Reserved"], index=["Available", "Occupied", "Reserved"].index(status), key=f"st_select_{t_name}", label_visibility="collapsed")
            if new_status != status:
                st.session_state.table_status[t_name] = new_status
                st.rerun()

# ==============================================================================
# PAGE 3: MENU MANAGER
# ==============================================================================

elif page == "🍴 Menu Manager":
    st.markdown("""
    <div class="main-header">
        <h1 class="main-title">🍴 Dynamic Menu Manager</h1>
        <p class="subtitle">Add, edit, enable/disable dishes and manage menu inventory in real-time</p>
    </div>
    """, unsafe_allow_html=True)

    tab_view, tab_add, tab_edit = st.tabs(["📋 View All Dishes", "➕ Add New Dish", "✏️ Edit / Delete Dish"])

    with tab_view:
        st.markdown("### Current Active Menu")
        st.dataframe(
            all_menu_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "price": st.column_config.NumberColumn("Price (₹)", format="₹%.2f"),
                "active": st.column_config.CheckboxColumn("Active State"),
            }
        )

    with tab_add:
        st.markdown("### Add New Item to Restaurant Database")
        with st.form("add_item_form"):
            ac1, ac2 = st.columns(2)
            new_cat = ac1.selectbox("Category", ["Starters", "Main Course", "Snacks", "Beverages", "Desserts"])
            new_name = ac2.text_input("Dish / Item Name", placeholder="e.g. Masala Dosa")
            
            ac3, ac4, ac5 = st.columns(3)
            new_price = ac3.number_input("Price (₹)", min_value=1.0, value=150.0, step=5.0)
            new_stock = ac4.number_input("Initial Stock Qty", min_value=0, value=50, step=5)
            is_active = ac5.selectbox("Status", [1, 0], format_func=lambda x: "Active" if x == 1 else "Inactive")

            submit_add = st.form_submit_button("➕ Save New Dish", type="primary", use_container_width=True)

            if submit_add:
                if not new_name.strip():
                    st.error("Please enter a valid item name.")
                else:
                    success, msg = db.add_menu_item(new_cat, new_name.strip(), new_price, new_stock, is_active)
                    if success:
                        st.success(f"🎉 {msg}")
                        st.rerun()
                    else:
                        st.error(f"❌ {msg}")

    with tab_edit:
        st.markdown("### Modify Existing Menu Dish")
        if all_menu_df.empty:
            st.info("No items in database.")
        else:
            selected_item_name = st.selectbox("Select Item to Edit", all_menu_df["item"].tolist())
            item_row = all_menu_df[all_menu_df["item"] == selected_item_name].iloc[0]

            with st.form("edit_item_form"):
                ec1, ec2 = st.columns(2)
                edit_cat = ec1.selectbox("Category", ["Starters", "Main Course", "Snacks", "Beverages", "Desserts"], index=["Starters", "Main Course", "Snacks", "Beverages", "Desserts"].index(item_row["category"]))
                edit_name = ec2.text_input("Item Name", value=item_row["item"])

                ec3, ec4, ec5 = st.columns(3)
                edit_price = ec3.number_input("Price (₹)", min_value=1.0, value=float(item_row["price"]), step=5.0)
                edit_stock = ec4.number_input("Stock Qty", min_value=0, value=int(item_row["stock"]), step=5)
                edit_active = ec5.selectbox("Status", [1, 0], index=0 if item_row["active"] == 1 else 1, format_func=lambda x: "Active" if x == 1 else "Inactive")

                btn_e1, btn_e2 = st.columns(2)
                submit_update = btn_e1.form_submit_button("💾 Save Changes", type="primary", use_container_width=True)
                submit_delete = btn_e2.form_submit_button("🗑️ Delete Dish", use_container_width=True)

                if submit_update:
                    success, msg = db.update_menu_item(int(item_row["id"]), edit_cat, edit_name.strip(), edit_price, edit_stock, edit_active)
                    if success:
                        st.success(f"🎉 {msg}")
                        st.rerun()
                    else:
                        st.error(f"❌ {msg}")

                if submit_delete:
                    success, msg = db.delete_menu_item(int(item_row["id"]))
                    if success:
                        st.success(f"🗑️ {msg}")
                        st.rerun()
                    else:
                        st.error(f"❌ {msg}")

# ==============================================================================
# PAGE 4: CUSTOMERS (CRM)
# ==============================================================================

elif page == "👥 Customers":
    st.markdown("""
    <div class="main-header">
        <h1 class="main-title">👥 Customer CRM Directory</h1>
        <p class="subtitle">Track customer history, visit counts, total lifetime spend & loyalty status</p>
    </div>
    """, unsafe_allow_html=True)

    cust_df = db.get_customers()

    if cust_df.empty:
        st.info("No customer records found yet. Complete orders with contact phone numbers to build CRM records.")
    else:
        # Search CRM
        c_search = st.text_input("🔎 Search Customer by Name or Phone...", placeholder="Search phone or name...")
        filtered_cust = cust_df.copy()
        if c_search.strip():
            filtered_cust = filtered_cust[
                filtered_cust["name"].str.contains(c_search.strip(), case=False, na=False) |
                filtered_cust["phone"].str.contains(c_search.strip(), case=False, na=False)
            ]

        # Tier calculation
        def get_tier(spent):
            if spent >= 2000:
                return "👑 VIP Platinum"
            elif spent >= 1000:
                return "🥇 Gold Member"
            else:
                return "🥈 Silver Guest"

        filtered_cust["Loyalty Tier"] = filtered_cust["total_spent"].apply(get_tier)

        st.dataframe(
            filtered_cust,
            use_container_width=True,
            hide_index=True,
            column_config={
                "total_spent": st.column_config.NumberColumn("Total Spent (₹)", format="₹%.2f"),
                "visits": st.column_config.NumberColumn("Total Visits"),
            }
        )

# ==============================================================================
# PAGE 5: ANALYTICS DASHBOARD
# ==============================================================================

elif page == "📊 Analytics":
    st.markdown("""
    <div class="main-header">
        <h1 class="main-title">📊 Executive Sales Dashboard</h1>
        <p class="subtitle">Real-time revenue metrics, top dishes analytics & payment distribution</p>
    </div>
    """, unsafe_allow_html=True)

    summary = db.get_analytics_summary()

    if summary["total_bills"] == 0:
        st.info("No bills generated yet. Complete orders on the POS screen to populate live analytics.")
    else:
        # Top Metrics
        a, b, c, d = st.columns(4)
        a.metric("💰 Total Revenue", f"₹{summary['total_sales']:,.2f}")
        b.metric("🧾 Total Bills", summary["total_bills"])
        c.metric("📈 Avg Order Value", f"₹{summary['avg_bill']:,.2f}")
        d.metric("🍽️ Dishes Sold", int(summary["items_sold"]))

        st.divider()

        # Charts Section
        ch_left, ch_right = st.columns(2)

        with ch_left:
            st.subheader("💳 Payment Methods Split")
            st.bar_chart(summary["payment_counts"])

        with ch_right:
            st.subheader("📦 Order Types Breakdown")
            st.bar_chart(summary["order_type_counts"])

        st.divider()

        ch_left2, ch_right2 = st.columns(2)
        with ch_left2:
            st.subheader("🔥 Top 5 Best-Selling Dishes")
            if not summary["top_items"].empty:
                st.dataframe(summary["top_items"], use_container_width=True, hide_index=True)
            else:
                st.info("No item details available.")

        with ch_right2:
            st.subheader("📈 Revenue per Bill")
            bills_df = summary["bills_df"]
            if not bills_df.empty:
                st.line_chart(bills_df.set_index("bill_no")["total"])

# ==============================================================================
# PAGE 6: BILL HISTORY
# ==============================================================================

elif page == "📜 Bill History":
    st.markdown("""
    <div class="main-header">
        <h1 class="main-title">📜 Historical Bill Register</h1>
        <p class="subtitle">Browse past invoices, inspect item breakdowns & export CSV reports</p>
    </div>
    """, unsafe_allow_html=True)

    bills_df = db.get_bills()

    if bills_df.empty:
        st.info("No bill history records found in database.")
    else:
        st.dataframe(
            bills_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "subtotal": st.column_config.NumberColumn(format="₹%.2f"),
                "discount": st.column_config.NumberColumn(format="₹%.2f"),
                "tax": st.column_config.NumberColumn(format="₹%.2f"),
                "total": st.column_config.NumberColumn(format="₹%.2f"),
            }
        )

        csv_data = bills_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "📥 Export All Bills to CSV",
            data=csv_data,
            file_name="restaurant_bill_history.csv",
            mime="text/csv",
        )

        st.divider()
        st.markdown("### 🔍 Inspect & Reprint Bill Invoice")
        selected_bill_no = st.selectbox("Select Bill No to View/Reprint", bills_df["bill_no"].tolist())
        
        if selected_bill_no:
            bill_info, items_df = db.get_bill_by_no(selected_bill_no)
            if bill_info:
                st.markdown(f"**Customer:** {bill_info['customer']} | **Date:** {bill_info['created_at']} | **Total:** ₹{bill_info['total']:,.2f}")
                st.dataframe(items_df, use_container_width=True, hide_index=True)
                
                # Regenerate PDF button
                re_pdf = pdf_gen.generate_pdf_invoice(
                    bill_no=bill_info["bill_no"],
                    customer=bill_info["customer"],
                    phone=bill_info["phone"],
                    order_type=bill_info["order_type"],
                    table_no=bill_info["table_no"],
                    payment=bill_info["payment"],
                    notes=bill_info["notes"],
                    rows=items_df.to_dict(orient="records"),
                    subtotal=bill_info["subtotal"],
                    discount=bill_info["discount"],
                    tax_pct=tax_pct,
                    tax_amount=bill_info["tax"],
                    grand_total=bill_info["total"]
                )
                
                st.download_button(
                    f"📥 Reprint PDF Invoice ({bill_info['bill_no']})",
                    data=re_pdf,
                    file_name=f"{bill_info['bill_no']}.pdf",
                    mime="application/pdf"
                )

# ==============================================================================
# PAGE 7: ABOUT
# ==============================================================================

else:
    st.markdown("""
    <div class="main-header">
        <h1 class="main-title">ℹ️ About System</h1>
        <p class="subtitle">5 Star Restaurant & Hotel Management System Specifications</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    ### 🌟 System Capabilities
    - **POS & Billing Engine**: Instant item catalog, search, live quantity updates, GST/tax calculations.
    - **SQLite Database Persistence**: Full database storage for bills, customer CRM, menu items, and sales statistics.
    - **ReportLab PDF Generator**: Generate clean downloadable tax invoice PDFs with item breakdowns and tax splits.
    - **Interactive Table Management**: Live table floor plan with Available, Occupied, and Reserved table tracking.
    - **Dynamic Menu Manager**: Add new dishes, adjust prices, edit stock, and toggle dish availability.
    - **Customer CRM**: Automatic customer lookup by phone number, lifetime visit count, and spend tracking.
    - **Executive Analytics**: Real-time sales metrics, payment mode splits, order type analysis, and top-selling dishes.
    """)
