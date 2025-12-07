from django.core.management.base import BaseCommand
from workflows.collectors import collect_forum
from workflows.tasks import save_items

class Command(BaseCommand):
    help = "Fetch Forum workflows for <country>"

    def add_arguments(self, parser):
        parser.add_argument("country", type=str)

    def handle(self, *args, **options):
        country = options["country"]

        self.stdout.write(f"Collecting Forum items for {country}...")
        items = collect_forum(country)

        save_items(items)

        self.stdout.write(self.style.SUCCESS(f"✔ Saved {len(items)} Forum items"))
