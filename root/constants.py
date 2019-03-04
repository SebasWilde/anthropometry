from openpyxl.styles import NamedStyle, Side, Border, Font, Alignment

SEXO = (
    ('H', 'Hombre'),
    ('M', 'Mujer'),
)

DECIMAL_FORMAT = '0.0'
PERCENTAGE_FORMAT = '0.0%'
MEDIUM_BORDER = Border(left=Side(style='medium'),
                       right=Side(style='medium'),
                       top=Side(style='medium'),
                       bottom=Side(style='medium'))

THIN_BORDER = Border(left=Side(style='thin'),
                       right=Side(style='thin'),
                       top=Side(style='thin'),
                       bottom=Side(style='thin'))

MEDIUM_BORDER_STYLE = NamedStyle(name='medium_border', border=MEDIUM_BORDER)

DEPORTISTA_STYLE = NamedStyle(name='deportista_style',
                              font=Font(name='Calibri', size=11, bold=True),
                              alignment=Alignment(horizontal='center'))

RESULTS_TITLE_STYLE = NamedStyle(name='results_title',
                                 font=Font(name='Arial Black', size=12, bold=True),
                                 alignment=Alignment(horizontal='center'))

ALIGN_MIDDLE = Alignment(horizontal='center', vertical='center')
