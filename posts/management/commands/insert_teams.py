from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management import BaseCommand

from posts.models import Team

User = get_user_model()


class Command(BaseCommand):
    help = "KBL 리그팀을 생성합니다."

    def handle(self, *args, **options):
        EMBLEM_URL = "media/team_emblems/KBL"

        teams = [
            {
                "name": "KBL",
                "league": Team.LeagueChoices.KBL,
                "emblem": f"{EMBLEM_URL}/kbl.png",
            },
            {
                "name": "서울 SK",
                "league": Team.LeagueChoices.KBL,
                "emblem": f"{EMBLEM_URL}/sk.png",
            },
            {
                "name": "수원 KT",
                "league": Team.LeagueChoices.KBL,
                "emblem": f"{EMBLEM_URL}/kt.png",
            },
            {
                "name": "대구 한국가스공사",
                "league": Team.LeagueChoices.KBL,
                "emblem": f"{EMBLEM_URL}/gas.png",
            },
            {
                "name": "부산 KCC",
                "league": Team.LeagueChoices.KBL,
                "emblem": f"{EMBLEM_URL}/kcc.png",
            },
            {
                "name": "창원 LG",
                "league": Team.LeagueChoices.KBL,
                "emblem": f"{EMBLEM_URL}/lg.png",
            },
            {
                "name": "안양 정관장",
                "league": Team.LeagueChoices.KBL,
                "emblem": f"{EMBLEM_URL}/jungkwanjang.png",
            },
            {
                "name": "울산 현대모비스",
                "league": Team.LeagueChoices.KBL,
                "emblem": f"{EMBLEM_URL}/mobis.png",
            },
            {
                "name": "원주 DB",
                "league": Team.LeagueChoices.KBL,
                "emblem": f"{EMBLEM_URL}/db.png",
            },
            {
                "name": "고양 소노",
                "league": Team.LeagueChoices.KBL,
                "emblem": f"{EMBLEM_URL}/sono.png",
            },
            {
                "name": "서울 삼성",
                "league": Team.LeagueChoices.KBL,
                "emblem": f"{EMBLEM_URL}/samsung.png",
            },
        ]

        for team in teams:
            Team.objects.get_or_create(
                name=team["name"],
                defaults={"league": team["league"], "emblem": team["emblem"]},
            )

        print("Teams inserted successfully!")
