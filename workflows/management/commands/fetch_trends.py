from django.core.management.base import BaseCommand
from workflows.collectors import collect_trends
from workflows.tasks import save_items

class Command(BaseCommand):
    help = "Fetch Google Trends workflows for <country>"

    def add_arguments(self, parser):
        parser.add_argument("country", type=str)

    def handle(self, *args, **options):
        country = options["country"]
        self.stdout.write(f"Collecting Trends for {country}")

        items = collect_trends(country)
        save_items(items, "Trends", country)

        self.stdout.write(self.style.SUCCESS(f"Saved {len(items)} trends items"))
