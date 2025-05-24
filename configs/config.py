from dynaconf import Dynaconf
from pathlib import Path

# 初始化Dynaconf
settings = Dynaconf(
    settings_files=['configs/main.toml', 'configs/biz.toml', 'configs/logger.toml'],  # 核心配置
    # includes=[],  # 附加配置
    environments=True,
    load_dotenv=True,
    lowercase_read=True
)


class MainConfig:
    @property
    def app_name(self):
        return settings.app_name

    @property
    def app_threads(self):
        return settings.app_threads


class BizConfig:
    @property
    def input_dir(self):
        return Path(settings.input_dir)

    @property
    def output_dir(self):
        return Path(settings.output_dir)

    @property
    def combine_program_count(self):
        return settings.combine_program_count

    @property
    def combine_topic_count(self):
        return settings.combine_topic_count

    @property
    def combine_material_count(self):
        return settings.combine_material_count

    @property
    def ffmpeg_path(self):
        return Path(settings.ffmpeg_path)

    @property
    def combine_rule(self):
        return settings.rule


def ensure_input_dirs():
    """验证必要路径"""
    if not BizConfig().input_dir.exists():
        raise FileNotFoundError(f"输入目录不存在: {BizConfig().input_dir}")


def ensure_output_dirs():
    """创建必要目录并验证路径"""
    if not BizConfig().output_dir.exists():
        BizConfig().output_dir.mkdir(parents=True, exist_ok=True)


ensure_input_dirs()
ensure_output_dirs()
print("[Debug] Loaded 'app_name':", MainConfig().app_name)
print("[Debug] Current Environment:", settings.current_env)
print("[Debug] All Settings:", settings.to_dict())
