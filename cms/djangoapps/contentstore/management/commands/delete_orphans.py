"""Script for deleting orphans"""
from django.core.management.base import BaseCommand, CommandError
from contentstore.views.item import _delete_orphans
from opaque_keys.edx.keys import CourseKey
from opaque_keys import InvalidKeyError
from opaque_keys.edx.locations import SlashSeparatedCourseKey
from xmodule.modulestore import ModuleStoreEnum


class Command(BaseCommand):
    """Command for deleting orphans"""
    help = '''
    Delete orphans from a MongoDB backed course. Takes two arguments:
    <course_id>: the course id of the course whose orphans you want to delete
    |commit|: optional argument. If not provided, will not run task.
    '''

    def handle(self, *args, **options):
        if len(args) not in {1, 2}:
            raise CommandError("delete_orphans requires one or more arguments: <course_id> |commit|")

        try:
            course_key = CourseKey.from_string(args[0])
        except InvalidKeyError:
            course_key = SlashSeparatedCourseKey.from_deprecated_string(args[0])

        commit = False
        if len(args) == 2:
            commit = args[1] == 'commit'

        if commit:
            print 'Deleting orphans from the course....'

            deleted_items = _delete_orphans(
                course_key, ModuleStoreEnum.UserID.mgmt_command
            )

            print "Success! Deleted the following orphans from the course:"
            print "\n".join(deleted_items)
