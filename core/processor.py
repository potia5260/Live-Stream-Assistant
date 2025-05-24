import os
from typing import List
import subprocess
from pathlib import Path


def gen_video(gen_video_cmd: List[str], output_video_path: Path, tmp_file_path: Path):
    try:
        print("开始视频合并处理...")
        subprocess.run(gen_video_cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=os.name == "nt")
        print(f"合并完成！输出文件为: {output_video_path.name},它的路径为: {output_video_path}")
    except subprocess.CalledProcessError as e:
        print(f"FFmpeg处理失败: {str(e)}")
    finally:
        if tmp_file_path.exists():
            tmp_file_path.unlink()
