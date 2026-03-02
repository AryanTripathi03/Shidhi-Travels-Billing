from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from io import BytesIO

# ---- CONFIGURATION ----
GREEN = HexColor("#8FBF3D")
RED = HexColor("#b30000")
COMPANY_NAME = "SHIDHI TOURS & TRAVELS"
MOBILE = "+91 9326719539"
EMAIL = "ravindratiwari7074@gmail.com"
# Single line address to prevent errors
ADDRESS = "Gautam nagar Arey milk colony N.modern backery goregaon East 400065"

BANK_DETAILS = (
    "Bank Details\n"
    "Bank Name: Punjab National Bank\n"
    "Name: SHIDHi TOURS AND TRAVELS\n"
    "A/C No: 10872413000535\n"
    "IFSC: PUNB0108710\n"
    "Branch: POONAM NAGAR"
)

# ==========================================
# 1. OUTSTATION PDF
# ==========================================
def generate_outstation_pdf(data):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    w, h = A4

    # HEADER
    try:
        c.drawImage("assets/logo.png", 40, h-95, width=120, height=60, mask='auto')
    except:
        c.setFont("Helvetica-Bold", 20)
        c.drawString(40, h-60, COMPANY_NAME)

    c.setFont("Helvetica-Bold", 10)
    c.drawRightString(w-40, h-50, "OUTSTATION INVOICE")
    c.setFont("Helvetica", 10)
    c.drawRightString(w-40, h-70, f"Mobile: {MOBILE}")
    c.drawRightString(w-40, h-85, f"Email: {EMAIL}")
    
    c.setFont("Helvetica", 8)
    c.drawRightString(w-40, h-100, ADDRESS)

    # BILL TO
    c.setFont("Helvetica-Bold", 10)
    c.drawString(40, h-150, "BILL TO")
    c.setFont("Helvetica", 10)
    c.drawString(40, h-165, data["customer"])
    c.drawRightString(w-40, h-150, f"Invoice #: {data['invoice_no']}")
    c.drawRightString(w-40, h-165, f"Date: {data['date']}")

    # TABLE
    c.setFillColor(GREEN)
    c.rect(40, h-200, w-80, 22, fill=1, stroke=0)
    c.setFillColorRGB(1,1,1)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, h-195, "Vehicle / Description")
    c.drawString(260, h-195, "KMs")
    c.drawString(360, h-195, "Rate")
    c.drawString(450, h-195, "Amount")

    y = h-225
    c.setFillColorRGB(0,0,0)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, y, data["vehicle"])
    c.drawRightString(330, y, str(data["kms"]))
    c.drawRightString(420, y, f"Rs. {data['rate']:.2f}")
    c.drawRightString(w-50, y, f"Rs. {data['main_amount']:.2f}")

    c.setFont("Helvetica", 9)
    c.setFillColorRGB(0.3, 0.3, 0.3)
    c.drawString(50, y-15, f"Route: {data['route']}")
    c.drawString(50, y-28, f"Travel Date: {data['travel_date']}")
    c.drawString(50, y-41, f"Total Days: {data['days']}")

    y2 = y-65
    c.setFillColorRGB(0,0,0)
    for name, qty, price, amt in data["extras"]:
        c.setFont("Helvetica", 10)
        c.drawString(50, y2, name)
        c.drawRightString(330, y2, str(qty))
        c.drawRightString(420, y2, f"Rs. {price:.2f}")
        c.drawRightString(w-50, y2, f"Rs. {amt:.2f}")
        y2 -= 18

    # TOTALS
    c.setStrokeColor(HexColor("#cccccc"))
    c.line(350, y2-10, w-40, y2-10)
    c.setFont("Helvetica", 10)
    c.drawRightString(420, y2-30, "Subtotal")
    c.drawRightString(w-50, y2-30, f"Rs. {data['total']:.2f}")

    c.setFillColor(GREEN)
    c.rect(350, y2-60, w-390, 22, fill=1, stroke=0)
    c.setFillColorRGB(1,1,1)
    c.setFont("Helvetica-Bold", 11)
    
    # FIXED OVERLAP for Outstation as well
    c.drawRightString(w-180, y2-55, "Grand Total")
    c.drawRightString(w-50, y2-55, f"Rs. {data['total']:,.2f}")

    # FOOTER
    y_section = y2 - 100
    c.setFillColorRGB(0,0,0)
    c.setFont("Helvetica", 9)
    text = c.beginText(40, y_section)
    for line in BANK_DETAILS.split("\n"): text.textLine(line)
    c.drawText(text)

    qr_size = 120
    try:
        c.setFont("Helvetica-Bold", 8)
        c.drawRightString(w-40, y_section + 10, "SCAN TO PAY")
        c.drawImage("assets/payment_qr.png", w-130, y_section - 110, width=qr_size, height=qr_size, mask='auto')
    except: pass

    y_sig = y_section - 180
    if y_sig < 50: c.showPage(); y_sig = h - 150
    try: c.drawImage("assets/signature.png", 40, y_sig, width=120, height=40, mask='auto')
    except: pass
    c.setFont("Helvetica", 9)
    c.drawString(40, y_sig - 10, f"For {COMPANY_NAME}")

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer


# ==========================================
# 2. LOCAL PDF (WITH OVERLAP FIX)
# ==========================================
def generate_local_pdf(data):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    w, h = A4

    # HEADER
    try:
        c.drawImage("assets/logo.png", 40, h-95, width=120, height=60, mask='auto')
    except:
        c.setFont("Helvetica-Bold", 20)
        c.drawString(40, h-60, COMPANY_NAME)

    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(RED)
    c.drawRightString(w-40, h-50, COMPANY_NAME)
    
    c.setFillColorRGB(0,0,0)
    c.setFont("Helvetica", 8)
    c.drawRightString(w-40, h-65, ADDRESS)
    c.setFont("Helvetica", 9)
    c.drawRightString(w-40, h-80, f"Mobile: {MOBILE}")
    c.drawRightString(w-40, h-92, f"Email: {EMAIL}")

    c.setStrokeColor(RED); c.setLineWidth(2)
    c.line(40, h-105, w-40, h-105); c.setLineWidth(1)

    # INFO BAR
    c.setFillColor(HexColor("#eeeeee"))
    c.rect(40, h-145, w-80, 20, fill=1, stroke=0)
    c.setFillColorRGB(0,0,0)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, h-139, f"Invoice No.: {data['invoice_no']}")
    c.drawRightString(w-50, h-139, f"Invoice Date: {data['date']}")

    # BILL TO
    c.setFont("Helvetica-Bold", 9)
    c.drawString(40, h-170, "BILL TO")
    c.setFont("Helvetica", 10)
    c.drawString(40, h-185, data["customer"])
    
    c.setFont("Helvetica-Bold", 9)
    c.drawRightString(w-40, h-170, f"Period: {data['from_date']} to {data['to_date']}")
    c.drawRightString(w-40, h-185, f"Vehicle No: {data['vehicle']}")

    # TABLE HEADER
    y_head = h-220
    c.setStrokeColor(HexColor("#000000"))
    c.line(40, y_head, w-40, y_head)
    c.line(40, y_head-20, w-40, y_head-20)
    
    c.setFont("Helvetica-Bold", 9)
    c.drawString(50, y_head-14, "SERVICES")
    c.drawRightString(360, y_head-14, "QTY.")
    c.drawRightString(450, y_head-14, "RATE")
    c.drawRightString(w-40, y_head-14, "AMOUNT")

    # ROWS
    y = y_head - 40
    c.setFont("Helvetica", 10)

    # Row 1
    c.drawString(50, y, f"{data['vehicle']} LOCAL USE")
    c.setFont("Helvetica", 8)
    c.drawString(50, y-12, f"({data['from_date']} to {data['to_date']})")
    c.setFont("Helvetica", 10)
    c.drawRightString(360, y, f"{data['total_days']} DAYS")
    c.drawRightString(450, y, str(data['rate']))
    c.drawRightString(w-40, y, str(data['main_amount']))
    y -= 25

    # Row 2
    if data['extra_hrs_qty'] > 0 or data['extra_mins_qty'] > 0:
        c.drawString(50, y, "EXTRA HOURS")
        time_str = f"{int(data['extra_hrs_qty'])}:{int(data['extra_mins_qty']):02d} HRS"
        c.drawRightString(360, y, time_str)
        c.drawRightString(450, y, str(data['extra_hrs_rate']))
        c.drawRightString(w-40, y, str(data['extra_hrs_amt']))
        y -= 25

    # Row 3
    if data['extra_kms_qty'] > 0:
        c.drawString(50, y, "EXTRA KM")
        c.drawRightString(360, y, f"{data['extra_kms_qty']} KMS")
        c.drawRightString(450, y, str(data['extra_kms_rate']))
        c.drawRightString(w-40, y, str(data['extra_kms_amt']))
        y -= 25

    # TOTALS
    y -= 10
    c.setStrokeColor(HexColor("#cccccc"))
    c.line(40, y, w-40, y)
    y -= 20

    c.setFont("Helvetica-Bold", 10)
    c.drawString(40, y, "SUBTOTAL")
    c.drawRightString(w-50, y, f"Rs. {data['subtotal']:,.2f}") # Comma format

    if data['toll'] > 0:
        y -= 20
        c.setFont("Helvetica", 9)
        c.drawRightString(w-120, y, "Toll / Parking :")
        c.drawRightString(w-50, y, f"Rs. {data['toll']}")

    # ---- TOTAL FIX IS HERE ----
    y -= 25
    c.setStrokeColor(HexColor("#000000"))
    c.line(w-200, y+15, w-40, y+15)
    
    c.setFont("Helvetica-Bold", 12)
    # Moved label to w-180 to allow space for Rs. 1,20,000
    c.drawRightString(w-180, y, "Total Amount") 
    c.drawRightString(w-40, y, f"Rs. {data['total']:,.2f}")

    # FOOTER
    y_footer = y - 60 
    
    c.setFont("Helvetica-Bold", 9)
    c.drawString(40, y_footer, "BANK DETAILS")
    c.setFont("Helvetica", 8)
    text = c.beginText(40, y_footer - 15)
    for line in BANK_DETAILS.split("\n"): text.textLine(line)
    c.drawText(text)

    qr_x = 180 
    qr_size = 100
    try:
        c.drawImage("assets/payment_qr.png", qr_x, y_footer - 85, width=qr_size, height=qr_size)
        c.setFont("Helvetica-Bold", 8)
        c.drawString(qr_x + 10, y_footer - 95, "Scan to Pay")
    except: pass

    try:
        c.drawImage("assets/signature.png", w-150, y_footer - 70, width=100, height=40)
        c.setFont("Helvetica-Bold", 8)
        c.drawRightString(w-40, y_footer - 85, "AUTHORISED SIGNATORY")
        c.drawRightString(w-40, y_footer - 95, f"For {COMPANY_NAME}")
    except: pass

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer
