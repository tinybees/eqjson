#!/usr/bin/env python3
# coding=utf-8

"""
@author: guoyanfeng
@software: PyCharm
@time: 2017-4-13 18:57
"""
import json
import unittest

from ejson import Ejson


class TestEjson1(unittest.TestCase):
    """
    ejson 单测第一种情况，以大括号开始
    """

    @classmethod
    def setUpClass(cls):
        with open("json_test_1.json") as f:
            json_doc = json.load(f)
        cls.ejson_obj = Ejson(json_doc)

    def test_101_get_first_tier(self, ):
        """

        Args:
            self,
        Returns:

        """
        val = self.ejson_obj.get_value_from_path("id")
        self.assertEqual(val, 1123123812831823)

    def test_102_get_second_tier(self, ):
        """

        Args:
            self,
        Returns:

        """
        val = self.ejson_obj.get_value_from_path("object.name")
        self.assertEqual(val, "myLittleObject")

    def test_103_get_third_tier(self, ):
        """

        Args:
            self,
        Returns:

        """
        val = self.ejson_obj.get_value_from_path("object.valueAsString.0")
        self.assertEqual(val, "one")

    def test_104_get_third_tier_list0_dict_value(self, ):
        """

        Args:
            self,
        Returns:

        """
        val = self.ejson_obj.get_value_from_path("object.value.1.key")
        self.assertEqual(val, "value2")

    def test_105_get_list_all_key_value(self, ):
        """

        Args:
            self,
        Returns:

        """
        val = self.ejson_obj.get_value_from_path("object.value.key")
        self.assertEqual(val, ["value1", "value2", "value3"])

    def test_106_change_first_tier(self, ):
        """

        Args:
            self,
        Returns:

        """
        self.ejson_obj.change_value("id", "123456")
        val = self.ejson_obj.get_value_from_path("id")
        self.assertEqual(val, 123456)

    def test_107_change_second_tier(self, ):
        """

        Args:
            self,
        Returns:

        """
        self.ejson_obj.change_value("object.name", "updatename")
        val = self.ejson_obj.get_value_from_path("object.name")
        self.assertEqual(val, "updatename")

    def test_107_change_list_value(self, ):
        """

        Args:
            self,
        Returns:

        """
        self.ejson_obj.change_value("object.value.2", ["five", "four"])
        val = self.ejson_obj.get_value_from_path("object.value.2")
        self.assertEqual(val, ["five", "four"])


class TestEjson2(unittest.TestCase):
    """
    ejson 单测第二种情况，以列表开始
    """

    @classmethod
    def setUpClass(cls):
        with open("json_test_2.json") as f:
            json_doc = json.load(f)
        cls.ejson_obj = Ejson(json_doc)

    def test_101_get_first_tier(self, ):
        """

        Args:
            self,
        Returns:

        """
        val = self.ejson_obj.get_value_from_path("1.id")
        self.assertEqual(val, 123456)

    def test_102_get_second_tier(self, ):
        """

        Args:
            self,
        Returns:

        """
        val = self.ejson_obj.get_value_from_path("0.object.name")
        self.assertEqual(val, "myLittleObject")

    def test_103_get_third_tier(self, ):
        """

        Args:
            self,
        Returns:

        """
        val = self.ejson_obj.get_value_from_path("1.object.valueAsString.0")
        self.assertEqual(val, "one")

    def test_104_get_third_tier_list0_dict_value(self, ):
        """

        Args:
            self,
        Returns:

        """
        val = self.ejson_obj.get_value_from_path("1.object.value.1.key")
        self.assertEqual(val, "value2")

    def test_105_get_list_all_key_value(self, ):
        """

        Args:
            self,
        Returns:

        """
        val = self.ejson_obj.get_value_from_path("0.object.value.key")
        self.assertEqual(val, ["value1", "value2", "value3"])

    def test_106_change_first_tier(self, ):
        """

        Args:
            self,
        Returns:

        """
        self.ejson_obj.change_value("0.id", "123456")
        val = self.ejson_obj.get_value_from_path("0.id")
        self.assertEqual(val, 123456)

    def test_107_change_second_tier(self, ):
        """

        Args:
            self,
        Returns:

        """
        self.ejson_obj.change_value("0.object.name", "updatename")
        val = self.ejson_obj.get_value_from_path("0.object.name")
        self.assertEqual(val, "updatename")

    def test_107_change_list_value(self, ):
        """

        Args:
            self,
        Returns:

        """
        self.ejson_obj.change_value("1.object.value.2", ["five", "four"])
        val = self.ejson_obj.get_value_from_path("1.object.value.2")
        self.assertEqual(val, ["five", "four"])


class TestEjson3(unittest.TestCase):
    """
    ejson 单测第二种情况，以列表开始
    """

    @classmethod
    def setUpClass(cls):
        with open("json_test_3.json") as f:
            json_doc = json.load(f)
        cls.ejson_obj = Ejson(json_doc)

    def test_101_get_first_tier(self, ):
        """

        Args:
            self,
        Returns:

        """
        val = self.ejson_obj.get_value_from_path("[id=123456]")
        self.assertEqual(val["id"], 123456)

    def test_102_get_second_tier(self, ):
        """

        Args:
            self,
        Returns:

        """
        val = self.ejson_obj.get_value_from_path("[id=123456].object.value")
        self.assertEqual(len(val), 3)

    def test_103_get_third_tier(self, ):
        """

        Args:
            self,
        Returns:

        """
        val = self.ejson_obj.get_value_from_path("[id=123456].object.value[key1=value1]")
        self.assertEqual(len(val), 3)

    def test_104_get_third_tier_list0_dict_value(self, ):
        """

        Args:
            self,
        Returns:

        """
        val = self.ejson_obj.get_value_from_path("[id=123456].object.value[key1=value1].key3")
        self.assertEqual(val, "value3")

    def test_105_get_list_all_key_value(self, ):
        """

        Args:
            self,
        Returns:

        """
        val = self.ejson_obj.get_value_from_path("1.object.value[key11=value11].key33")
        self.assertEqual(val, "value33")

    def test_106_get_value_by_mul_attr(self, ):
        """

        Args:
            self,
        Returns:

        """
        val = self.ejson_obj.get_value_from_path("1.object.value[key11=value11,key22=value22, key33=value33].key33")
        self.assertEqual(val, "value33")

    def test_107_get_list_by_mul_attr(self, ):
        """

        Args:
            self,
        Returns:

        """
        val = self.ejson_obj.get_value_from_path("1.object.value[key11=value11,key22=value22, key33=value33]")
        self.assertEqual(len(val), 3)

    def test_108_not_found_by_mul_attr(self, ):
        """

        Args:
            self,
        Returns:

        """
        val = self.ejson_obj.get_value_from_path("1.object.value[key11=value11,key22=value2, key33=value33]")
        self.assertIs(val, None)


if __name__ == '__main__':
    # unittest.main(verbosity=2)
    test_load = unittest.TestLoader()
    suite = test_load.loadTestsFromTestCase(TestEjson1)
    suite.addTest(test_load.loadTestsFromTestCase(TestEjson2))
    suite.addTest(test_load.loadTestsFromTestCase(TestEjson3))
    unittest.TextTestRunner(verbosity=2).run(suite)
