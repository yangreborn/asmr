import os
import mutagen
from datetime import datetime
from django.utils import timezone
from pathlib import Path
import re


class AudioFileParser:
    """音频文件解析工具类"""

    AUDIO_EXTENSIONS = ['.mp3', '.wav', '.flac', '.m4a', '.aac', '.ogg']

    @staticmethod
    def get_audio_duration(file_path):
        """获取音频文件时长（秒）"""
        try:
            audio = mutagen.File(file_path)
            if audio is not None:
                return int(audio.info.length)
        except:
            pass
        return None

    @staticmethod
    def extract_info_from_filename(filename):
        """从文件名中提取信息"""
        info = {
            'name': Path(filename).stem,
            'level': 0,
            'duration': None
        }

        # 尝试从文件名中提取等级（如：作品名_L3.mp3）
        level_match = re.search(r'[Ll](\d+)', filename)
        if level_match:
            info['level'] = int(level_match.group(1))

        # 尝试从文件名中提取时长（如：作品名_30min.mp3）
        duration_match = re.search(r'(\d+)\s*min', filename, re.IGNORECASE)
        if duration_match:
            info['duration'] = int(duration_match.group(1)) * 60  # 转换为秒

        return info

    @staticmethod
    def is_audio_file(file_path):
        """检查是否为音频文件"""
        return Path(file_path).suffix.lower() in AudioFileParser.AUDIO_EXTENSIONS


import os
from pathlib import Path
from collections import defaultdict


class DirectoryScanner:
    """目录扫描工具类"""

    @staticmethod
    def scan_directory(base_path):
        """
        扫描目录结构，返回作者和对应的音频文件列表
        返回格式: {author_name: [audio_file_path1, audio_file_path2, ...]}
        """
        if not os.path.exists(base_path):
            raise ValueError(f"目录不存在: {base_path}")

        if not os.path.isdir(base_path):
            raise ValueError(f"路径不是目录: {base_path}")

        author_files = defaultdict(list)

        # 遍历第一级子目录（作者目录）
        for author_dir in os.listdir(base_path):
            author_path = os.path.join(base_path, author_dir)

            if os.path.isdir(author_path):
                # 扫描作者目录下的音频文件
                audio_files = DirectoryScanner._find_audio_files(author_path)
                author_files[author_dir] = audio_files

        return author_files

    @staticmethod
    def _find_audio_files(directory):
        """递归查找目录下的所有音频文件"""
        audio_files = []

        for root, _, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                if AudioFileParser.is_audio_file(file_path):
                    audio_files.append(file_path)

        return audio_files