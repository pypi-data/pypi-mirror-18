from unittest import TestCase


class _ObjComparisonTestCase(TestCase):
    maxDiff = None  # Show diff output regardless of size

    def runTest(self):
        pass

_octc = _ObjComparisonTestCase()


def get_obj_comparison_message(a, b):
    """Retrieve a textual comparison of two objects.
    If the objects are of the same type and are compare-able,
    their differences will be identified in the message.
    """
    try:
        _octc.assertEqual(a, b)
    except AssertionError as exc:
        return exc.message
