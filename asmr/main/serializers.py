
from rest_framework import serializers
from django.conf import settings
import os

class AudioImportSerializer(serializers.Serializer):
    directory_path = serializers.CharField(max_length=500,required=True,help_text='服务器本地目录路径')
    studio_name = serializers.CharField(
        max_length=100,
        required=False,
        allow_null=True,
        allow_blank=True,
        help_text='工作室名称'
    )
    country = serializers.IntegerField(
        default=0,
        min_value=0,
        max_value=3,
        help_text='作者国家 (0:中国, 1:日本, 2:韩国, 3:其他)'
    )
    type = serializers.IntegerField(
        default=0,
        min_value=0,
        max_value=4,
        help_text='作者类型 (0:音声, 1:视频音声, 2:视频, 3:图片, 4:其他)'
    )

    def validate_directory_path(self, value):
        """验证目录路径"""
        # 安全检查：确保路径在允许的范围内
        allowed_base = getattr(settings, 'ALLOWED_IMPORT_DIRECTORIES', ['/data/audio'])
        if not any(value.startswith(allowed) for allowed in allowed_base):
            raise serializers.ValidationError('不允许访问该目录')

        if not os.path.exists(value):
            raise serializers.ValidationError(f'目录不存在: {value}')

        if not os.path.isdir(value):
            raise serializers.ValidationError(f'路径不是目录: {value}')

        return value

    def validate(self, attrs):
        """全局验证"""
        # 可以在这里添加更多的验证逻辑
        return attrs