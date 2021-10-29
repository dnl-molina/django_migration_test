from __future__ import absolute_import, unicode_literals

import os

from django.core.management.commands.makemigrations import (
    Command as MakeMigrationsCommand,
)
from django.db.migrations.loader import MigrationLoader

APP_NAME = "api"


class Command(MakeMigrationsCommand):
    """Cause git conflict when branches have migrations conflict"""

    def handle(self, *app_labels, **options):
        super(Command, self).handle(*app_labels, **options)
        loader = MigrationLoader(None, ignore_no_migrations=True)
        list_migrations = [migration[1] for migration in loader.disk_migrations.keys() if migration[0] == APP_NAME]
        list_migrations.sort()

        current_migrations = None
        manifest_filename = f"migrations_{APP_NAME}.manifest"

        if os.path.exists(manifest_filename):
            with open(manifest_filename) as f:
                current_migrations = f.read()

        with open(manifest_filename, "w") as f:
            if current_migrations is None or current_migrations != "\n".join(list_migrations):
                for migration in list_migrations:
                    f.write(f"{migration}\n")

            graph = loader.graph
            leaf_nodes = graph.leaf_nodes(APP_NAME)
            if len(leaf_nodes) != 1:
                raise Exception("App {} has multiple leaf migrations!".format(APP_NAME))
                f.write("{}: {}\n".format(APP_NAME, leaf_nodes[0][1]))
