import os
from pathlib import Path
from django.db import transaction
from .models import Author, ChineseAsmr, Studio
from .utils import AudioFileParser
from .utils import DirectoryScanner


class AudioImportService:
    """音频文件导入服务"""

    def __init__(self, default_studio=None, default_country=0, default_type=0):
        self.default_studio = default_studio
        self.default_country = default_country
        self.default_type = default_type

    @transaction.atomic
    def import_from_directory(self, base_path, studio_name=None):
        """
        从目录导入作者和音频文件
        base_path: 基础目录路径
        studio_name: 工作室名称，如果为None则使用默认工作室
        """
        try:
            # 获取或创建工作室
            studio = self._get_or_create_studio(studio_name)

            # 扫描目录
            author_files = DirectoryScanner.scan_directory(base_path)

            results = {
                'total_authors': len(author_files),
                'imported_authors': 0,
                'total_audio_files': 0,
                'imported_audio_files': 0,
                'authors': [],
                'errors': []
            }

            # 处理每个作者
            for author_name, audio_files in author_files.items():
                try:
                    author_result = self._process_author(
                        author_name, audio_files, studio
                    )
                    results['authors'].append(author_result)
                    results['imported_authors'] += 1
                    results['total_audio_files'] += len(audio_files)
                    results['imported_audio_files'] += author_result['imported_audio_files']
                except Exception as e:
                    error_msg = f"处理作者 {author_name} 时出错: {str(e)}"
                    results['errors'].append(error_msg)

            return results

        except Exception as e:
            raise Exception(f"导入过程中出错: {str(e)}")

    def _get_or_create_studio(self, studio_name):
        """获取或创建工作室"""
        if studio_name:
            studio, created = Studio.objects.get_or_create(
                name=studio_name,
                defaults={'description': f'自动创建的工作室: {studio_name}'}
            )
            return studio
        return self.default_studio

    def _process_author(self, author_name, audio_files, studio):
        """处理单个作者"""
        # 获取或创建作者
        author, created = Author.objects.get_or_create(
            name=author_name,
            defaults={
                'studio': studio,
                'country': self.default_country,
                'type': self.default_type,
                'description': f'从目录导入的作者: {author_name}'
            }
        )

        result = {
            'author_name': author_name,
            'author_id': author.id,
            'author_created': created,
            'total_audio_files': len(audio_files),
            'imported_audio_files': 0,
            'audio_files': []
        }

        # 处理音频文件
        for audio_file in audio_files:
            try:
                asmr = self._create_asmr_from_audio(audio_file, author)
                result['audio_files'].append({
                    'file_path': audio_file,
                    'asmr_id': asmr.id,
                    'status': 'success'
                })
                result['imported_audio_files'] += 1
            except Exception as e:
                result['audio_files'].append({
                    'file_path': audio_file,
                    'status': 'error',
                    'error': str(e)
                })

        return result

    def _create_asmr_from_audio(self, audio_path, author):
        """从音频文件创建ASMR记录"""
        # 从文件名和音频元数据中提取信息
        filename = Path(audio_path).name
        file_info = AudioFileParser.extract_info_from_filename(filename)

        # 获取音频时长
        duration = AudioFileParser.get_audio_duration(audio_path)
        if duration is None and file_info['duration']:
            duration = file_info['duration']

        # 创建ASMR记录
        asmr = ChineseAsmr.objects.create(
            name=file_info['name'],
            author=author,
            duration=duration,
            level=file_info['level'],
            description=f'从音频文件导入: {filename}'
        )

        return asmr