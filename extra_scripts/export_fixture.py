from django.core.management import call_command
import os
import django

# Setup Django (only needed if running outside manage.py context)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "teststudy.settings")
django.setup()

with open("data.json", "w", encoding="utf-8") as f:
    call_command("dumpdata", indent=2, stdout=f)