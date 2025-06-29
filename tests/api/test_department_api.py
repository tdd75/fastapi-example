from faker import Faker

fake = Faker().unique


class TestSearchDepartment:
    def test_search_departments(self, client, department_1, department_2):
        # Arrange
        params = {
            'keyword': department_1.name[:-1],
        }

        # Act
        response = client.get('/department/', params=params)

        # Assert
        assert response.status_code == 200, response.text
        data = response.json()
        assert data['total'] == 1
        assert len(data['items']) == 1

        item_0 = data['items'][0]
        assert item_0['id'] == department_1.id
