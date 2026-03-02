import streamlit as st
from datetime import date
import os
from invoice_pdf import generate_outstation_pdf, generate_local_pdf

st.set_page_config(page_title="Shidhi Travels Billing", layout="centered")

# CSS Styling
st.markdown("""
    <style>
    div.stButton > button:first-child {
        background-color: #b30000; 
        color: white; 
        width: 100%;
        height: 50px;
        font-size: 18px;
        border: none;
        border-radius: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# ---- LOGIC: MANAGE INVOICE NUMBER ----
def get_invoice_number():
    # If file doesn't exist, start at 1001
    if not os.path.exists("invoice_counter.txt"):
        with open("invoice_counter.txt", "w") as f:
            f.write("1001")
        return 1001
    # Read the last number
    with open("invoice_counter.txt", "r") as f:
        try:
            return int(f.read())
        except:
            return 1001

def increment_invoice_number(current_no):
    # Save the NEXT number (current + 1)
    with open("invoice_counter.txt", "w") as f:
        f.write(str(current_no + 1))

# ---- SIDEBAR ----
try:
    st.sidebar.image("assets/logo.png", width=150)
except:
    st.sidebar.write("PRIYANSHU TOURS & TRAVELS")
    
invoice_type = st.sidebar.radio("Select Invoice Type", ["Outstation Trip", "Local Trip"])

st.title(f"{invoice_type}")

# Load the number from file
current_invoice_no = get_invoice_number()

# Allow manual override (Important for Mobile usage)
col_inv, col_empty = st.columns([1, 2])
with col_inv:
    invoice_no = st.number_input("Invoice No.", value=current_invoice_no, step=1)

# ---- INPUTS ----
col1, col2 = st.columns(2)
with col1:
    customer = st.text_input("Customer Name")
    mobile = st.text_input("Customer Mobile")
with col2:
    vehicle = st.text_input("Vehicle No / Model")

st.divider()

# ===========================
# 1. OUTSTATION
# ===========================
if invoice_type == "Outstation Trip":
    travel_date = st.date_input("Date of Journey", value=date.today())
    
    c1, c2, c3 = st.columns(3)
    with c1: kms = st.number_input("Total KMs", min_value=0)
    with c2: rate = st.number_input("Rate per KM", min_value=0.0)
    with c3: days = st.number_input("Total Days", min_value=1)
    
    route = st.text_input("Route Description")
    
    st.subheader("Extra Charges")
    e1, e2 = st.columns(2)
    driver_allow = e1.number_input("Driver Allowance", step=50.0)
    toll = e2.number_input("Toll / Parking", step=50.0)

    # Calculate
    main_amount = kms * rate
    extras = []
    if driver_allow > 0: extras.append(("Driver Allowance", 1, driver_allow, driver_allow))
    if toll > 0: extras.append(("Toll / Parking", 1, toll, toll))
    
    total = main_amount + sum(x[3] for x in extras)

    if st.button("Generate Outstation Bill"):
        data = {
            "invoice_no": invoice_no,
            "date": date.today().strftime("%d-%m-%Y"),
            "customer": customer, "vehicle": vehicle,
            "kms": kms, "rate": rate, "main_amount": main_amount,
            "route": route, "days": days, "travel_date": travel_date.strftime("%d-%m-%Y"),
            "extras": extras, "total": total
        }
        pdf = generate_outstation_pdf(data)
        
        # Save the new number for next time
        increment_invoice_number(invoice_no)
        
        st.success(f"Invoice {invoice_no} Generated!")
        st.download_button("Download PDF", pdf, f"Invoice_{invoice_no}.pdf", "application/pdf")
        
        # Refresh to show new number (optional, requires rerun)
        # st.experimental_rerun()

# ===========================
# 2. LOCAL TRIP
# ===========================
else:
    # --- DATE RANGE PICKER ---
    d1, d2 = st.columns(2)
    from_d = d1.date_input("From Date", value=date.today())
    to_d = d2.date_input("To Date", value=date.today())
    
    # Calculate Total Days
    total_days = (to_d - from_d).days + 1
    if total_days < 1: total_days = 1
    
    st.info(f"Total Billable Days: {total_days}")

    # --- PACKAGE ---
    l1, l2 = st.columns(2)
    base_rate = l1.number_input("Package Rate (Per Day)", value=3000.0)
    
    base_amount = base_rate * total_days
    
    st.write("---")
    
    # --- EXTRA HOURS & MINUTES ---
    st.caption("Extra Time")
    t1, t2, t3 = st.columns(3)
    e_hr_qty = t1.number_input("Extra Hours", min_value=0)
    e_min_qty = t2.number_input("Extra Minutes", min_value=0, max_value=59, step=15)
    e_hr_rate = t3.number_input("Rate per Hour", value=200.0)
    
    # --- EXTRA KMS ---
    st.caption("Extra KMs")
    k1, k2 = st.columns(2)
    e_km_qty = k1.number_input("Extra KMs", min_value=0)
    e_km_rate = k2.number_input("Rate per KM", value=18.0)
    
    toll_local = st.number_input("Toll / Parking (Local)", step=50.0)

    # --- CALCULATION ---
    total_extra_hours = e_hr_qty + (e_min_qty / 60)
    extra_hr_amt = total_extra_hours * e_hr_rate
    extra_km_amt = e_km_qty * e_km_rate
    
    subtotal = base_amount + extra_hr_amt + extra_km_amt
    total_local = subtotal + toll_local

    st.markdown(f"### Total: Rs. {total_local:,.2f}")

    if st.button("Generate Local Bill"):
        data = {
            "invoice_no": invoice_no,
            "date": date.today().strftime("%d-%m-%Y"),
            "from_date": from_d.strftime("%d-%m-%Y"),
            "to_date": to_d.strftime("%d-%m-%Y"),
            "total_days": total_days,
            "customer": customer, "mobile": mobile, "vehicle": vehicle,
            "rate": base_rate, "main_amount": base_amount,
            
            "extra_hrs_qty": e_hr_qty, "extra_mins_qty": e_min_qty, 
            "extra_hrs_rate": e_hr_rate, "extra_hrs_amt": extra_hr_amt,
            
            "extra_kms_qty": e_km_qty, "extra_kms_rate": e_km_rate, "extra_kms_amt": extra_km_amt,
            "subtotal": subtotal, "toll": toll_local, "total": total_local
        }
        pdf = generate_local_pdf(data)
        
        # Save the new number
        increment_invoice_number(invoice_no)

        st.success(f"Invoice {invoice_no} Generated!")
        st.download_button("Download Local Bill", pdf, f"Invoice_{invoice_no}.pdf", "application/pdf")
