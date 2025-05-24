import random
import re
from pathlib import Path
from typing import Dict, List
from utils import sorted_utils as s


def random_select_program_list(base_dir: Path, count) -> list[Path]:
    # 获取所有有效节目列表
    all_folders = [
        p for p in base_dir.iterdir()
        if p.is_dir() and p.name.startswith("NO.")
    ]
    return random.sample(all_folders, min(count, len(all_folders)))


def build_program_material_list(combine_rule_master_slave_dict: Dict[str, str], program_path: Path,
                        combine_topic_count: int, combine_material_count: int, exclude_hidden=True) -> List[Path]:
    """生成合并素材列表

    Args:
        combine_rule_master_slave_dict: 合并规则
        program_path: 节目路径
        combine_topic_count: 合并的主题数量
        combine_material_count: 合并的素材数量
        exclude_hidden: 隐藏文件标识位

    Returns:
        合并节目素材列表
    """
    combine_program_material_list = []

    combine_master_topic_list = []
    combine_slave_topic_no_path_dict = {}

    print(f"combine_rule_master_slave_dict:{combine_rule_master_slave_dict}")
    master_topic_no_list = list(combine_rule_master_slave_dict.keys())
    print(f"根据配置将以下序号的主题进行master随机列表生成操作:{master_topic_no_list[:]}")
    random_topic_no_list = random.sample(master_topic_no_list, min(combine_topic_count, len(master_topic_no_list)))
    print(f"以下序号的主题为随机生成的master列表:{random_topic_no_list[:]}")
    # 本节目中需要合并的主题序号字典
    program_combine_topic_no_dict = distill_program_combine_topic_no_dict(random_topic_no_list, combine_rule_master_slave_dict)
    print(f"以下序号的主题为需要合并->key为Master,value为Slave:{program_combine_topic_no_dict}")
    salve_topic_no_list = program_combine_topic_no_dict.values()
    print("\n")
    # 获取需要合并的主题列表
    for entry in program_path.iterdir():
        if entry.is_dir():
            if exclude_hidden and entry.name.startswith('.'):
                # 跳过隐藏目录
                continue
            topic_no = distill_topic_no(entry)
            if topic_no in program_combine_topic_no_dict:
                combine_master_topic_list.append(entry)
            elif topic_no in salve_topic_no_list:
                combine_slave_topic_no_path_dict[topic_no] = entry

    for combine_master_topic in combine_master_topic_list:
        sorted_master_material_list = sorted(
            [f.name for f in combine_master_topic.iterdir() if f.is_file()],
            key=s.natural_sort_key
        )

        sorted_master_material_list_len = len(sorted_master_material_list)
        random_material_name_list = random.sample(sorted_master_material_list,
                                             min(combine_material_count, sorted_master_material_list_len))
        master_topic_no = distill_topic_no(combine_master_topic)
        slave_topic_no = program_combine_topic_no_dict[master_topic_no]
        combine_slave_topic = combine_slave_topic_no_path_dict[slave_topic_no]
        random_material_segment_list = build_combine_material_segment_list(combine_master_topic, combine_slave_topic, random_material_name_list)
        combine_program_material_list.extend(random_material_segment_list)
    print(f"当前节目{program_path.name}的合并素材列表为:{combine_program_material_list[:]}")
    return combine_program_material_list


def build_whole_material_list(combine_rule_master_slave_dict: Dict[str, str], random_program_list: List[Path],
                              combine_topic_count: int, combine_material_count: int) -> List[Path]:
    """构建完整的素材列表
    :param combine_rule_master_slave_dict: 合并规则
    :param random_program_list: 随机节目列表
    :param combine_topic_count: 合并的主题数量
    :param combine_material_count: 合并的素材数量
    :return: whole_material_list 整体素材列表
    """
    whole_material_list = []
    if random_program_list:
        for random_program in random_program_list:
            program_material_list = build_program_material_list(combine_rule_master_slave_dict, random_program,
                                                                 combine_topic_count, combine_material_count)
            whole_material_list.extend(program_material_list)
    return whole_material_list


def build_combine_material_segment_list(master_topic: Path, slave_topic: Path,
                                        random_material_name_list: List[str]) -> List[Path]:
    """构建合并素材列表片段
    :param master_topic: master主题
    :param slave_topic: slave主题
    :param random_material_name_list: 随机素材名列表
    :return:
    """
    combine_material_segment_list = []
    for random_material_name in random_material_name_list:
        random_master_material_path = master_topic.joinpath(random_material_name)
        random_slave_material_path = slave_topic.joinpath(random_material_name)
        combine_material_segment_list.append(random_master_material_path)
        combine_material_segment_list.append(random_slave_material_path)
    return combine_material_segment_list


def distill_program_combine_topic_no_dict(random_topic_no_list: List[str],
                                          combine_rule_dict: Dict[str, str]) -> Dict[str, str]:
    """根据随机主题序号提取需要合并的主题序号
    :param random_topic_no_list: 随机生成的主题序号列表
    :param combine_rule_dict: 主题合并规则字典
    :return: 需要合并的主题序号字典
    """
    program_combine_topic_no_dict = {}
    for topic_no in random_topic_no_list:
        if topic_no in random_topic_no_list:
            program_combine_topic_no_dict[topic_no] = combine_rule_dict[topic_no]
    return program_combine_topic_no_dict


def distill_topic_no(path: Path):
    """提取主题序号
    :param path: 主题路径
    :return: 主题序号
    """
    return re.split(r'(\d+)', path.name)[1]
