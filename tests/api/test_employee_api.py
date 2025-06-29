from faker import Faker

from app import connection_pool
from app.constant.employee_constant import EmployeeAllowedFields
from app.core.rate_limiter import SEARCH_RATE_LIMITER

fake = Faker().unique


class TestSearchEmployee:
    def test_search_employees(self, client, employee_1, employee_2):
        # Arrange
        params = {
            'organization_id': employee_1.organization_id,
            'keyword': employee_1.first_name[:-1],
        }

        # Act
        response = client.get('/employee/', params=params)

        # Assert
        assert response.status_code == 200, response.text
        data = response.json()
        assert data['total'] == 1
        assert len(data['items']) == 1

        item_0 = data['items'][0]
        assert item_0['id'] == employee_1.id
        with connection_pool.open_session() as session:
            employee = session.merge(employee_1)

            allowed_fields = set(employee.organization.column_config) | {'id'}
            not_allowed_fields = {field for field in EmployeeAllowedFields if field not in allowed_fields}

            assert set(item_0['allowed_fields']) == allowed_fields

            for field in allowed_fields:
                assert item_0[field], f'Field {field} should be in the response'
            for field in not_allowed_fields:
                assert not item_0[field], f'Field {field} should not be in the response'

    def test_employee_search_rate_limit(self, client, employee_1, employee_2):
        # Arrange
        allowed_requests = 5
        SEARCH_RATE_LIMITER.max_requests = allowed_requests
        SEARCH_RATE_LIMITER.reset_all()
        params = {
            'organization_id': employee_1.organization_id,
        }

        # Act
        responses = []
        for _ in range(allowed_requests + 10):
            response = client.get('/employee/', params=params)
            responses.append(response)

        # Assert
        for i, response in enumerate(responses):
            if i < allowed_requests:
                assert response.status_code == 200, f'Failed at request {i + 1}: {response.text}'
            else:
                assert response.status_code == 429, f'Expected rate limit at request {i + 1}, got: {response.status_code}'
                assert 'Rate limit exceeded' in response.text
