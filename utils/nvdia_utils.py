import subprocess


def check_nvidia_support(ffmpeg_path: str) -> bool:
    """检测系统是否支持NVIDIA硬件加速"""
    try:
        # 验证硬件加速器支持
        hwaccel_proc = subprocess.run(
            [ffmpeg_path, '-hwaccels'],
            capture_output=True,
            text=True,
            timeout=5
        )

        print(f"hwaccel_proc={hwaccel_proc}")

        # 检查编码器支持
        encoder_proc = subprocess.run(
            [ffmpeg_path, '-encoders'],
            capture_output=True,
            text=True,
            timeout=5
        )
        print(f"encoder_proc={encoder_proc}")

        # 双重验证机制
        return ('cuda' in hwaccel_proc.stdout.lower()
                and 'h264_nvenc' in encoder_proc.stdout)
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
        return False
