from tests.conftest import clubs_data

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
