from faker import Faker

fake = Faker().unique


class TestSearchLocation:
    def test_search_locations(self, client, location_1, location_2):
        # Arrange
        params = {
            'keyword': location_1.name[:-1],
        }

        # Act
        response = client.get('/location/', params=params)

        # Assert
        assert response.status_code == 200, response.text
        data = response.json()
        assert data['total'] == 1
        assert len(data['items']) == 1

        item_0 = data['items'][0]
        assert item_0['id'] == location_1.id
