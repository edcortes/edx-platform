"""Tests running the delete_orphan command"""

from django.core.management import call_command
from contentstore.tests.test_orphan import TestOrphanBase


class TestDeleteOrphan(TestOrphanBase):
    """
    Tests for running the delete_orphan management command.
    Inherits from TestOrphan in order to use its setUp method.
    """
    def setUp(self):
        super(TestDeleteOrphan, self).setUp()
        self.course_id = self.course.id.to_deprecated_string()

    def test_delete_orphans_no_commit(self):
        call_command('delete_orphans', self.course_id)
        self.store.has_item(self.course.id.make_usage_key('html', 'html_different_parents'))
        self.store.has_item(self.course.id.make_usage_key('vertical', 'OrphanVert'))
        self.store.has_item(self.course.id.make_usage_key('chapter', 'OrphanChapter'))
        self.store.has_item(self.course.id.make_usage_key('html', 'OrphanHtml'))

    def test_delete_orphans_commit(self):
        call_command('delete_orphans', self.course_id, 'commit')

        # make sure this module wasn't deleted
        self.store.has_item(self.course.id.make_usage_key('html', 'html_different_parents'))

        # and make sure that these were
        self.assertFalse(self.store.has_item(self.course.id.make_usage_key('vertical', 'OrphanVert')))
        self.assertFalse(self.store.has_item(self.course.id.make_usage_key('chapter', 'OrphanChapter')))
        self.assertFalse(self.store.has_item(self.course.id.make_usage_key('html', 'OrphanHtml')))
