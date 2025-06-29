from faker import Faker

fake = Faker().unique


class TestSearchPosition:
    def test_search_positions(self, client, position_1, position_2):
        # Arrange
        params = {
            'keyword': position_1.title[:-1],
        }

        # Act
        response = client.get('/position/', params=params)

        # Assert
        assert response.status_code == 200, response.text
        data = response.json()
        assert data['total'] == 1
        assert len(data['items']) == 1

        item_0 = data['items'][0]
        assert item_0['id'] == position_1.id
