from django.core.management.base import BaseCommand
from ...models import Component           #ye dot lagake directory refernce karna mazedaar hai
# from datetime import datetime
from openpyxl import load_workbook


class Command(BaseCommand):
    help = 'Import components from Excel (trusted input)'

    def add_arguments(self, parser):
        parser.add_argument('excel_file', type=str)

    def handle(self, *args, **kwargs):
        excel_file_path = kwargs['excel_file']

        wb = load_workbook(excel_file_path)
        sheet = wb.active

        headers = [cell.value for cell in sheet[1]]

        for row in sheet.iter_rows(min_row=2, values_only=True):
            row_data = dict(zip(headers, row))

            category = row_data['category']
            name = row_data['name']
            quantity = int(row_data['quantity'])

            #date_strings = row_data['date_of_purchase'].split(',')
            #for date_str in date_strings:
               # purchase_date = datetime.strptime(
               #     date_str.strip(),
               #     "%Y-%m-%d"
               # ).date()

            Component.objects.update_or_create(
                comp_category=category,
                comp_name=name,
               #date_of_purchase=purchase_date,
                defaults={'comp_quantity_available': quantity}
            )

        self.stdout.write(self.style.SUCCESS("Excel import completed"))
