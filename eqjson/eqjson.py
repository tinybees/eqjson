#!/usr/bin/env python3
# coding=utf-8

"""
@author: guoyanfeng
@software: PyCharm
@time: 18-3-30 下午1:32
"""

__all__ = ["EasyQueryjson"]


class EasyQueryjson(object):
    """
    通用的字符串语法类获取、更改、添加json的值

    暂时不支持根节点的添加操作
    """

    def __init__(self, json_obj):
        """
        通用的字符串语法类获取、更改、添加json的值

        暂时不支持根节点的添加操作
        Args:
            json_obj:python对象,如果是json则需要load后再传参
        Returns:

        """
        self.json_obj = json_obj

    def get_value(self, path):
        """
        通过通用的path寻址来获得对应的值
        Args:
            path
        Returns:

        """
        if "[" in path and "]" in path:
            return self._get_value_by_attr(path)
        else:
            return self._get_value(path)

    def change_value(self, path, value):
        """
        通过path和value来改变path对应的值
        Args:
            path
            value

        Returns:

        """
        json_value = self.get_value(path)
        cutted_path = path.rsplit('.', 1)[0]
        parent_json_value = self.get_value(cutted_path)

        # 对更改json的值做校验，防止改错
        if isinstance(parent_json_value, dict) or path == cutted_path:
            if self._is_value(json_value) and self._is_value(value):
                self._set_value(path, self._change_value_type(json_value, value))
            elif isinstance(value, list) and isinstance(json_value, list):
                self._set_value(path, value)
            elif isinstance(value, dict) and isinstance(json_value, dict):
                self._set_value(path, value)
            else:
                raise ValueError("更改的值{0}和模板中的值{1}的类型不一致,请检查!".format(type(value), type(json_value)))
        elif isinstance(parent_json_value, list):
            self._set_value(path, value)

    def remove_value(self, path):
        """
        通过path删除对应json节点的值
        Args:
            path

        Returns:

        """
        self._set_value(path, None)

    def append_value(self, path, value):
        """
        通过path和value来添加path对应的值
        Args:
            path
            value

        Returns:

        """
        json_value = self.get_value(path)
        if isinstance(json_value, list):
            json_value.append(value)
        elif isinstance(json_value, dict):
            self._append_entry(json_value, value)
        else:
            raise ValueError("基本类型值{0} {1}无法进行添加操作".format(json_value, type(json_value)))

    def _get_value(self, path, json_obj=None):
        """
        通过通用的path寻址来获得对应的值
        Args:
            path:
            json_obj: 提供的json doc 或者 self.json_obj
        Returns:

        """
        if path:
            splitted_path = str(path).split('.')
            return self._get_value_by_path(splitted_path, json_obj or self.json_obj)
        else:
            return json_obj or self.json_obj

    @staticmethod
    def _append_entry(json_value, value):
        """
        更新字典
        Args:
            json_value
            value

        Returns:

        """
        if isinstance(value, dict):
            json_value.update(value)
        else:
            raise ValueError("添加的值{0}和模板中的值{1}的类型不一致".format(type(value), type(json_value)))

    @staticmethod
    def _change_value_type(src_value, value):
        """
        把value的类型尽量更改为和src_value一样
        Args:
            src_value, value
        Returns:

        """
        try:
            return type(src_value)(value)
        except ValueError:
            return value

    def _set_value(self, path, value):
        """
        更改值的实际方法,更改值测试过了，删除值没有测试过
        Args:
            path
            value

        Returns:

        """
        if path.count('.') >= 1:
            cutted_path = path.rsplit('.', 1)
            obj = self.get_value(cutted_path[0])
            if isinstance(obj, dict):
                if value is None:
                    del obj[cutted_path[1]]
                else:
                    obj[cutted_path[1]] = value
            elif isinstance(obj, list):
                if cutted_path[1].isdigit():
                    if value is None:
                        obj.pop(int(cutted_path[1]))
                    else:
                        obj[int(cutted_path[1])] = value
                else:
                    raise ValueError("{0}类型是list，而{1}类型不是number，无法取值".format(type(obj), type(cutted_path[1])))

        else:
            if isinstance(self.json_obj, dict):
                if value is None:
                    del self.json_obj[path]
                else:
                    self.json_obj[path] = value
            elif isinstance(self.json_obj, list):
                if path.isdigit():
                    if value is None:
                        self.json_obj.pop(int(path))
                    else:
                        self.json_obj[int(path)] = value
                else:
                    raise ValueError("{0}类型是list，而{1}类型不是number，无法取值".format(type(self), type(path)))

    def _get_value_by_path(self, path, json_obj):
        """
        递归调用来取得对应path的值
        Args:
            path
            json_obj

        Returns:

        """
        if len(path) == 0:
            return json_obj
        e = path[0]
        json_obj = self._get_one_level_deeper(e, json_obj)
        path.remove(e)
        return self._get_value_by_path(path, json_obj)

    def _get_one_level_deeper(self, input_key, json_obj):
        """
        判断各种类型，通过inputkey，获得json_obj对应的值,支持json是字典或者是列表,列表直接通过数字访问
        Args:
            input_key:
            json_obj

        Returns:

        """

        if isinstance(json_obj, dict):
            return json_obj.get(input_key)
        elif isinstance(json_obj, list):
            if self._is_list_of_objects(json_obj):
                if input_key.isdigit():
                    # 如果是数字直接返回对应的值
                    return json_obj[int(input_key)]
                else:
                    # 如果不是数字返回列表中每项的key对应的值组成的列表
                    return self._get_values_from_list_by_key(input_key, json_obj)
            elif self._is_list_of_not_dict_objects(json_obj):
                if input_key.isdigit():
                    return json_obj[int(input_key)]
                else:
                    return json_obj
            else:
                return json_obj

    @staticmethod
    def _is_list_of_objects(input_list):
        """
        判断值得类型，判断是否是列表并且包含字典
        Args:
            input_list

        Returns:

        """
        if isinstance(input_list, list) and len(input_list) > 0:
            return True if isinstance(input_list[0], dict) else False

    def _is_list_of_not_dict_objects(self, input_list):
        """
        判断值得类型，判断是否是列表并且包含除字典外的类型
        Args:
            input_list

        Returns:

        """
        return not self._is_list_of_objects(input_list)

    @staticmethod
    def _is_value(value):
        return True if isinstance(value, (int, str, float, complex)) else False

    @staticmethod
    def _get_values_from_list_by_key(key, json_obj):
        """
        如果jsonobj是一个列表，那么返回类表中对应的每一个key的值
        Args:
            key:
            json_obj

        Returns:

        """
        result = []
        for e in json_obj:
            if isinstance(e, dict):
                result.append(e.get(key))
        return result

    def _get_val_from_unordered_list_by_unique_val(self, json_obj, path):
        """
        从无序的列表中，通过一个唯一值或者多个唯一值得到改列表中确定的节点
        Args:
            json_obj:需要查找的python对象
            path: 需要获取值的path路径，eg data.name[id=123]，data.name[id=123,path=test]
        Returns:
            返回由data.name[id=123]或者data.name[id=123,path=test]确定的节点
        """
        path = path.replace(" ", "")
        pre_path = path[:path.index("[")]
        pre_node_val = self._get_value(pre_path, json_obj)

        if isinstance(pre_node_val, list):
            attr_path = path[path.index("[") + 1:path.index("]")]
            if "," in attr_path:
                attr_pairs_value = [val.split("=") for val in attr_path.split(",")]
            else:
                attr_pairs_value = [attr_path.split("=")]
            for node in pre_node_val:
                for attr_name, attr_value in attr_pairs_value:
                    if str(node.get(attr_name)) != attr_value:
                        break
                else:
                    return node
            else:
                return None
        else:
            return pre_node_val

    def _get_value_by_attr(self, path):
        """
        通过path中的属性获取由属性确定的节点，目前每层节点能指定一个或多个属性，可以在多层节点上指定属性
        Args:
            path：需要获取值的path路径，eg data.name[id=123, path=test].name[id=1234].name
        Returns:
            返回由data.name[id=123, path=test].name[id=1234].name确定的值
        """
        path = path.replace(" ", "")
        json_obj = self.json_obj
        if path.count("]") == 1:
            left_path = path[:path.index("]") + 1]
            after_path = path[path.index("]") + 1:].strip(".")
            json_obj = self._get_val_from_unordered_list_by_unique_val(json_obj, left_path)
            return self._get_value(after_path, json_obj) if after_path else json_obj
        else:
            after_path = path
            for _ in range(after_path.count("]")):
                left_path = after_path[:after_path.index("]") + 1]
                json_obj = self._get_val_from_unordered_list_by_unique_val(json_obj, left_path)
                after_path = after_path[after_path.index("]") + 1:].strip(".")
            return self._get_value(after_path, json_obj) if after_path else json_obj
