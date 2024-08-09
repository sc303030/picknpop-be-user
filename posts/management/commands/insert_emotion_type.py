from django.core.management import BaseCommand

from posts.models import EmotionType


class Command(BaseCommand):
    help = "감정표현을 생성합니다."

    def handle(self, *args, **options):
        emotion_types = [
            {
                "name": "like",
                "description": "좋아요",
            },
            {
                "name": "funny",
                "description": "재밌어요",
            },
            {
                "name": "surprised",
                "description": "놀라워요",
            },
            {
                "name": "love",
                "description": "사랑해요",
            },
            {
                "name": "angry",
                "description": "화나요",
            },
            {
                "name": "sad",
                "description": "슬퍼요",
            },
        ]

        for emotion_type in emotion_types:
            EmotionType.objects.get_or_create(
                name=emotion_type["name"],
                defaults={"description": emotion_type["description"]},
            )

        print("EmotionType inserted successfully!")
