from pathlib import Path
from utils import nvdia_utils as n
from utils import time_utils as t
import tempfile


def build_output_file_path(output_dir: Path):
    out_file_name = f"live_stream_{t.get_current_time_in_mills()}.mp4"
    output_file_path = output_dir.joinpath(out_file_name)
    print(f"输出的合成视频文件路径为: {output_file_path}")
    return output_file_path


def build_ffmpeg_command_list(input_files: list, output_file_path: Path, ffmpeg_path: str) -> tuple[list[str], Path]:
    """构建支持NVIDIA加速检测的FFmpeg命令"""
    # 创建临时文件
    with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8') as tmp_file:
        for file in input_files:
            # 用 Path 对象处理路径
            abs_path = Path(file).resolve()  # 获取标准化绝对路径
            posix_path = abs_path.as_posix()  # 转换为 POSIX 格式路径（自动处理斜杠）
            escaped_path = posix_path.replace("'", r"'\''")  # 转义单引号

            # 写入符合 FFmpeg concat 协议的格式
            tmp_file.write(f"file '{escaped_path}'\n")

        # 获取 Path 格式的临时文件路径
        tmp_file_path = Path(tmp_file.name)

    # 硬件加速检测
    use_nvidia = n.check_nvidia_support(ffmpeg_path)

    # 构建基础命令
    cmd = [str(ffmpeg_path), '-y']

    # 添加硬件加速参数
    if use_nvidia:
        cmd.extend([
            '-hwaccel', 'cuda',  # CUDA解码加速
            '-hwaccel_output_format', 'cuda'  # GPU内存直传
        ])

    # 合并参数
    cmd.extend([
        '-f', 'concat',
        '-safe', '0',
        '-i', tmp_file_path,
        '-c', 'copy'  # 保持流拷贝阶段
    ])

    # 动态选择编码参数
    if use_nvidia:
        transcode_params = [
            '-c:v', 'h264_nvenc',  # NVIDIA编码器
            '-preset', 'p6',  # NVIDIA专用预设
            '-cq', '23',  # 等效CRF的NVIDIA参数
            '-rc', 'vbr',  # 可变比特率模式
            '-c:a', 'aac',
            '-b:a', '192k'
        ]
    else:
        transcode_params = [
            '-c:v', 'libx264',
            '-preset', 'medium',
            '-crf', '23',
            '-c:a', 'aac',
            '-b:a', '192k'
        ]

    # Windows系统文件锁定处理
    if output_file_path.exists():
        output_file_path.unlink()

    return cmd + transcode_params + [str(output_file_path)], tmp_file_path
