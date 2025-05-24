from configs.config import BizConfig
from core import selector, merger, rule_resolver, processor


def main():
    biz_config = BizConfig()
    input_dir = biz_config.input_dir
    combine_program_count = biz_config.combine_program_count
    combine_topic_count = biz_config.combine_topic_count
    combine_material_count = biz_config.combine_material_count
    combine_rule = biz_config.combine_rule
    ffmpeg_path = biz_config.ffmpeg_path
    # 解析合并规则
    combine_rule_master_slave_dict = rule_resolver.resolve_combined_master_slave_rule(combine_rule)
    # 随机获取的节目列表
    random_program_list = selector.random_select_program_list(input_dir, combine_program_count)
    # 完整的待合并素材列表
    whole_material_list = selector.build_whole_material_list(combine_rule_master_slave_dict, random_program_list, combine_topic_count, combine_material_count)
    output_dir = biz_config.output_dir
    output_file_path = merger.build_output_file_path(output_dir)
    ffmpeg_cmd_list, tmp_file_path = merger.build_ffmpeg_command_list(whole_material_list, output_file_path, ffmpeg_path)
    print(f"ffmpeg_cmd_list={ffmpeg_cmd_list}")
    processor.gen_video(ffmpeg_cmd_list, output_file_path, tmp_file_path)


if __name__ == '__main__':
    main()
