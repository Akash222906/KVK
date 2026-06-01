from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import io
import datetime

GREEN = colors.HexColor('#1a6b2e')
LIGHT_GREEN = colors.HexColor('#e8f5e9')
GOLD = colors.HexColor('#f9a825')
DARK = colors.HexColor('#212121')
GRAY = colors.HexColor('#757575')

def build_report(farmer_data, weather, recommendations, yield_pred, pest_risks, market_prices, schemes, advisory):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4,
                             rightMargin=2*cm, leftMargin=2*cm,
                             topMargin=2*cm, bottomMargin=2*cm)

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('Title', parent=styles['Normal'],
                                  fontSize=18, textColor=GREEN,
                                  alignment=TA_CENTER, fontName='Helvetica-Bold', spaceAfter=4)
    sub_style = ParagraphStyle('Sub', parent=styles['Normal'],
                                fontSize=10, textColor=GRAY,
                                alignment=TA_CENTER, spaceAfter=2)
    h2_style = ParagraphStyle('H2', parent=styles['Normal'],
                               fontSize=13, textColor=GREEN,
                               fontName='Helvetica-Bold', spaceAfter=6, spaceBefore=12)
    body_style = ParagraphStyle('Body', parent=styles['Normal'],
                                 fontSize=10, textColor=DARK, spaceAfter=4)

    story = []

    # Header
    story.append(Paragraph("KVK Krishak Seva — Farm Advisory Report", title_style))
    story.append(Paragraph("Krishi Vigyan Kendra · ICAR · Government of India", sub_style))
    story.append(Paragraph(f"Generated on: {datetime.datetime.now().strftime('%d %B %Y, %I:%M %p')}", sub_style))
    story.append(HRFlowable(width="100%", thickness=2, color=GREEN))
    story.append(Spacer(1, 0.3*cm))

    # Farmer Profile
    story.append(Paragraph("1. Farmer Profile", h2_style))
    profile_data = [
        ['Field', 'Details', 'Field', 'Details'],
        ['Farmer Name', farmer_data.get('name','—'), 'District', farmer_data.get('district','—')],
        ['Primary Crop', farmer_data.get('crop','—'), 'Farm Area', f"{farmer_data.get('area','—')} ha"],
        ['Soil Type', farmer_data.get('soil_type','Loamy'), 'Season', farmer_data.get('season','Kharif')],
        ['Soil N (kg/ha)', str(farmer_data.get('N','—')), 'Soil P (kg/ha)', str(farmer_data.get('P','—'))],
        ['Soil K (kg/ha)', str(farmer_data.get('K','—')), 'Soil pH', str(farmer_data.get('pH','—'))],
    ]
    t = Table(profile_data, colWidths=[4*cm, 6*cm, 4*cm, 6*cm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), GREEN),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('BACKGROUND', (0,1), (-1,-1), LIGHT_GREEN),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_GREEN]),
        ('GRID', (0,0), (-1,-1), 0.5, colors.lightgrey),
        ('FONTNAME', (0,1), (0,-1), 'Helvetica-Bold'),
        ('FONTNAME', (2,1), (2,-1), 'Helvetica-Bold'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t)

    # Weather
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph("2. Current Weather & 7-Day Forecast", h2_style))
    curr = weather.get('current', {})
    weather_data = [
        ['Temperature', 'Humidity', 'Rainfall', 'Wind Speed', 'Season', 'Conditions'],
        [f"{curr.get('temperature','—')}°C", f"{curr.get('humidity','—')}%",
         f"{curr.get('rainfall','—')} mm", f"{curr.get('wind_speed','—')} km/h",
         curr.get('season','—'), curr.get('conditions','—')],
    ]
    wt = Table(weather_data, colWidths=[3*cm, 3*cm, 3*cm, 3*cm, 3*cm, 3*cm])
    wt.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), GREEN),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('BACKGROUND', (0,1), (-1,1), LIGHT_GREEN),
        ('GRID', (0,0), (-1,-1), 0.5, colors.lightgrey),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(wt)

    # Forecast
    story.append(Spacer(1, 0.2*cm))
    forecast = weather.get('forecast', [])[:7]
    if forecast:
        fc_data = [['Day', 'Max Temp', 'Min Temp', 'Rain Chance', 'Conditions']]
        for f in forecast:
            fc_data.append([f['day'], f"{f['max_temp']}°C", f"{f['min_temp']}°C",
                             f"{f['rain_chance']}%", f['conditions']])
        fct = Table(fc_data, colWidths=[3*cm, 3.5*cm, 3.5*cm, 3.5*cm, 4.5*cm])
        fct.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#2e7d32')),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,-1), 9),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_GREEN]),
            ('GRID', (0,0), (-1,-1), 0.5, colors.lightgrey),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('PADDING', (0,0), (-1,-1), 5),
        ]))
        story.append(fct)

    # ML Recommendations
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph("3. AI Crop Recommendations (Machine Learning)", h2_style))
    rec_data = [['Rank', 'Recommended Crop', 'Confidence (%)', 'Suitability']]
    for i, r in enumerate(recommendations, 1):
        suitability = 'Excellent' if r['confidence'] > 60 else 'Good' if r['confidence'] > 35 else 'Fair'
        rec_data.append([str(i), r['crop'], f"{r['confidence']}%", suitability])
    rt = Table(rec_data, colWidths=[2*cm, 7*cm, 5*cm, 4*cm])
    rt.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), GREEN),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_GREEN]),
        ('GRID', (0,0), (-1,-1), 0.5, colors.lightgrey),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(rt)

    story.append(Spacer(1, 0.2*cm))
    story.append(Paragraph(f"<b>Predicted Yield for {farmer_data.get('crop','selected crop')}:</b> {yield_pred} quintal/hectare", body_style))

    # Pest Risk
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph("4. Pest & Disease Risk Assessment", h2_style))
    pest_data = [['Pest / Disease', 'Risk Level', 'Recommended Treatment']]
    for p in pest_risks:
        pest_data.append([p['pest'], p['risk'], p['treatment']])
    pt = Table(pest_data, colWidths=[5*cm, 3*cm, 10*cm])
    risk_colors = {'High': colors.HexColor('#ffcdd2'), 'Medium': colors.HexColor('#fff9c4'), 'Low': LIGHT_GREEN}
    pt.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), GREEN),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('GRID', (0,0), (-1,-1), 0.5, colors.lightgrey),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('PADDING', (0,0), (-1,-1), 5),
        ('WORDWRAP', (2,1), (2,-1), True),
    ]))
    story.append(pt)

    # Market Prices
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph("5. Current Market Prices", h2_style))
    mp_data = [['Crop', 'MSP (₹/quintal)', 'Market Price (₹/quintal)', 'Trend']]
    for mp in market_prices[:6]:
        mp_data.append([mp['crop'], str(mp['msp']) if mp['msp'] else 'No MSP',
                         f"₹{mp['market_price']}", mp['trend'].upper()])
    mpt = Table(mp_data, colWidths=[4*cm, 5*cm, 6*cm, 3*cm])
    mpt.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), GREEN),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_GREEN]),
        ('GRID', (0,0), (-1,-1), 0.5, colors.lightgrey),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(mpt)

    # Advisory
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph("6. Seasonal Advisory", h2_style))
    for tip in advisory:
        story.append(Paragraph(f"• {tip}", body_style))

    # Schemes
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph("7. Government Schemes You May Qualify For", h2_style))
    for s in schemes[:4]:
        story.append(Paragraph(f"<b>{s['name']} — {s['full_name']}</b>", body_style))
        story.append(Paragraph(f"Benefit: {s['benefit']}", body_style))
        story.append(Paragraph(f"Eligibility: {s['eligibility']}", body_style))
        story.append(Spacer(1, 0.15*cm))

    # Footer
    story.append(Spacer(1, 0.3*cm))
    story.append(HRFlowable(width="100%", thickness=1, color=GREEN))
    story.append(Paragraph("This report is generated by KVK Krishak Seva AI System. For further assistance, contact your nearest Krishi Vigyan Kendra.", sub_style))

    doc.build(story)
    buffer.seek(0)
    return buffer
