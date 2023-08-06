from __future__ import unicode_literals
from django.db import reset_queries, transaction, router
from reversion.models import Revision, Version
from reversion.management.commands import BaseRevisionCommand
from reversion.revisions import create_revision, set_comment, add_to_revision


class Command(BaseRevisionCommand):

    help = "Creates initial revisions for a given app [and model]."

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        parser.add_argument(
            "--comment",
            action="store",
            default="Initial version.",
            help="Specify the comment to add to the revisions. Defaults to 'Initial version'.")
        parser.add_argument(
            "--batch-size",
            action="store",
            type=int,
            default=500,
            help="For large sets of data, revisions will be populated in batches. Defaults to 500.",
        )

    def handle(self, *app_labels, **options):
        verbosity = getattr(options, "verbosity", 0)
        using = getattr(options, "using", None)
        model_db = getattr(options, "model_db", None)
        comment = getattr(options, "comment", "Initial version.")
        batch_size = getattr(options, "batch_size", 500)
        # Create revisions.
        using = using or router.db_for_write(Revision)
        with transaction.atomic(using=using):
            for model in self.get_models(options):
                # Check all models for empty revisions.
                if verbosity >= 1:
                    self.stdout.write("Creating revisions for {name}".format(
                        name=model._meta.verbose_name,
                    ))
                created_count = 0
                # _safe_subquery does not work in Django 1.7
                # So we replace it with this query for now
                live_objs = model._default_manager.db_manager(model_db).all()
                # Save all the versions.
                ids = list(live_objs.values_list("pk", flat=True).order_by())
                total = len(ids)
                for i in range(0, total, batch_size):
                    chunked_ids = ids[i:i+batch_size]
                    objects = live_objs.in_bulk(chunked_ids)
                    for obj in objects.values():
                        with create_revision(using=using):
                            set_comment(comment)
                            add_to_revision(obj, model_db=model_db)
                        created_count += 1
                    reset_queries()
                    if verbosity >= 2:
                        self.stdout.write("- Created {created_count} / {total}".format(
                            created_count=created_count,
                            total=total,
                        ))
                # Print out a message, if feeling verbose.
                if verbosity >= 1:
                    self.stdout.write("- Created {total} / {total}".format(
                        total=total,
                    ))
