from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from LittleLemon.LittleLemonAPI.utils import GroupEnum


class Command(BaseCommand):
    help = "Seed groups with initial data"

    def handle(self, *args, **kwargs):
        print("Seeding groups...")

        for group in GroupEnum:
            group_name = group.value
            _, created = Group.objects.get_or_create(name=group_name)
            if created:
                print(f"Created group: {group_name}")
            else:
                print(f"Group already exists: {group_name}")

        self.stdout.write(self.style.SUCCESS("Seeding completed!"))
