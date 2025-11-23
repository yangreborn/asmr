import os

from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .serializers import AudioImportSerializer
from .services import AudioImportService


class AudioImportView(CreateAPIView):
    """
    从目录导入作者和音频文件

    POST /api/import-audio/
    参数:
    - directory_path: 服务器本地目录路径
    - studio_name: 工作室名称（可选）
    - country: 作者国家（可选，默认0）
    - type: 作者类型（可选，默认0）
    """
    serializer_class = AudioImportSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        directory_path = validated_data['directory_path']
        studio_name = validated_data.get('studio_name')
        country = validated_data.get('country', 0)
        type = validated_data.get('type', 0)

        try:
            # 创建导入服务实例
            import_service = AudioImportService(
                default_country=country,
                default_type=type
            )

            # 执行导入
            results = import_service.import_from_directory(directory_path, studio_name)

            return Response({
                'status': 'success',
                'message': '导入完成',
                'data': results
            })

        except Exception as e:
            return Response({
                'status': 'error',
                'message': str(e),
                'data': None
            })