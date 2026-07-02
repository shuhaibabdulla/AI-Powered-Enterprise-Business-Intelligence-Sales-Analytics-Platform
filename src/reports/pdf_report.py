# ================================================
# RETAILX CORP — AUTOMATED PDF REPORT GENERATOR
# Run: python src/reports/pdf_report.py
# Output: outputs/pdf/retailx_report.pdf
# ================================================

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer,
    Table, TableStyle, HRFlowable
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
import pandas as pd
import os
from datetime import datetime

# ---- PATHS ----
EXPORTS_PATH = 'outputs/exports/'
OUTPUT_PATH  = 'outputs/pdf/'
os.makedirs(OUTPUT_PATH, exist_ok=True)

# ---- LOAD DATA ----
print("📂 Loading data...")
executive = pd.read_csv(EXPORTS_PATH + 'executive_kpi_summary.csv')
categories = pd.read_csv(EXPORTS_PATH + 'category_kpis.csv')
monthly    = pd.read_csv(EXPORTS_PATH + 'monthly_revenue.csv')
forecast   = pd.read_csv(EXPORTS_PATH + 'sales_forecast.csv')
print("✅ Data loaded")

# ---- COLORS ----
DARK_BLUE  = colors.HexColor('#1E3A5F')
LIGHT_BLUE = colors.HexColor('#2563EB')
WHITE      = colors.white
LIGHT_GRAY = colors.HexColor('#F8F9FA')
DARK_GRAY  = colors.HexColor('#343A40')
GREEN      = colors.HexColor('#198754')
RED        = colors.HexColor('#DC3545')
YELLOW     = colors.HexColor('#FFC107')

# ---- DOCUMENT ----
output_file = OUTPUT_PATH + 'retailx_report.pdf'
doc = SimpleDocTemplate(
    output_file,
    pagesize=A4,
    rightMargin=1.5*cm,
    leftMargin=1.5*cm,
    topMargin=1.5*cm,
    bottomMargin=1.5*cm
)

# ---- STYLES ----
styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    'CustomTitle',
    parent=styles['Title'],
    fontSize=24,
    textColor=WHITE,
    backColor=DARK_BLUE,
    alignment=TA_CENTER,
    spaceAfter=6,
    spaceBefore=6,
    fontName='Helvetica-Bold',
    leading=30
)

subtitle_style = ParagraphStyle(
    'Subtitle',
    parent=styles['Normal'],
    fontSize=11,
    textColor=DARK_GRAY,
    alignment=TA_CENTER,
    spaceAfter=20,
    fontName='Helvetica'
)

section_style = ParagraphStyle(
    'Section',
    parent=styles['Heading1'],
    fontSize=14,
    textColor=WHITE,
    backColor=LIGHT_BLUE,
    spaceBefore=15,
    spaceAfter=8,
    fontName='Helvetica-Bold',
    leading=20,
    leftIndent=5
)

body_style = ParagraphStyle(
    'Body',
    parent=styles['Normal'],
    fontSize=10,
    textColor=DARK_GRAY,
    spaceAfter=6,
    fontName='Helvetica',
    leading=14
)

insight_style = ParagraphStyle(
    'Insight',
    parent=styles['Normal'],
    fontSize=10,
    textColor=DARK_GRAY,
    spaceAfter=4,
    fontName='Helvetica',
    leftIndent=10,
    leading=14
)

# ---- BUILD CONTENT ----
content = []

# ================================================
# HEADER
# ================================================
content.append(Paragraph(
    "RetailX Corp", title_style
))
content.append(Paragraph(
    "AI-Powered Business Intelligence Report", title_style
))
content.append(Spacer(1, 0.3*cm))
content.append(Paragraph(
    f"Generated: {datetime.now().strftime('%B %d, %Y')} "
    f"| Data Period: 2016 - 2018 "
    f"| Market: Brazil",
    subtitle_style
))
content.append(HRFlowable(
    width="100%", thickness=2,
    color=LIGHT_BLUE, spaceAfter=10
))

# ================================================
# SECTION 1: EXECUTIVE SUMMARY
# ================================================
content.append(Paragraph("1. Executive KPI Summary", section_style))
content.append(Spacer(1, 0.2*cm))

# KPI Table
kpi_table_data = [
    ['KPI', 'Value', 'Status']
]

kpi_rows = [
    ('Total Revenue',           'R$ 15,843,553.24', '✅ Strong'),
    ('Total Orders',            '99,441',            '✅ Strong'),
    ('Average Order Value',     'R$ 160.58',         '✅ Good'),
    ('Total Unique Customers',  '96,096',            '✅ Strong'),
    ('Repeat Purchase Rate',    '3.1%',              '⚠️ Low'),
    ('Avg Delivery Days',       '12.0 days',         '⚠️ Monitor'),
    ('Late Delivery Rate',      '8.1%',              '⚠️ Monitor'),
    ('Average Review Score',    '4.09 / 5.00',       '✅ Good'),
    ('YoY Revenue Growth',      '21.0%',             '✅ Strong'),
]

for row in kpi_rows:
    kpi_table_data.append(list(row))

kpi_table = Table(
    kpi_table_data,
    colWidths=[7*cm, 5*cm, 4*cm]
)
kpi_table.setStyle(TableStyle([
    # Header
    ('BACKGROUND',  (0,0), (-1,0), DARK_BLUE),
    ('TEXTCOLOR',   (0,0), (-1,0), WHITE),
    ('FONTNAME',    (0,0), (-1,0), 'Helvetica-Bold'),
    ('FONTSIZE',    (0,0), (-1,0), 11),
    ('ALIGN',       (0,0), (-1,0), 'CENTER'),
    ('TOPPADDING',  (0,0), (-1,0), 8),
    ('BOTTOMPADDING',(0,0),(-1,0), 8),
    # Data rows
    ('FONTNAME',    (0,1), (-1,-1), 'Helvetica'),
    ('FONTSIZE',    (0,1), (-1,-1), 10),
    ('ALIGN',       (1,1), (-1,-1), 'CENTER'),
    ('ALIGN',       (0,1), (0,-1), 'LEFT'),
    ('TOPPADDING',  (0,1), (-1,-1), 6),
    ('BOTTOMPADDING',(0,1),(-1,-1), 6),
    # Alternating rows
    ('BACKGROUND',  (0,1), (-1,1),  LIGHT_GRAY),
    ('BACKGROUND',  (0,3), (-1,3),  LIGHT_GRAY),
    ('BACKGROUND',  (0,5), (-1,5),  LIGHT_GRAY),
    ('BACKGROUND',  (0,7), (-1,7),  LIGHT_GRAY),
    ('BACKGROUND',  (0,9), (-1,9),  LIGHT_GRAY),
    # Value column color
    ('TEXTCOLOR',   (1,1), (1,-1), LIGHT_BLUE),
    # Grid
    ('GRID',        (0,0), (-1,-1), 0.5, colors.HexColor('#DDDDDD')),
    ('ROWBACKGROUNDS', (0,0), (-1,-1), [WHITE, LIGHT_GRAY]),
]))

content.append(kpi_table)
content.append(Spacer(1, 0.5*cm))

# ================================================
# SECTION 2: KEY BUSINESS INSIGHTS
# ================================================
content.append(Paragraph("2. Key Business Insights", section_style))
content.append(Spacer(1, 0.2*cm))

insights = [
    "💰 <b>Revenue:</b> Total revenue of R$ 15.84M across 99,441 orders demonstrates strong market presence in Brazilian e-commerce.",
    "📈 <b>Growth:</b> 21% Year-over-Year revenue growth indicates healthy business expansion and increasing market share.",
    "⚠️ <b>Retention Risk:</b> Repeat purchase rate of only 3.1% is critically low. 96.9% of customers buy once and never return — immediate retention strategy required.",
    "🚚 <b>Delivery Performance:</b> Average delivery time of 12 days with 8.1% late delivery rate needs operational improvement to boost customer satisfaction.",
    "⭐ <b>Customer Satisfaction:</b> Average review score of 4.09/5.00 indicates generally positive customer experience despite delivery concerns.",
    "🏆 <b>Top Category:</b> Health Beauty leads in revenue, followed by Watches Gifts and Bed Bath Table — focus marketing on these categories.",
]

for insight in insights:
    content.append(Paragraph(f"• {insight}", insight_style))
    content.append(Spacer(1, 0.1*cm))

content.append(Spacer(1, 0.3*cm))

# ================================================
# SECTION 3: TOP PRODUCT CATEGORIES
# ================================================
content.append(Paragraph("3. Top 10 Product Categories", section_style))
content.append(Spacer(1, 0.2*cm))

cat_sorted = categories.sort_values(
    'total_revenue', ascending=False
).head(10).reset_index(drop=True)

cat_table_data = [['Rank', 'Category', 'Revenue (R$)', 'Orders']]
for i, row in cat_sorted.iterrows():
    rank = ['🥇','🥈','🥉'][i] if i < 3 else str(i+1)
    cat_table_data.append([
        rank,
        row['product_category_name_english'],
        f"R$ {row['total_revenue']:,.0f}",
        f"{int(row['total_orders']):,}"
    ])

cat_table = Table(
    cat_table_data,
    colWidths=[2*cm, 8*cm, 5*cm, 3*cm]
)
cat_table.setStyle(TableStyle([
    ('BACKGROUND',   (0,0), (-1,0), DARK_BLUE),
    ('TEXTCOLOR',    (0,0), (-1,0), WHITE),
    ('FONTNAME',     (0,0), (-1,0), 'Helvetica-Bold'),
    ('FONTSIZE',     (0,0), (-1,0), 10),
    ('ALIGN',        (0,0), (-1,-1), 'CENTER'),
    ('ALIGN',        (1,1), (1,-1), 'LEFT'),
    ('FONTNAME',     (0,1), (-1,-1), 'Helvetica'),
    ('FONTSIZE',     (0,1), (-1,-1), 9),
    ('TOPPADDING',   (0,0), (-1,-1), 5),
    ('BOTTOMPADDING',(0,0), (-1,-1), 5),
    ('TEXTCOLOR',    (2,1), (2,-1), LIGHT_BLUE),
    ('GRID',         (0,0), (-1,-1), 0.5,
     colors.HexColor('#DDDDDD')),
    ('ROWBACKGROUNDS',(0,1),(-1,-1),[WHITE, LIGHT_GRAY]),
]))

content.append(cat_table)
content.append(Spacer(1, 0.5*cm))

# ================================================
# SECTION 4: REVENUE FORECAST
# ================================================
content.append(Paragraph("4. Revenue Forecast — Next 3 Months",
                          section_style))
content.append(Spacer(1, 0.2*cm))

content.append(Paragraph(
    "Based on Linear Regression model trained on 20 months of "
    "historical data. Time-based train/test split used to prevent "
    "data leakage.",
    body_style
))
content.append(Spacer(1, 0.2*cm))

forecast_table_data = [
    ['Month', 'Predicted Revenue (R$)', 'Model']
]
for _, row in forecast.iterrows():
    forecast_table_data.append([
        row['month'],
        f"R$ {row['predicted_revenue']:,.2f}",
        'Linear Regression'
    ])

forecast_table = Table(
    forecast_table_data,
    colWidths=[5*cm, 7*cm, 5*cm]
)
forecast_table.setStyle(TableStyle([
    ('BACKGROUND',   (0,0), (-1,0), DARK_BLUE),
    ('TEXTCOLOR',    (0,0), (-1,0), WHITE),
    ('FONTNAME',     (0,0), (-1,0), 'Helvetica-Bold'),
    ('FONTSIZE',     (0,0), (-1,0), 11),
    ('ALIGN',        (0,0), (-1,-1), 'CENTER'),
    ('FONTNAME',     (0,1), (-1,-1), 'Helvetica'),
    ('FONTSIZE',     (0,1), (-1,-1), 11),
    ('TOPPADDING',   (0,0), (-1,-1), 8),
    ('BOTTOMPADDING',(0,0), (-1,-1), 8),
    ('TEXTCOLOR',    (1,1), (1,-1), LIGHT_BLUE),
    ('FONTNAME',     (1,1), (1,-1), 'Helvetica-Bold'),
    ('GRID',         (0,0), (-1,-1), 0.5,
     colors.HexColor('#DDDDDD')),
    ('ROWBACKGROUNDS',(0,1),(-1,-1),[WHITE, LIGHT_GRAY]),
]))

content.append(forecast_table)
content.append(Spacer(1, 0.5*cm))

# ================================================
# FOOTER
# ================================================
content.append(HRFlowable(
    width="100%", thickness=1,
    color=LIGHT_BLUE, spaceAfter=8
))
content.append(Paragraph(
    "RetailX Corp — Confidential Business Report | "
    "Generated by AI-Powered Analytics Platform | "
    f"{datetime.now().strftime('%Y')}",
    ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=8,
        textColor=DARK_GRAY,
        alignment=TA_CENTER
    )
))

# ================================================
# BUILD PDF
# ================================================
doc.build(content)

print()
print("=" * 50)
print("✅ PDF REPORT GENERATED SUCCESSFULLY!")
print(f"   File: {output_file}")
print("   Sections:")
print("   1. Executive KPI Summary")
print("   2. Key Business Insights")
print("   3. Top 10 Product Categories")
print("   4. Revenue Forecast")
print("=" * 50)