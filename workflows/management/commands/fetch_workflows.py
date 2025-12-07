from django.core.management.base import BaseCommand
from workflows.collectors import (
    collect_youtube_for_country,
    collect_forum,
    collect_trends,
)
from workflows.tasks import save_items


class Command(BaseCommand):
    help = "Fetch workflows from YouTube, Forum, and Google Trends for US + IN"

    def handle(self, *args, **options):
        self.stdout.write("🚀 Starting workflow collection...")

        total = 0

        for country in ["US", "IN"]:
            self.stdout.write(f"🌎 Country = {country}")

            self.stdout.write("  🎥 YouTube...")
            yt = collect_youtube_for_country(country)
            save_items(yt, "YouTube", country)
            self.stdout.write(f"    → {len(yt)} youtube items")
            total += len(yt)

            self.stdout.write("  💬 Forum...")
            fr = collect_forum(country)
            save_items(fr, "Forum", country)
            self.stdout.write(f"    → {len(fr)} forum items")
            total += len(fr)

            self.stdout.write("  📈 Google Trends...")
            tr = collect_trends(country)
            save_items(tr, "GoogleTrends", country)
            self.stdout.write(f"    → {len(tr)} trends items")
            total += len(tr)

        self.stdout.write(self.style.SUCCESS(f"✔ Stored {total} workflows"))
