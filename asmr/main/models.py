from django.db import models

# Create your models here.
class Studio(models.Model):
    name = models.CharField(max_length=20, verbose_name='工作室名称')
    description = models.TextField(verbose_name='工作室描述', null=True, blank=True)
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')
    edit_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')
    is_over = models.BooleanField(default=False, verbose_name='是否结束')

    class Meta:
        verbose_name = '工作室'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class Author(models.Model):
    name = models.CharField(max_length=20, verbose_name='作者名称')
    studio = models.ForeignKey(Studio, on_delete=models.CASCADE, null=True, verbose_name='工作室名称')
    description = models.TextField(verbose_name='作者描述', null=True, blank=True)
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')
    edit_time = models.DateTimeField(auto_now=True,verbose_name='修改时间')
    is_over = models.BooleanField(default=False, verbose_name='是否结束')
    COUNTRY_CHOICES = [
        (0, '中国'),
        (1, '日本'),
        (2, '韩国'),
        (3, '其他'),
    ]
    country = models.SmallIntegerField(default=0, choices=COUNTRY_CHOICES, verbose_name='作者国家')
    TYPE_CHOICES = [
        (0, '音声'),
        (1, '视频音声'),
        (2, '视频'),
        (3, '图片'),
        (4, '其他')
    ]
    type = models.SmallIntegerField(default=0, choices=TYPE_CHOICES, verbose_name='作者类型')
    is_cast = models.BooleanField(default=False, verbose_name='是否是主播')
    level = models.SmallIntegerField(default=0, verbose_name='作者等级')
    alias = models.CharField(max_length=100, verbose_name='作者别名', null=True, blank=True)

    class Meta:
        verbose_name = '作者'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class ChineseAsmr(models.Model):
    name = models.CharField(max_length=100, verbose_name='asmr名称')
    description = models.TextField(verbose_name='asmr描述', blank=True, null=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name='作者名称', null=True, blank=True)
    next = models.ForeignKey('self', on_delete=models.CASCADE, null=True, verbose_name='下一集名称')
    duration = models.IntegerField(verbose_name='asmr时长', null=True)
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')
    edit_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')
    level = models.SmallIntegerField(default=0, verbose_name='asmr等级')
    remark = models.TextField(verbose_name='备注', null=True, blank=True)

    class Meta:
        verbose_name = 'asmr'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name