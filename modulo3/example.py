from geraldo import Report, DetailBand, ObjectValue
from geraldo.utils import cm
from geraldo.generators import PDFGenerator
names = ['Mychelle', 'Leticia', 'Tarsila', 'Marta', 'Vera', 'Leni']
class MyReport(Report):
     class band_detail(DetailBand):

         height=0.7*cm
         elements=[
             ObjectValue(attribute_name='capitalize'),
             ]
report = MyReport(queryset=names)
report.generate_by(PDFGenerator, filename='female-names.pdf')

#sadasdasdasd
