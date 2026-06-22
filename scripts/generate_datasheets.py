"""
Generate PDF datasheets for all 7 TERNS EXIM products.
Run from project root: python scripts/generate_datasheets.py
Output: static/datasheets/<product>.pdf
"""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer, HRFlowable
)
from reportlab.platypus.flowables import KeepTogether

# Brand colours
NAVY  = colors.HexColor("#0B1F3A")
GOLD  = colors.HexColor("#C9A84C")
LIGHT = colors.HexColor("#F5F7FA")
WHITE = colors.white
GREY  = colors.HexColor("#4B5563")
DGREY = colors.HexColor("#1A2A3A")

PAGE_W, PAGE_H = A4
MARGIN = 18 * mm

COMPANY = "TERNS EXIM"
TAGLINE = "Registered Merchant Exporter — Coimbatore, India"
EMAIL   = "sales@ternsexim.com"
PHONE   = "+91 63690 97465"
WEB     = "www.ternsexim.com"
PORTS   = "FOB / CIF from Chennai · Tuticorin · Mumbai · Mundra"
CURRENCIES = "USD · EUR · AED"
MOQ     = "10,000 pieces or 700 kg"
QA      = "Mill Test Certificate (EN 10204 Type 3.1) · Optional SGS / BV / TÜV inspection"

PRODUCTS = [
    {
        "filename": "hex_bolts.pdf",
        "title": "Hex Bolts",
        "subtitle": "Hexagonal Head Bolts — Partial & Full Thread",
        "hs_code": "7318.15",
        "specs": [
            ("Property Classes",    "4.6, 4.8, 5.8, 8.8, 10.9, 12.9"),
            ("Size Range",          "M4 – M100 (M5–M64 ex-stock; larger on order)"),
            ("Diameter × Length",   "M4–M100 metric; UNC/UNF 1/4\"–4\" also available"),
            ("Standards",           "DIN 931, DIN 933, ISO 4014, ISO 4017, ASTM A307, ASTM A325, ASTM A490, IS 1367, BS 3692"),
            ("Thread Types",        "Full thread (DIN 933 / ISO 4017); Partial thread (DIN 931 / ISO 4014)"),
            ("Materials",           "Carbon Steel (MS), Alloy Steel (Cr-Mo), SS 304 (A2), SS 316 (A4), Brass, Duplex SS"),
            ("Finishes",            "Plain / Black, Zinc Electroplated (Cr3), Hot-Dip Galvanized (HDG), Dacromet, Black Oxide"),
            ("MOQ",                 MOQ),
            ("Lead Time",           "7–21 working days from order confirmation"),
            ("Certification",       QA),
            ("HS Code",             "7318.15"),
        ],
        "grade_table": {
            "headers": ["Property Class", "Tensile Strength (MPa)", "Yield Strength (MPa)", "Typical Application"],
            "rows": [
                ["8.8",  "800",  "640",  "General structural, machinery, automotive"],
                ["10.9", "1040", "940",  "High-stress joints, heavy equipment, steel structures"],
                ["12.9", "1220", "1100", "Critical high-load, precision engineering"],
            ],
        },
        "applications": [
            "Steel structure fabrication & civil construction",
            "Automotive assembly and heavy transport vehicles",
            "Industrial machinery, pumps & compressors",
            "Petrochemical, oil & gas pipeline flanges",
            "Power generation & wind turbine structures",
            "Marine, offshore platforms & shipbuilding",
        ],
    },
    {
        "filename": "nuts.pdf",
        "title": "Industrial Nuts",
        "subtitle": "Hex, Heavy Hex, Lock, Flange, Nyloc, Castle, Coupling Nuts",
        "hs_code": "7318.16",
        "specs": [
            ("Types",            "Hex, Heavy Hex, Nyloc Lock, Flange, Castle (Slotted), Wing, Coupling (Long)"),
            ("Property Classes", "4, 5, 6, 8, 10, 12 (metric); Grade A/B/C/DH (ASTM A563)"),
            ("Size Range",       "M3 – M80 metric; 1/4\"–3\" UNC/UNF imperial"),
            ("Standards",        "DIN 934, DIN 985, DIN 6923, DIN 935, DIN 6334, ISO 4032, ISO 7042, ASTM A563, BS 3692, IS 1364"),
            ("Materials",        "Carbon Steel (MS), SS 304 (A2), SS 316 (A4), Alloy Steel, Brass, Bronze"),
            ("Finishes",         "Plain, Zinc Electroplated (Cr3), Hot-Dip Galvanized (HDG), Dacromet, Black Oxide, Phosphate"),
            ("MOQ",              MOQ),
            ("Lead Time",        "5–15 working days (standard); 15–25 days non-standard"),
            ("Certification",    QA),
            ("HS Code",          "7318.16"),
        ],
        "grade_table": {
            "headers": ["Nut Property Class", "Proof Load Stress (MPa)", "Mating Bolt", "Typical Use"],
            "rows": [
                ["8",  "800",  "Class 8.8 bolts",  "General structural and machinery"],
                ["10", "1040", "Class 10.9 bolts", "High-stress joints, heavy equipment"],
                ["12", "1150", "Class 12.9 bolts", "Critical high-load applications"],
            ],
        },
        "applications": [
            "General structural bolted connections & fabrication",
            "Automotive assembly lines & vehicle manufacturing",
            "Machinery, conveyors, and industrial equipment",
            "Pipe flanges, pressure vessels, and heat exchangers",
            "Electrical enclosures & panel boards",
            "Construction, bridges, and infrastructure projects",
        ],
    },
    {
        "filename": "washers.pdf",
        "title": "Industrial Washers",
        "subtitle": "Flat, Spring, Lock, Belleville, Fender & Structural Washers",
        "hs_code": "7318.22",
        "specs": [
            ("Types",         "Flat (DIN 125), Spring (DIN 127), Lock (DIN 6798), Belleville (DIN 2093), Fender, Structural (ASTM F436)"),
            ("Size Range",    "M3 – M100 metric; 3/16\"–4\" imperial; custom OD/ID available"),
            ("Standards",     "DIN 125-A/B, DIN 127-A/B, DIN 137, DIN 2093, ISO 7089, ISO 7090, ASTM F436, BS 4320, IS 2016"),
            ("Materials",     "Carbon Steel (MS), SS 304 (A2), SS 316 (A4), Alloy Steel, Brass, Copper, Bronze"),
            ("Finishes",      "Plain, Zinc Electroplated (Cr3), Hot-Dip Galvanized (HDG), Black Oxide, Phosphate, Dacromet"),
            ("Thickness",     "Per DIN/ISO standard; custom 0.5 mm – 20 mm available"),
            ("MOQ",           MOQ),
            ("Lead Time",     "5–14 working days (standard); 14–21 days custom dimensions"),
            ("Certification", QA),
            ("HS Code",       "7318.22"),
        ],
        "grade_table": {
            "headers": ["Washer Type", "Standard", "Primary Function"],
            "rows": [
                ["Flat Washer",           "DIN 125 / ISO 7089",  "Distributes load, protects surface"],
                ["Spring Washer",         "DIN 127",             "Resists loosening under vibration"],
                ["Lock Washer",           "DIN 6798",            "Teeth bite surface, prevents rotation"],
                ["Belleville Disc Spring","DIN 2093",            "High-load preload maintenance"],
                ["Fender Washer",         "DIN 9021",            "Large OD for soft or oversized holes"],
                ["Structural / Hardened", "ASTM F436",           "For A325 / A490 structural bolts"],
            ],
        },
        "applications": [
            "Structural steel bolted connections & fabrication",
            "Pipe flanges, pressure vessels, and heat exchangers",
            "Automotive, rail, and heavy vehicle assemblies",
            "Vibration-prone machinery and rotating equipment",
            "Electrical switchgear, panel boards, cable management",
            "HVAC, plumbing, and building services installations",
        ],
    },
    {
        "filename": "screws.pdf",
        "title": "Industrial Screws",
        "subtitle": "Machine, Self-Drilling, Wood, Drywall, Chipboard & Socket Cap Screws",
        "hs_code": "7318.15",
        "specs": [
            ("Types",         "Machine (CSK/Pan/Cheese), Self-Tapping, Self-Drilling, Wood, Drywall, Chipboard, Socket Cap"),
            ("Drive Types",   "Phillips (PH), Slotted, Pozi (PZ), Hex (Allen), Torx (TX), Combo"),
            ("Head Styles",   "Countersunk (CSK/Flat), Pan, Round, Cheese, Bugle, Truss, Hex Flange"),
            ("Size Range",    "M2 – M24 metric; #4–1/2\" imperial; ST 2.9–ST 6.3 self-tapping"),
            ("Length Range",  "6 mm – 200 mm standard; custom to 300 mm"),
            ("Standards",     "DIN 963, DIN 965, DIN 966, DIN 7981, DIN 7982, ISO 1207, ISO 7046, ASTM B18.6, IS 1367"),
            ("Property Class","4.8, 8.8 (machine); Class 12.9 (socket cap DIN 912); case-hardened (self-drilling)"),
            ("Materials",     "Carbon Steel (MS), SS 304 (A2), SS 316 (A4), Brass, Aluminium"),
            ("Finishes",      "Zinc Electroplated (Cr3), Black Phosphate, Black Oxide, Dacromet, Hot-Dip Galvanized, Bright Zinc"),
            ("MOQ",           MOQ),
            ("Lead Time",     "7–21 working days from order confirmation"),
            ("Certification", QA),
            ("HS Code",       "7318.15"),
        ],
        "grade_table": {
            "headers": ["Screw Type", "Standard", "Typical Application"],
            "rows": [
                ["Machine Screw",     "DIN 84 / DIN 963 / ISO 1207", "Fastening into pre-tapped metal holes"],
                ["Self-Tapping",      "DIN 7981",                    "Forms thread in sheet metal / plastic"],
                ["Self-Drilling",     "—",                           "Drills & taps in one operation"],
                ["Socket Cap",        "DIN 912",                     "High-strength machinery, class 12.9"],
                ["Drywall Screw",     "—",                           "Plasterboard to steel or timber studs"],
                ["Wood / Chipboard",  "—",                           "Timber, MDF, particleboard, decking"],
            ],
        },
        "applications": [
            "Electrical panels, switchgear & electronics assemblies",
            "Roofing sheets, cladding & metal building systems",
            "Furniture, cabinetry & timber frame construction",
            "Drywall / plasterboard partitioning systems",
            "Automotive interiors, HVAC ducting & sheet metal",
            "Marine fitout, solar panel mounting & signage",
        ],
    },
    {
        "filename": "threaded_rods.pdf",
        "title": "Threaded Rods & Stud Bolts",
        "subtitle": "Full Thread Rod (DIN 975), Stud Bolt (DIN 976), Anchor Rod",
        "hs_code": "7318.15",
        "specs": [
            ("Types",         "Full Thread Rod (DIN 975), Stud Bolt (DIN 976), Double-End Stud, Tap-End Stud, Anchor Rod"),
            ("Property Classes","4.8, 8.8 (metric); Grade B7 / B8 (ASTM A193)"),
            ("Diameter",      "M6 – M100"),
            ("Length",        "1000 mm – 6000 mm (standard 1 m & 2 m cuts; custom lengths on order)"),
            ("Standards",     "DIN 975, DIN 976, ASTM A193, ASTM A307, ASTM A320, IS 1367"),
            ("Materials",     "Carbon Steel (MS), Alloy Steel (Cr-Mo), SS 304 (A2), SS 316 (A4)"),
            ("Finishes",      "Plain, Zinc Electroplated, Hot-Dip Galvanized (HDG)"),
            ("MOQ",           MOQ),
            ("Lead Time",     "Quote on enquiry"),
            ("Certification", QA),
            ("HS Code",       "7318.15"),
        ],
        "grade_table": {
            "headers": ["Property Class", "Tensile Strength (MPa)", "Yield Strength (MPa)", "Typical Use"],
            "rows": [
                ["4.8",      "400",  "320",  "General-purpose, low-stress fixing"],
                ["8.8",      "800",  "640",  "Structural and high-load applications"],
                ["Gr. B7",   "860+", "725+", "High-temp pressure bolting (ASTM A193)"],
            ],
        },
        "applications": [
            "Anchor bolt extensions in civil foundations",
            "Suspended ceiling and HVAC duct hanging systems",
            "Pipe support hangers and strut channel assemblies",
            "High-pressure flange bolting in oil & gas (Grade B7)",
            "Structural tie rods in bridges and tension structures",
            "Machinery assembly and general-purpose threaded work",
        ],
    },
    {
        "filename": "anchor_bolts.pdf",
        "title": "Anchor Bolts",
        "subtitle": "J-Bolt, L-Bolt, U-Bolt, Eye Bolt, Wedge Anchor",
        "hs_code": "7318.15",
        "specs": [
            ("Types",         "J-Bolt, L-Bolt, U-Bolt, Eye Bolt, Rag Bolt, Lewis Bolt, Wedge Anchor"),
            ("Grades",        "Grade 36, 55, 105 (ASTM F1554); Property Class 4.6, 8.8 (IS)"),
            ("Size Range",    "M6 – M100 diameter (M12–M48 ex-stock; larger on order)"),
            ("Length",        "Up to 3000 mm; custom lengths from engineer drawings"),
            ("Standards",     "ASTM F1554, IS 1367, IS 5624, DIN 529, BS 7419"),
            ("Materials",     "Carbon Steel, SS 304 (A2), SS 316 (A4), Alloy Steel"),
            ("Finishes",      "Zinc Electroplated, Hot-Dip Galvanized (HDG)"),
            ("MOQ",           MOQ),
            ("Lead Time",     "Quote on enquiry"),
            ("Certification", QA),
            ("HS Code",       "7318.15"),
        ],
        "grade_table": {
            "headers": ["Type", "Shape", "Typical Application"],
            "rows": [
                ["J-Bolt",       "Curved hook (J-shape)",  "Cast-in-place; machinery bases, column anchoring"],
                ["L-Bolt",       "Right-angle 90° bend",   "Cast-in-place; horizontal pull-out resistance"],
                ["U-Bolt",       "U-shaped clamp",         "Clamping pipes / rods to structural members"],
                ["Wedge Anchor", "Expansion anchor",       "Post-installed; existing masonry / concrete"],
                ["Eye Bolt",     "Loop head",              "Lifting, rigging, and lifting lug applications"],
            ],
        },
        "applications": [
            "Anchoring structural steel columns to concrete piers",
            "Pump, compressor, and heavy equipment base plates",
            "Transmission towers & electricity pylons",
            "Solar panel mounting structures & wind masts",
            "Precast concrete & retaining wall construction",
            "Overhead crane runway beams & bridge structures",
        ],
    },
    {
        "filename": "foundation_bolts.pdf",
        "title": "Foundation Bolts",
        "subtitle": "J-Type, L-Type, Plate-Type — IS 5624 / ASTM F1554 / DIN 529",
        "hs_code": "7318.15",
        "specs": [
            ("Types",     "Type A, B, C, D, E per IS 5624; J-Type, L-Type, Plate-Type (Anchor Plate)"),
            ("Grades",    "Grade 36, 55, 105 (ASTM F1554); Property Class 4.6, 8.8 (IS)"),
            ("Diameter",  "M16 – M100"),
            ("Length",    "300 mm – 3000 mm; custom from engineer drawings (2-week approval)"),
            ("Standards", "IS 5624, ASTM F1554, DIN 529, BS 7419, IS 1367, EN 14399"),
            ("Materials", "Carbon Steel, SS 304 (A2), SS 316 (A4), Alloy Steel"),
            ("Finishes",  "Zinc Electroplated, Hot-Dip Galvanized (HDG)"),
            ("MOQ",       MOQ),
            ("Lead Time", "Quote on enquiry"),
            ("Certification", QA),
            ("HS Code",   "7318.15"),
        ],
        "grade_table": {
            "headers": ["Type", "Description", "Typical Application"],
            "rows": [
                ["J-Type",     "J-shaped hook cast into concrete",       "Steel columns, machinery bases"],
                ["L-Type",     "Right-angle 90° bend",                   "Horizontal pull-out resistance"],
                ["Plate-Type", "Bolt with welded anchor plate at base",   "Turbine pads, seismic zones — highest pull-out"],
            ],
        },
        "applications": [
            "Structural steel column base plates in buildings & bridges",
            "Heavy industrial machinery & turbine foundation pads",
            "Conveyor systems, compressors, and pumping stations",
            "Overhead crane rails and runway beam pedestals",
            "Power plant boilers, generators, and turbine halls",
            "Petrochemical, refinery, and offshore platform structures",
        ],
    },
]


def build_header(product):
    """Return a Table that acts as the page header."""
    left = Paragraph(
        f'<font size="18" color="#0B1F3A"><b>{product["title"]}</b></font><br/>'
        f'<font size="9" color="#4B5563">{product["subtitle"]}</font>',
        ParagraphStyle("h", fontName="Helvetica")
    )
    right = Paragraph(
        f'<font size="13" color="#C9A84C"><b>{COMPANY}</b></font><br/>'
        f'<font size="7.5" color="#4B5563">{TAGLINE}</font>',
        ParagraphStyle("r", fontName="Helvetica", alignment=2)
    )
    t = Table([[left, right]], colWidths=[(PAGE_W - 2*MARGIN)*0.58, (PAGE_W - 2*MARGIN)*0.42])
    t.setStyle(TableStyle([
        ("VALIGN",      (0,0), (-1,-1), "MIDDLE"),
        ("LINEBELOW",   (0,0), (-1,-1), 1.5, GOLD),
        ("BOTTOMPADDING",(0,0),(-1,-1), 6),
        ("TOPPADDING",  (0,0),(-1,-1), 6),
    ]))
    return t


def build_spec_table(rows):
    col1 = (PAGE_W - 2*MARGIN) * 0.30
    col2 = (PAGE_W - 2*MARGIN) * 0.70

    style = ParagraphStyle("cell", fontName="Helvetica", fontSize=8.5, leading=12, textColor=DGREY)
    data = []
    for i, (k, v) in enumerate(rows):
        key_p = Paragraph(f"<b>{k}</b>", style)
        val_p = Paragraph(v, style)
        data.append([key_p, val_p])

    t = Table(data, colWidths=[col1, col2])
    ts = [
        ("VALIGN",      (0,0),(-1,-1), "TOP"),
        ("TOPPADDING",  (0,0),(-1,-1), 4),
        ("BOTTOMPADDING",(0,0),(-1,-1), 4),
        ("LEFTPADDING", (0,0),(-1,-1), 6),
        ("RIGHTPADDING",(0,0),(-1,-1), 6),
        ("LINEBELOW",   (0,0),(-1,-2), 0.5, colors.HexColor("#E2E8F0")),
        ("ROWBACKGROUNDS", (0,0),(-1,-1), [WHITE, LIGHT]),
        ("BOX",         (0,0),(-1,-1), 0.5, colors.HexColor("#CBD5E0")),
    ]
    t.setStyle(TableStyle(ts))
    return t


def build_grade_table(gt):
    headers = gt["headers"]
    rows    = gt["rows"]
    n_cols  = len(headers)
    avail   = PAGE_W - 2*MARGIN
    col_w   = [avail / n_cols] * n_cols

    header_style = ParagraphStyle("th", fontName="Helvetica-Bold", fontSize=8, textColor=WHITE, leading=11)
    cell_style   = ParagraphStyle("td", fontName="Helvetica", fontSize=8, textColor=DGREY, leading=11)

    data = [[Paragraph(h, header_style) for h in headers]]
    for row in rows:
        data.append([Paragraph(cell, cell_style) for cell in row])

    t = Table(data, colWidths=col_w)
    ts = [
        ("BACKGROUND",  (0,0),(-1,0), NAVY),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[WHITE, LIGHT]),
        ("VALIGN",      (0,0),(-1,-1), "MIDDLE"),
        ("TOPPADDING",  (0,0),(-1,-1), 4),
        ("BOTTOMPADDING",(0,0),(-1,-1), 4),
        ("LEFTPADDING", (0,0),(-1,-1), 6),
        ("RIGHTPADDING",(0,0),(-1,-1), 6),
        ("LINEBELOW",   (0,0),(-1,-1), 0.5, colors.HexColor("#CBD5E0")),
        ("BOX",         (0,0),(-1,-1), 0.5, colors.HexColor("#CBD5E0")),
    ]
    t.setStyle(TableStyle(ts))
    return t


def build_applications(apps):
    style = ParagraphStyle("app", fontName="Helvetica", fontSize=8.5, textColor=DGREY, leading=13)
    items = [Paragraph(f"<b>✔</b>  {a}", style) for a in apps]
    # 2-column layout
    mid = (len(items) + 1) // 2
    left_col  = items[:mid]
    right_col = items[mid:]
    # pad to same length
    while len(right_col) < len(left_col):
        right_col.append(Paragraph("", style))
    data = list(zip(left_col, right_col))
    col_w = [(PAGE_W - 2*MARGIN) / 2] * 2
    t = Table(data, colWidths=col_w)
    t.setStyle(TableStyle([
        ("VALIGN", (0,0),(-1,-1), "TOP"),
        ("TOPPADDING",  (0,0),(-1,-1), 3),
        ("BOTTOMPADDING",(0,0),(-1,-1), 3),
    ]))
    return t


def build_export_footer(hs_code):
    style = ParagraphStyle("ft", fontName="Helvetica", fontSize=8, textColor=GREY, leading=12)
    bold  = ParagraphStyle("ftb", fontName="Helvetica-Bold", fontSize=8, textColor=NAVY, leading=12)

    export_data = [
        [Paragraph("<b>Export Terms</b>", bold), Paragraph(PORTS, style)],
        [Paragraph("<b>Currencies</b>",   bold), Paragraph(CURRENCIES, style)],
        [Paragraph("<b>MOQ</b>",          bold), Paragraph(MOQ, style)],
        [Paragraph("<b>HS Code</b>",      bold), Paragraph(hs_code, style)],
        [Paragraph("<b>Quality</b>",      bold), Paragraph(QA, style)],
    ]
    col1 = 30 * mm
    col2 = PAGE_W - 2*MARGIN - col1
    t = Table(export_data, colWidths=[col1, col2])
    t.setStyle(TableStyle([
        ("VALIGN",      (0,0),(-1,-1), "TOP"),
        ("TOPPADDING",  (0,0),(-1,-1), 3),
        ("BOTTOMPADDING",(0,0),(-1,-1), 3),
        ("LEFTPADDING", (0,0),(-1,-1), 0),
        ("LINEBELOW",   (0,0),(-1,-2), 0.4, colors.HexColor("#E2E8F0")),
    ]))
    return t


def build_contact_bar():
    style = ParagraphStyle("cb", fontName="Helvetica-Bold", fontSize=8.5, textColor=WHITE, leading=13)
    text  = f"{COMPANY}  |  {EMAIL}  |  {PHONE}  |  {WEB}  |  Merchant Exporter · Not a Manufacturer"
    t = Table([[Paragraph(text, style)]], colWidths=[PAGE_W - 2*MARGIN])
    t.setStyle(TableStyle([
        ("BACKGROUND",   (0,0),(0,0), NAVY),
        ("TOPPADDING",   (0,0),(0,0), 7),
        ("BOTTOMPADDING",(0,0),(0,0), 7),
        ("LEFTPADDING",  (0,0),(0,0), 10),
        ("ALIGN",        (0,0),(0,0), "CENTER"),
    ]))
    return t


def section_heading(text):
    return Paragraph(
        f'<font name="Helvetica-Bold" size="10" color="#0B1F3A">{text}</font>',
        ParagraphStyle("sh", spaceAfter=4)
    )


def build_pdf(product, out_dir):
    path = os.path.join(out_dir, product["filename"])
    doc  = SimpleDocTemplate(
        path,
        pagesize=A4,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=MARGIN,  bottomMargin=MARGIN + 4*mm,
        title=f"{product['title']} Datasheet — TERNS EXIM",
        author="TERNS EXIM",
        subject=product["subtitle"],
    )

    story = []

    # Header
    story.append(build_header(product))
    story.append(Spacer(1, 8*mm))

    # Specifications
    story.append(section_heading("Technical Specifications"))
    story.append(build_spec_table(product["specs"]))
    story.append(Spacer(1, 6*mm))

    # Grade / type table
    if product.get("grade_table"):
        story.append(section_heading("Grades / Types at a Glance"))
        story.append(build_grade_table(product["grade_table"]))
        story.append(Spacer(1, 6*mm))

    # Applications
    if product.get("applications"):
        story.append(section_heading("Key Applications"))
        story.append(build_applications(product["applications"]))
        story.append(Spacer(1, 6*mm))

    # Gold separator
    story.append(HRFlowable(width="100%", thickness=1.5, color=GOLD))
    story.append(Spacer(1, 4*mm))

    # Export & QA info
    story.append(section_heading("Export & Quality Information"))
    story.append(build_export_footer(product["hs_code"]))
    story.append(Spacer(1, 5*mm))

    # Contact bar
    story.append(build_contact_bar())

    doc.build(story)
    print(f"  Generated: {product['filename']}")


if __name__ == "__main__":
    out_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                           "static", "datasheets")
    os.makedirs(out_dir, exist_ok=True)
    print(f"Writing PDFs to: {out_dir}")
    for p in PRODUCTS:
        build_pdf(p, out_dir)
    print(f"Done — {len(PRODUCTS)} datasheets generated.")
