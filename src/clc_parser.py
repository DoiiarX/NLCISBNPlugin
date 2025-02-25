import json
import re
import os
from .data_wrapper import data as tree

class Parser:
    # 不含复分信息的正则表达式
    # 粗略判断，允许非法的如M、TZ等大类目
    REGEX_CLC_CLASSIC = r'[A-Z]{2}\d{0,3}'
    # 仅允许第五版规定的大类目
    REGEX_CLC_CLASSIC_V5_STRICT = r'(?:[A-K]|[N-V]|X|Z)[A-Z]?\d{0,3}'

    def __init__(self):
        self.clean_regex = self.generate_clean_regex()
        # 加载数据文件
        # 注意: 实际使用时需要有一个data.json文件
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        self.clc_tree_regex = self.load_tree_json(tree)
        self.clc_info = self.load_clc_info(tree)

    # 单例模式
    _instance = None
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @classmethod
    def parse(cls, s):
        """
        解析中图分类号，获得三级信息
        
        :param s: 复杂的图书中图分类号信息
        :return: 可能有多个结果的字典
        """
        instance = cls.get_instance()
        
        result = {}
        s = s.replace('；', ';')
        codes = s.split(';')
        for code in codes:
            code = code.strip()
            if not code:
                continue
            
            result[code] = instance.parse_code(code)
        
        return result

    @classmethod
    def get_clc_info_by_code(cls, code):
        """
        通过一二三级中图分类号，查询相关信息
        
        :param code: 一到三级单个中图分类号
        :return: 分类信息字典
        """
        instance = cls.get_instance()
        return instance.clc_info.get(code, {})

    def parse_code(self, code):
        """
        解析单个中图分类号
        
        :param code: 单个中图分类号
        :return: 一到三级中图分类号的列表
        """
        code = self.clean(code)
        if not code:
            return []
        
        # 先解析第一级
        first_code = self.run_sub_regex_on_code(code, self.clc_tree_regex)
        if first_code is False:
            return []
        
        # 再解析第二级
        second_code = self.run_sub_regex_on_code(
            code, 
            self.clc_tree_regex.get(first_code, {}).get('children', {})
        )
        if second_code is False:
            return [first_code]
        
        # 再解析第三级
        third_code = self.run_sub_regex_on_code(
            code,
            self.clc_tree_regex.get(first_code, {}).get('children', {}).get(second_code, {}).get('children', {})
        )
        if third_code is False:
            return [first_code, second_code]
        
        return [first_code, second_code, third_code]

    @staticmethod
    def run_sub_regex_on_code(code, regex_tree=None):
        """
        传入规则树，扫描下一级规则，传入中图分类号，找到最先匹配项
        成功返回中图分类号,失败则返回False
        """
        if not regex_tree:
            return False
        
        for key, value in regex_tree.items():
            if re.search(value['regex'], code):
                return key
        
        return False

    def clean(self, s):
        """
        清洗中图分类号，输出最简单格式
        
        :param s: 复杂格式的单个中图分类号
        :return: 清洗后的中图分类号
        """
        s = s.strip()
        match = re.search(self.clean_regex, s)
        return match.group(1) if match else ''

    def load_clc_info(self, tree):
        """
        加载中图分类号对应的信息，到三级为止
        
        :param tree: 从json加载的中图分类树数据
        :return: 中图分类信息字典
        """
        result = {}
        
        for first in tree:
            first_code = first['code']
            first_name = first['name']
            
            for second in first['children']:
                second_code = second['code']
                second_name = second['name']
                
                for third in second['children']:
                    third_code = third['code']
                    third_name = third['name']
                    
                    result[third_code] = {
                        'code': third_code,
                        'name': third_name,
                        'path': [first_code, second_code, third_code],
                        'namePath': [first_name, second_name, third_name]
                    }
                
                result[second_code] = {
                    'code': second_code,
                    'name': second_name,
                    'path': [first_code, second_code],
                    'namePath': [first_name, second_name]
                }
            
            result[first_code] = {
                'code': first_code,
                'name': first_name,
                'path': [first_code],
                'namePath': [first_name]
            }
        
        return result

    def load_tree_json(self, tree):
        """
        加载资源文件，获得中图分类树状结构
        
        :param tree: 从json加载的中图分类树数据
        :return: 中图分类正则表达式规则树
        """
        result = {}
        
        for first in tree:  # 一级分类
            first_code = first['code']
            first_value = {
                'regex': self.build_regex_from_codes([first_code]),
                'children': {}
            }
            
            for second in first['children']:  # 第二级
                second_code = second['code']
                sub_codes = self.get_children_codes_recursively(second)
                second_value = {
                    'regex': self.build_regex_from_codes(sub_codes),
                    'children': {}
                }
                
                for third in second['children']:  # 第三级
                    third_code = third['code']
                    sub_codes = self.get_children_codes_recursively(third)
                    third_value = {
                        'regex': self.build_regex_from_codes(sub_codes),
                        'children': {}
                    }
                    second_value['children'][third_code] = third_value
                
                first_value['children'][second_code] = second_value
            
            result[first_code] = first_value
        
        return result

    def build_regex_from_codes(self, codes):
        """
        通过多个中图分类号，创建识别的正则函数
        
        :param codes: 多个中图分类号
        :return: 正则表达式字符串
        """
        codes_str = '|'.join(codes)
        codes_regex = r'^' + codes_str.replace('.', r'\.').replace('+', r'[+]').replace('-', r'[\-]')
        return codes_regex

    def get_children_codes_recursively(self, node):
        """
        通过树状结构，遍历加载所有的子孙节点中图分类号
        
        :param node: 树节点
        :return: 中图分类号列表
        """
        result = self.parse_clc_code_str(node['code'])
        
        for child in node.get('children', []):
            result.extend(self.get_children_codes_recursively(child))
        
        result.reverse()
        return result

    def parse_clc_code_str(self, s):
        """
        解析json中的分类号，先做清洗，遇到/字符就展开，返回处理后的所有中图分类号
        
        :param s: 未展开的中图分类号
        :return: 展开后的中图分类数组
        """
        s = s.replace('[', '').replace(']', '').replace('{', '').replace('}', '')
        
        result = []
        # X922.3/.7 这个格式
        regex1 = r'^(.+?)\.(\d+)\/\.(\d+)(.*?)$'
        # T-013/-017 这个格式
        regex2 = r'^(.+?)[\-](\d+)\/[\-](\d+)(.*?)$'
        # Z813/817 这个格式
        regex3 = r'^(.+?)(\d+)\/(\d+)(.*?)$'
        
        match1 = re.match(regex1, s)
        match2 = re.match(regex2, s)
        match3 = re.match(regex3, s)
        
        if match1:
            prefix = match1.group(1)
            start = int(match1.group(2))
            end = int(match1.group(3))
            postfix = match1.group(4)
            
            for i in range(start, end + 1):
                result.append(f"{prefix}.{i}{postfix}")
        
        elif match2:
            prefix = match2.group(1)
            start = int(match2.group(2))
            end = int(match2.group(3))
            postfix = match2.group(4)
            
            for i in range(start, end + 1):
                result.append(f"{prefix}-{i}{postfix}")
        
        elif match3:
            prefix = match3.group(1)
            start = int(match3.group(2))
            end = int(match3.group(3))
            postfix = match3.group(4)
            
            for i in range(start, end + 1):
                result.append(f"{prefix}{i}{postfix}")
        
        else:
            result = [s]
        
        return result

    def generate_clean_regex(self):
        """
        输出含复分信息的正则表达式
        
        :return: 正则表达式
        """
        # 可以处理粗略的分类信息
        regex_clc_simple = r'\[?(' + self.REGEX_CLC_CLASSIC_V5_STRICT + r'(?:\/\d{1,3})?a?(?:[.\-=+]\d{1,3}|\(\d{1,3}\)|"\d{1,3}"|<\d{1,3}>)*)\]?'
        # 可以处理形如 {停用分类号}<现用分类号> 的分类信息
        regex_clc_abandoned_included = r'{?' + regex_clc_simple + r'(?:}<(?:' + regex_clc_simple + r')>)?'
        # 可以处理含组合助记符的分类信息
        regex_clc_complete = regex_clc_abandoned_included + r'(?:[:+](?:' + regex_clc_abandoned_included + r'))*'
        
        return regex_clc_complete


# 使用示例
if __name__ == "__main__":
    test_codes = """
        A
        O1-62
        J523.2"17"+3:G5
        TP312
        K837.125.6(202)+R173:G25a
        [X-019]
        F08:G40-054
        K876.3=49
        G49a
        K825.2；E251-53
        I287.8
        I712.45
        I611.65
        K854-53
        F0-0
        {D922.59} 
    """
    
    for code in test_codes.strip().split('\n'):
        code = code.strip()
        if not code:
            continue
            
        print(f"\n===== 解析 {code} ===== ")
        
        res = Parser.parse(code)
        for k, v in res.items():
            print(f"> {k} :")
            if v:
                last_code = v[-1]
                info = Parser.get_clc_info_by_code(last_code)
                print(info)