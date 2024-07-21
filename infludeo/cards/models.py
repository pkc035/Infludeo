from django.db import models

class PhotoCard(models.Model):
    """
    PhotoCard 모델

    Attributes:
        name (CharField): PhotoCard 이름(최대 길이는 100자)
        description (TextField): PhotoCard에 대한 설명
        image (ImageField): PhotoCard의 이미지(이미지 파일은 'photo_cards/' 디렉토리에 업로드)
        created_at (DateTimeField): PhotoCard가 생성된 날짜
    """
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='photo_cards/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        PhotoCard 인스턴스의 문자열 표현을 반환.

        Returns:
            str: PhotoCard의 이름
        """
        return self.name