from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy

from .models import Deportista, Medida

from openpyxl import Workbook
# from openpyxl.writer.excel import save_virtual_workbook
from openpyxl.styles import NamedStyle
from openpyxl.utils import get_column_letter


class ReporterTrainerExcelView(LoginRequiredMixin, View):

    def set_table(self, ws, row_next, mediciones):
        header = ['N°', 'Apellidos y Nombres', 'F. de Eval', 'Edad',
                  'Peso bruto (kg)', 'Estatura (cm)', 'IMC', 'Masa magra (kg)',
                  'Sum pliegues (mm)', '% Grasa corporal', 'Talla sentado',
                  'Indice citura cadera', 'TRC', 'SUBS', 'BICP', 'SPRI',
                  'SPRE', 'ABD', 'MSM', 'PANT', 'Endo', 'Meso', 'Ecto',
                  'Catacterización', 'Observación']

        for col in range(0, len(header)):
            _ = ws.cell(column=col + 1, row=row_next,
                        value='{0}'.format(header[col]))
        row_next += 1

        date_style = NamedStyle(name='date', number_format='DD/MM/YYYY')
        decimal_one_style = NamedStyle(name='decimal', number_format='0.0')

        for row in range(0, mediciones.count()):
            col = 1
            _ = ws.cell(column=col, row=row_next, value=row + 1)
            col += 1
            _ = ws.cell(column=col, row=row_next,
                        value='{0}'.format(mediciones[row]
                                           .deportista.get_full_name()))
            col += 1
            fecha_registro = ws.cell(column=col, row=row_next,
                                     value=mediciones[row].fecha_registro)
            fecha_registro.style = date_style
            col += 1
            _ = ws.cell(column=col, row=row_next,
                        value=mediciones[row].get_age_at_moment_metrics())
            col += 1
            _ = ws.cell(column=col, row=row_next,
                        value=mediciones[row].peso_bruto)
            col += 1
            _ = ws.cell(column=col, row=row_next,
                        value=mediciones[row].estatura)
            col += 1
            imc = ws.cell(column=col, row=row_next,
                          value=mediciones[row].get_indice_masa_corporal())
            imc.style = decimal_one_style
            col += 1
            masa_magra = ws.cell(column=col, row=row_next,
                                 value=mediciones[row].get_masa_magra())
            masa_magra.style = decimal_one_style
            col += 1
            suma_pliegues = ws.cell(column=col, row=row_next,
                                    value=mediciones[row].get_sum_pliegues())
            suma_pliegues.style = decimal_one_style
            col += 1
            grasa_corporal = ws.cell(column=col, row=row_next,
                                     value=mediciones[
                                         row].get_grasa_corporal())
            grasa_corporal.number_format = '0.0%'
            col += 1
            _ = ws.cell(column=col, row=row_next,
                        value=mediciones[row].talla_sentado)
            col += 1
            _ = ws.cell(column=col, row=row_next,
                        value=mediciones[row].triceps)
            col += 1
            _ = ws.cell(column=col, row=row_next,
                        value=mediciones[row].subescapular)
            col += 1
            _ = ws.cell(column=col, row=row_next,
                        value=mediciones[row].biceps)
            col += 1
            _ = ws.cell(column=col, row=row_next,
                        value=mediciones[row].suprailiaco)
            col += 1
            _ = ws.cell(column=col, row=row_next,
                        value=mediciones[row].supraespinal)
            col += 1
            _ = ws.cell(column=col, row=row_next,
                        value=mediciones[row].abdominales)
            col += 1
            _ = ws.cell(column=col, row=row_next,
                        value=mediciones[row].muslo_medio)
            col += 1
            _ = ws.cell(column=col, row=row_next,
                        value=mediciones[row].pliege_pierna)
            col += 1
            endo = ws.cell(column=col, row=row_next,
                           value=mediciones[row].get_endomorfismo())
            endo.style = decimal_one_style
            col += 1
            meso = ws.cell(column=col, row=row_next,
                           value=mediciones[row].get_mesomorfismo())
            meso.style = decimal_one_style
            col += 1
            ecto = ws.cell(column=col, row=row_next,
                           value=mediciones[row].get_ectomorfismo())
            ecto.style = decimal_one_style
            col += 1
            _ = ws.cell(column=col, row=row_next,
                        value='{0}'.format(
                            mediciones[row].get_caracterizacion()))
            col += 1
            _ = ws.cell(column=col,
                        row=row_next,
                        value='{0}'
                        .format(mediciones[row].get_observacion_masa_grasa()[1]
                                + '/' +
                                mediciones[
                                    row].get_observacion_masa_muscular()[1]))
            col += 1
            row_next += 1

        col_next = len(header) + 1

        _ = ws.cell(column=2, row=row_next+2, value='Observaciones:')
        text = 'Todos los nombres marcados con verde son deportistas ' \
               'catalogados como "madurador temprano" es decir son ' \
               'aquellos que ya han tenido su pico de maduración máximo y es ' \
               'probable que puedan tolerar el entrenamiento mejor que el ' \
               'resto, tener mejores tiempo de recuperación, mayor fuerza, ' \
               'resistencia, etc. Los deportistas en blanco son "maduradores ' \
               'normales" y probablemente tengan su pico de maduración en el ' \
               'transcurso del año. Finalmente, todos los marcados con ' \
               'amarillo son "maduradores tardíos" pero probablemente su pico ' \
               'se dará en más de un año. El indicador Talla//Edad nos ' \
               'muestra a los deportistas que presentan la relación de la ' \
               'talla para la edad y según esto son catalogados como ' \
               '"Altos", "Muy altos" o "Normales"'
        _ = ws.cell(column=6, row=row_next+2, value=text)
        _ = ws.cell(column=col_next-1, row=row_next+2,
                    value='Lic. José Miguel Chambi Enríquez')
        _ = ws.cell(column=col_next - 1, row=row_next + 3,
                    value='CNP : 5582')
        row_next += 4

        return row_next, col_next

    def set_header(self, ws, col_next, institucion, categoria):
        _ = ws.cell(column=col_next - 1, row=1,
                    value='{0}'.format(institucion).upper())
        _ = ws.cell(column=col_next - 1, row=2, value='AREA DE NUTRICIÓN ')

        ws.merge_cells('A3:' + get_column_letter(col_next-1)+str(3))
        ws.cell(column=1, row=3).value = \
            'INFORME DE EVALUACIÓN ANTROPOMÉTRICA - {0}'\
                .format(categoria).upper()

    def get(self, request, *args, **kwargs):
        deporte = request.GET.get('deporte', None)
        date_input = request.GET.get('date', None)
        if not deporte:
            return HttpResponseRedirect(reverse_lazy('reporter'))
        categoria = request.GET.get('categoria', None)
        if categoria:
            deportistas = Deportista.objects.filter(deporte=deporte,
                                                    categoria=categoria)
        else:
            deportistas = Deportista.objects.filter(deporte=deporte)

        if date_input:
            year, month = date_input.split('-')
            mediciones = Medida.objects.filter(
                deportista__in=deportistas,
                fecha_registro__month__gte=month,
                fecha_registro__year__gte=year
            ).order_by('-fecha_registro')
        else:
            mediciones = Medida.objects.filter(deportista__in=deportistas) \
                .order_by('-fecha_registro')

        institucion = mediciones.first().deportista.institucion
        categoria = mediciones.first().deportista.categoria

        wb = Workbook()
        ws = wb.active

        row_next = 7
        row_next, col_next = self.set_table(ws, row_next, mediciones)
        self.set_header(ws, col_next, institucion, categoria)

        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="users.xls"'
        wb.save(response)
        return response
