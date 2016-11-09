from django.test import TestCase

from .models import Post

class PostTests(TestCase):

    def test_str(self):
        test_title = Post(title="Sample Title")
        self.assertEquals(str(test_title),"Sample Title")


