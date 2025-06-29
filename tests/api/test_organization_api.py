from faker import Faker

fake = Faker().unique


class TestSearchOrganization:
    def test_search_organizations(self, client, organization_1, organization_2):
        # Arrange
        params = {
            'keyword': organization_1.name[:-1],
        }

        # Act
        response = client.get('/organization/', params=params)

        # Assert
        assert response.status_code == 200, response.text
        data = response.json()
        assert data['total'] == 1
        assert len(data['items']) == 1

        item_0 = data['items'][0]
        assert item_0['id'] == organization_1.id
