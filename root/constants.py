from openpyxl.styles import NamedStyle, Side, Border, Font, Alignment

SEXO = (
    ('H', 'Hombre'),
    ('M', 'Mujer'),
)

DATE_STYLE = NamedStyle(name='date', number_format='DD/MM/YYYY')
ONE_DECIMAL_STYLE = NamedStyle(name='decimal', number_format='0.0')
DECIMAL_FORMAT = '0.0'
PERCENTAGE_FORMAT = '0.0%'
MEDIUM_BORDER = Border(left=Side(style='medium'),
                       right=Side(style='medium'),
                       top=Side(style='medium'),
                       bottom=Side(style='medium'))

MEDIUM_BORDER_STYLE = NamedStyle(name='medium_border', border=MEDIUM_BORDER)

DEPORTISTA_STYLE = NamedStyle(name='deportista_style',
                              font=Font(name='Calibri', size=11, bold=True),
                              alignment=Alignment(horizontal='center'))

RESULTS_TITLE_STYLE = NamedStyle(name='results_title',
                                 font=Font(name='Arial Black', size=12, bold=True),
                                 alignment=Alignment(horizontal='center'))

ALIGN_MIDDLE = Alignment(horizontal='center', vertical='center')
