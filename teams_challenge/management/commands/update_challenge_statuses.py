# challenge/management/commands/update_challenge_statuses.py

from django.core.management.base import BaseCommand

from teams_challenge.services import update_challenge_statuses


class Command(BaseCommand):
    help = "Update challenge statuses"

    def handle(self, *args, **kwargs):
        update_challenge_statuses()

        self.stdout.write(
            self.style.SUCCESS(
                "Challenge statuses updated successfully."
            )
        )