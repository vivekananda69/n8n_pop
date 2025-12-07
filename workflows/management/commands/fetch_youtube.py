from django.core.management.base import BaseCommand
from workflows.collectors import collect_youtube_for_country
from workflows.tasks import save_items


class Command(BaseCommand):
    help = "Fetch YouTube workflows for <country>"

    def add_arguments(self, parser):
        parser.add_argument("country", type=str)

    def handle(self, *args, **options):
        country = options["country"]
        self.stdout.write(f"Collecting YouTube for {country}...")

        items = collect_youtube_for_country(country)
        save_items(items, "YouTube", country)

        self.stdout.write(self.style.SUCCESS(f"Saved {len(items)} youtube items"))
