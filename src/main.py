import reportlab
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.enums import TA_CENTER
import os

BASE_HEIGHT = 132
BASE_WIDTH = 72

BASE_WIDTH_WITH_MARGIN = BASE_WIDTH + 4
ADJUSTED_FIRST_COLUMN_WIDTH = BASE_WIDTH * 0.67
ADJUSTED_SECOND_COLUMN_WIDTH = BASE_WIDTH * 0.33

HL_BOLD_WIDTH = 4
HL_THICK_WIDTH = 2
LINE_SEPARATOR_WIDTH = 0.5

def create_nutrition_facts(
    serving_size,
    calories,
    total_fat,
    saturated_fat,
    trans_fat,
    cholesterol,
    sodium,
    total_carb,
    dietary_fiber,
    total_sugars,
    added_sugars,
    protein,
    vitamin_d,
    calcium,
    iron,
    potassium
):
    # Register DejaVu Sans font for Cyrillic support
    pdfmetrics.registerFont(TTFont('DejaVuSans', '../fonts/DejaVuSans.ttf'))
    pdfmetrics.registerFont(TTFont('DejaVuSans-Bold', '../fonts/DejaVuSans-Bold.ttf'))
    
    # Create PDF with specified width (89mm)
    doc = SimpleDocTemplate(
        "label.pdf",
        pagesize=((BASE_WIDTH_WITH_MARGIN)*mm, BASE_HEIGHT*mm),
        rightMargin=0,
        leftMargin=0,
        topMargin=0,
        bottomMargin=0
    )

    header_text = '''Пищевая Ценность'''
    
    header_style = reportlab.lib.styles.ParagraphStyle(
        name='Header',
        fontName='DejaVuSans-Bold',
        fontSize=18,
        alignment=TA_CENTER,
    )
    
    header = reportlab.platypus.Paragraph(header_text, style=header_style)
    
    # Create separator line after header
    separator_data = [['']]
    separator_table = Table(separator_data, colWidths=[BASE_WIDTH*mm])
    separator_style = TableStyle([
        ('LINEBELOW', (0, 0), (0, 0), LINE_SEPARATOR_WIDTH, colors.gray),
        ('TOPPADDING', (0, 0), (0, 0), 0),
        ('BOTTOMPADDING', (0, 0), (0, 0), 1),
    ])
    separator_table.setStyle(separator_style)

    # Define daily recommended values (based on 2000 calorie diet)
    daily_values = {
        'total_fat': 78,  # g
        'saturated_fat': 20,  # g
        'trans_fat': 0,  # g (minimize intake)
        'cholesterol': 300,  # mg
        'sodium': 2300,  # mg
        'total_carb': 275,  # g
        'dietary_fiber': 28,  # g
        'total_sugars': 50,  # g (recommended limit)
        'added_sugars': 50,  # g
        'protein': 50,  # g
        'vitamin_d': 20,  # mcg 
        'calcium': 1300,  # mg
        'iron': 18,  # mg
        'potassium': 4700,  # mg
    }

    def cp(name, value):
        '''
        Calculate the percentage of the daily recommended value
        '''
        return f'{int(((float(value) if value else 0) / daily_values[name]) * 100)}%'
    
    # Define data for the table
    data = [
        [f'Размер порции', f'{serving_size}'],
        [f'Калории', f'{calories}'],
        ['', '% Дневной Нормы*'],
        [f'Всего жиров {total_fat}г', cp('total_fat', total_fat)],
        [f' Насыщенные жиры {saturated_fat}г', cp('saturated_fat', saturated_fat)],
        [f' Транс-жиры {trans_fat}г', ''],
        [f'Холестерин {cholesterol}мг', cp('cholesterol', cholesterol)],
        [f'Натрий {sodium}мг', cp('sodium', sodium)],
        [f'Всего углеводов {total_carb}г', cp('total_carb', total_carb)],
        [f' Пищевые волокна {dietary_fiber}г', cp('dietary_fiber', dietary_fiber)],
        [f' Всего сахаров {total_sugars}г', ''],
        [f'     Добавленные сахара {added_sugars}г', cp('added_sugars', added_sugars)],
        [f'Белки {protein}г', ''],
        [f'Витамин Д {vitamin_d}мкг', cp('vitamin_d', vitamin_d)],
        [f'Кальций {calcium}мг', cp('calcium', calcium)],
        [f'Железо {iron}мг', cp('iron', iron)],
        [f'Калий {potassium}мг', cp('potassium', potassium)]
    ]
    
    # Create table
    table = Table(data, colWidths=[ADJUSTED_FIRST_COLUMN_WIDTH*mm, ADJUSTED_SECOND_COLUMN_WIDTH*mm])
    
    # Define table style
    style = TableStyle([
        ('FONT', (0, 0), (-1, -1), 'DejaVuSans'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('FONTSIZE', (0, 0), (1, 0), 12), # Serving size
        ('FONTSIZE', (0, 1), (1, 1), 20), # Calories
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('LINEBELOW', (0, 0), (-1, -1), LINE_SEPARATOR_WIDTH, colors.gray), # Typical line
        ('LINEBELOW', (0, 0), (1, 0), HL_BOLD_WIDTH, colors.black),  # After serving size
        ('LINEBELOW', (0, 1), (1, 1), HL_THICK_WIDTH, colors.black),  # After calories
        ('LINEBELOW', (0, 12), (1, 12), HL_BOLD_WIDTH, colors.black),  # After protein
        ('LINEBELOW', (0, 16), (1, 16), HL_THICK_WIDTH, colors.black),  # After calcium
        ('BOTTOMPADDING', (0, 1), (-1, -1), 2),
        ('TOPPADDING', (0, 1), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 0), (1, 0), 8), # For serving size
        ('BOTTOMPADDING', (0, 1), (1, 1), 16), # For calories
        ('BOTTOMPADDING', (0, 12), (1, 12), 4), # For protein
        ('TOPPADDING', (0, 13), (1, 13), 5),
        ('FONT', (0, 0), (1, 3), 'DejaVuSans-Bold'),
        ('FONT', (0, 6), (1, 8), 'DejaVuSans-Bold'),
        ('FONT', (0, 12), (1, 12), 'DejaVuSans-Bold'),
        ('FONT', (1, 0), (1, 12), 'DejaVuSans-Bold'),
        ('FONTSIZE', (0, 3), (0, 3), 9),
        ('FONTSIZE', (0, 6), (0, 6), 9),
        ('FONTSIZE', (0, 12), (0, 12), 9),
    ])
    
    table.setStyle(style)

    footer_text = '''* % Дневной Нормы показывает, сколько питательных веществ содержится в порции продукта для ежедневной диеты. 2000 калорий в день используются для общих рекомендаций по питанию.'''
    
    footer_style = reportlab.lib.styles.ParagraphStyle(
        name='Footer',
        fontName='DejaVuSans',
        fontSize=7,
        leading=7,  # Уменьшаем межстрочный интервал (leading должен быть чуть больше fontSize)
    )
    
    footer = reportlab.platypus.Paragraph(footer_text, style=footer_style)
    spacer4px = reportlab.platypus.Spacer(1, 4)  # 4 pixels of vertical space

    # Build PDF
    doc.build([header, separator_table, table, spacer4px, footer])
    return "label.pdf"

# Example usage
if __name__ == "__main__":
    create_nutrition_facts(
        serving_size="100г",
        calories="250",
        total_fat="12",
        saturated_fat="3",
        trans_fat="0",
        cholesterol="30",
        sodium="470",
        total_carb="31",
        dietary_fiber="2",
        total_sugars="1",
        added_sugars="0",
        protein="5",
        vitamin_d="2",
        calcium="260",
        iron="1.2",
        potassium="35"
    )

