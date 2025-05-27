import unittest
from utils import extract_title

class TestExtractTitle(unittest.TestCase):
    def test_extract_title(self):
        md = """
normal text

** bold **

### not this
# heading

_italic_
"""
        title = extract_title(md)
        self.assertEqual(title, "heading")

    def test_fail_title(self):
        md = """
normal text
## not title

#### not title neither

#Invalid title

that's all
"""
        with self.assertRaises(Exception) as context:
            title = extract_title(md)
        self.assertEqual(str(context.exception), "Markdown doesn't have a valid title")

