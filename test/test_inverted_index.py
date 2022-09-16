import os
import unittest

from app.api import build_inverted_index, get_inverted_index
from app.helpers import update_index
from app.inverted_index import InvertedIndex


class TestInvertedIndex(unittest.TestCase):

    def setUp(self):
        self.test_raw_string = "Python Python is an interpreted, high-level, general-purpose programming language"
        self.test_raw_input = """
        Python Python is an interpreted, high-level, general-purpose programming language
        Java Java is a general-purpose programming language
        C++ C++ is a high-level, general-purpose programming language"""

        self.test_raw_index = {
            1: "Python Python is an interpreted, high-level, general-purpose programming language",
            2: "Java Java is a general-purpose programming language",
            3: "C++ C++ is a high-level, general-purpose programming language"
        }

        self.should_be_inverted_index = {
            'Python': {1},
            'is': {1, 2, 3},
            'an': {1},
            'interpreted,': {1},
            'high-level,': {1, 3},
            'general-purpose': {1, 2, 3},
            'programming': {1, 2, 3},
            'language': {1, 2, 3},
            'Java': {2},
            'a': {2, 3},
            'C++': {3},
        }

    def test_can_create_inverted_index(self):
        input_dict = self.test_raw_index
        should_be_output = self.should_be_inverted_index

        output = get_inverted_index(input_dict)

        self.assertTrue(should_be_output == output)

    def test_can_update_empty_index(self):
        input_index = {}
        input_ws = {"a", "b", "c"}
        input_k = 1

        should_be_result = {"a": {1}, "b": {1}, "c": {1}}
        result = update_index(input_ws, input_k, input_index)

        self.assertTrue(should_be_result == result)

    def test_can_update_non_empty_index(self):
        input_index = {"a": {5}, "b": {6}, "c": {7}}
        input_ws = {"a", "b", "c"}
        input_k = 1

        should_be_output = {"a": {1, 5}, "b": {1, 6}, "c": {1, 7}}
        output = update_index(input_ws, input_k, input_index)

        self.assertTrue(should_be_output == output)

    def test_can_build_inverted_index_type(self):
        input_dict = self.test_raw_index
        output = build_inverted_index(input_dict)

        self.assertIsInstance(output, InvertedIndex)

    def test_inverted_index_object_can_query(self):
        test_qs = [
            (['Python'], {1}),
            (['Python', 'C++'], {}),
            (['Java', 'is'], {2}),
            (['is', 'a', 'general-purpose', 'programming', 'language'], {2, 3})
        ]

        input_dict = self.test_raw_index
        index_obj = build_inverted_index(input_dict)

        for query, should_be_result in test_qs:
            result = index_obj.query(query)

            self.assertSetEqual(set(should_be_result), result)

    def test_inverted_index_object_can_dump_data(self):
        input_dict = self.test_raw_index
        index_obj = build_inverted_index(input_dict)

        index_obj.dump("output")

    def test_inverted_index_object_can_build_clone_from_dumped_index(self):
        input_dict = self.test_raw_index
        index_obj_src = build_inverted_index(input_dict)
        index_obj_src.dump("output")
        index_obj_dst = index_obj_src.load("output")
        os.remove("output")
        self.assertIsInstance(index_obj_dst, InvertedIndex)
        self.assertNotEqual(index_obj_dst, InvertedIndex)

    def test_inverted_index_object_dumps_and_restores_index(self):
        input_dict = self.test_raw_index
        index_obj_src = build_inverted_index(input_dict)
        index_obj_src.dump("output")
        index_obj_dst = index_obj_src.load("output")
        os.remove("output")

        self.assertTrue(index_obj_src.index(), index_obj_dst.index())


if __name__ == '__main__':
    unittest.main()
