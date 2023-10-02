import server
from server import app


class TestPointsUpdate:
    client = app.test_client()
    competition = [
        {
            "name": "Competition Test",
            "date": "2023-10-10 10:10:10",
            "numberOfPlaces": "25"
        }
    ]

    club = [
        {
            "name": "Test club 1",
            "email": "test@test.com",
            "points": "12"
        }
    ]

    def setup_method(self):
        server.competitions = self.competition
        server.clubs = self.club

    def test_points(self):
        places_reserved = 1

        self.client.post(
            "/purchasePlaces",
            data={
                "places": places_reserved,
                "club": self.club[0]["name"],
                "competition": self.competition[0]["name"]
            }
        )

        result = self.client.get("/board")

        assert result.status_code == 200
