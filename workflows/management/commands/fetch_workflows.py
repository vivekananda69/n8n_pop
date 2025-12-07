from django.core.management.base import BaseCommand
from workflows.collectors import (
    collect_youtube_for_country,
    collect_forum,
    collect_trends,
)
from workflows.tasks import save_items

class Command(BaseCommand):
    help = "Fetch ALL workflows (YouTube, Forum, Trends) for US + IN"

    def handle(self, *args, **options):
        self.stdout.write("🚀 Starting full workflow collection...")

        all_items = []

        for country in ["US", "IN"]:
            self.stdout.write(f"\n🌎 Collecting for {country}")

            yt = collect_youtube_for_country(country)
            self.stdout.write(f"✔ YouTube: {len(yt)} items")
            all_items += yt

            fr = collect_forum(country)
            self.stdout.write(f"✔ Forum: {len(fr)} items")
            all_items += fr

            tr = collect_trends(country)
            self.stdout.write(f"✔ Trends: {len(tr)} items")
            all_items += tr

        self.stdout.write("\n💾 Saving to database...")
        save_items(all_items)

        self.stdout.write(self.style.SUCCESS(f"🎉 Done! Saved total {len(all_items)} workflows"))
