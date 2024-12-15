#!/usr/bin/env python3
"""
In this task you will write the unit test for utils.access_nested_map
"""
import unittest
from utils import access_nested_map, get_json, memoize
from parameterized import parameterized
from typing import Mapping, Sequence, Any, Dict
from unittest.mock import patch


class TestAccessNestedMap(unittest.TestCase):
    """
    TestAccessNestedMap class that
    inherits from unittest.TestCase
    """
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {'b': 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)
    ])
    def test_access_nested_map(self, nested_map: Mapping, path: Sequence,
                               expected: Any) -> None:
        """
        TestAccessNestedMap.test_access_nested_map method to
        test that the method returns what it is supposed to
        """
        result = access_nested_map(nested_map, path)
        self.assertEqual(result, expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b"))
    ])
    def test_access_nested_map_exception(self, nested_map: Mapping,
                                         path: Sequence) -> None:
        """
        Implement TestAccessNestedMap.test_access_nested_map_exception.
        Use the assertRaises context manager to test that a KeyError is
        raised for the following inputs
        """
        with self.assertRaises(KeyError):
            access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    """
    class and implement the TestGetJson.test_get_json method
    to test that utils.get_json returns the expected result
    """
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False})
    ])
    @patch("requests.get")
    def test_get_json(self, url: str, test_payload: Dict, mock_get) -> None:
        """
        method to test that utils.get_json returns the expected result
        """
        mock_get.return_value.json.return_value = test_payload
        response = get_json(url)
        mock_get.assert_called_once_with(url)
        self.assertEqual(response, test_payload)


class TestMemoize(unittest.TestCase):
    """
    Implement the TestMemoize(unittest.TestCase)
    class with a test_memoize method
    """
    def test_memoize(self) -> None:
        """
        test_memoize method
        """
        class TestClass:
            """
            class TestClass
            """
            def a_method(self) -> None:
                """
                method return 42
                """
                return 42

            @memoize
            def a_property(self) -> None:
                """
                method return method
                """
                return self.a_method()

        with patch.object(TestClass, "a_method", return_value=42) as mocked:
            spec = TestClass()
            spec.a_property
            spec.a_property
            mocked.asset_called_once()


if __name__ == "__main__":
    unittest.main()
