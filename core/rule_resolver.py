from typing import Dict


def resolve_combined_master_slave_rule(combine_rule: str) -> Dict[str, str]:
    """解析合并规则中的主从关系

    :param: combine_rule
    :return: Dict[str, str]
    """
    combine_rule_master_slave_dict = {}
    if combine_rule:
        rule_items = combine_rule.split("|")
        for rule_item in rule_items:
            master = rule_item.split("+")[0]
            slave = rule_item.split("+")[1]
            combine_rule_master_slave_dict[master] = slave

    return combine_rule_master_slave_dict

