from tests.conftest import clubs_data, competitions_data

import server


class TestClass:
    def test_index_page_status_ok(self, client):
        """
            Vérification si le code renvoyé est 200
            lorsque l'on appelle la page "index"
        """
        response = client.get('/')
        assert response.status_code == 200

    def test_index_unkwown_email(self, client):
        """
            Test de réponse pour un email non connue
        """
        email = "unkwownmail@test.com"
        response = client.post("/showSummary", data={"email": email})

        assert response.status_code == 302

    def test_email_in_the_database(self, client, mocker):
        """
            Test de réponse d'un email connue dans la base de données
        """
        mocker.patch.object(server, "clubs", clubs_data)
        club_email = "test@test.com"

        response = client.post("/showSummary", data={"email": club_email})
        data = response.data.decode()
        assert response.status_code == 200
        assert "test@test.com" in data

    def test_purchasePlaces_status_ok(self, client):
        """
            Vérification si le code renvoyé est 200
            lorsque l'on appelle la page "purchasePlaces"
            et que l'on sélectionne un évenement
        """
        response = client.get("/book/Fall%20Classic/Simply%20Lift")
        assert response.status_code == 200

    def test_order_places_and_enough_points(self, client, mocker):
        """
            Vérification si on a assez de point pour commander des places
        """
        mocker.patch.object(server, "clubs", clubs_data)
        mocker.patch.object(server, "competitions", competitions_data)

        club = "Test Club 1"
        competition = "Competition Test"
        points = 10

        response = client.post("/purchasePlaces", data={
            "club": club,
            "competition": competition,
            "places": points})
        data = response.data.decode()

        assert response.status_code == 200
        assert "Great-booking complete!" in data

    def test_order_places_and_not_enough_points(self, client, mocker):
        """
            Vérification si on a pas assez de point pour commander des places
        """
        mocker.patch.object(server, "clubs", clubs_data)
        mocker.patch.object(server, "competitions", competitions_data)

        club = "Test Club 1"
        competition = "Competition Test"
        points = 14

        response = client.post("/purchasePlaces", data={
            "club": club,
            "competition": competition,
            "places": points})
        data = response.data.decode()

        assert response.status_code == 200
        assert "Vous n&#39;avez pas assez de points pour inscrire le nombre demandé" in data

    def test_limited_to_12_places_maximum(self, client, mocker):
        """
            Limitation à 12 places en réservation
        """
        mocker.patch.object(server, "clubs", clubs_data)
        mocker.patch.object(server, "competitions", competitions_data)

        club = "Test Club 2"
        competition = "Competition Test"
        points = 13

        response = client.post("/purchasePlaces", data={
            "club": club,
            "competition": competition,
            "places": points})
        data = response.data.decode()

        assert response.status_code == 200
        assert "Vous ne pouvez pas commander plus de 12 places" in data

    def test_negative_entry(self, client, mocker):
        """
            Vérification si on a une saisie négative en réservation de place
        """
        mocker.patch.object(server, "clubs", clubs_data)
        mocker.patch.object(server, "competitions", competitions_data)

        club = "Test Club 2"
        competition = "Competition Test"
        points = -5

        response = client.post("/purchasePlaces", data={
            "club": club,
            "competition": competition,
            "places": points})
        data = response.data.decode()

        assert response.status_code == 200
        assert "Vous ne pouvez pas saisir une quantité négative" in data

    def test_past_date(self, client, mocker):
        """
            Vérification si on a une date dans le passé
        """
        mocker.patch.object(server, "clubs", clubs_data)
        mocker.patch.object(server, "competitions", competitions_data)

        response = client.get("/book/Competition_Test_date/Simply%20Lift")
        data = response.data.decode()

        assert response.status_code == 200
        assert "Ce concours est dans le passé" in data
