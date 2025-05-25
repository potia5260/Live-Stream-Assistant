import subprocess


def check_nvidia_support(ffmpeg_path: str) -> bool:
    """检测系统是否支持NVIDIA硬件加速（兼容VPS误报场景）"""
    try:
        # 第一阶段：基础支持检测
        hwaccel_proc = subprocess.run(
            [ffmpeg_path, '-hwaccels'],
            capture_output=True,
            text=True,
            timeout=5
        )
        encoder_proc = subprocess.run(
            [ffmpeg_path, '-encoders'],
            capture_output=True,
            text=True,
            timeout=5
        )
        if not ('cuda' in hwaccel_proc.stdout.lower() and 'h264_nvenc' in encoder_proc.stdout):
            return False  # 提前终止，避免无意义测试

        # 第二阶段：实际编解码能力测试（避免仅依赖FFmpeg输出误判）
        test_command = [
            ffmpeg_path, '-y', '-f', 'lavfi', '-i', 'nullsrc=s=64x64:d=1',  # 生成测试视频源
            '-c:v', 'h264_nvenc',  # 使用NVENC编码器
            '-f', 'null', '-'  # 输出到空设备
        ]
        test_proc = subprocess.run(
            test_command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            timeout=10
        )

        # 关键错误过滤（如未找到设备、驱动不可用等）
        error_keywords = ["No NVENC capable devices found", "Cannot load libnvcuvid.so"]
        if any(keyword in test_proc.stdout for keyword in error_keywords):
            return False

        # 综合返回结果（返回码为0且无关键错误）
        return test_proc.returncode == 0

    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired) as e:
        print(f"检测异常: {str(e)}")
        return False
