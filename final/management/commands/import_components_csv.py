import csv
from django.core.management.base import BaseCommand
from base.models import Component  # Replace with your actual app name
from datetime import datetime

class Command(BaseCommand):
    help = 'Import components from CSV (supports multiple dates per row)'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **kwargs):
        csv_file_path = kwargs['csv_file']
        try:
            with open(csv_file_path, 'r', encoding='utf-8', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    try:
                        category = row['category'].strip()
                        name = row['name'].strip()
                        quantity = self.safe_int(row['quantity'])
                        date_strings = row['date_of_purchase'].split(',')

                        for date_str in date_strings:
                            purchase_date = self.parse_date(date_str)
                            if purchase_date:
                                obj, created = Component.objects.update_or_create(
                                    category=category,
                                    name=name,
                                    date_of_purchase=purchase_date,
                                    defaults={'quantity': quantity}
                                )
                                if created:
                                    self.stdout.write(self.style.SUCCESS(f"Imported: {name} on {purchase_date}"))
                                else:
                                    self.stdout.write(self.style.WARNING(f"Updated: {name} on {purchase_date}"))
                            else:
                                self.stdout.write(self.style.WARNING(f"Skipped invalid date: {date_str} in row: {row}"))
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f"Error importing row: {row}"))
                        self.stdout.write(self.style.ERROR(str(e)))

            self.stdout.write(self.style.SUCCESS('All valid components imported!'))

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR('CSV file not found. Ensure components_2.csv exists in the root directory.'))

    def parse_date(self, value):
        if not value:
            return None
        value = value.strip()
        for fmt in ("%Y-%m-%d", "%d.%m.%Y"):
            try:
                return datetime.strptime(value, fmt).date()
            except ValueError:
                continue
        return None

    def safe_int(self, value):
        try:
            return int(float(value.strip()))
        except (ValueError, AttributeError):
            return 0
