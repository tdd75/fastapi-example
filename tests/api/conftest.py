import pytest
from faker import Faker

from app import connection_pool
from app.constant.employee_constant import EmployeeStatus, EmployeeAllowedFields
from app.model.department import Department
from app.model.employee import Employee
from app.model.location import Location
from app.model.organization import Organization
from app.model.position import Position
from app.repository import employee_repository, organization_repository, department_repository, location_repository, \
    position_repository

fake = Faker().unique


@pytest.fixture
def organization_1() -> Organization:
    with connection_pool.open_session() as session:
        organization = Organization(
            name=fake.company(),
            domain=fake.domain_name(),
            column_config=[
                EmployeeAllowedFields.FIRST_NAME,
                EmployeeAllowedFields.LAST_NAME,
                EmployeeAllowedFields.EMAIL,
                EmployeeAllowedFields.DEPARTMENT,
                EmployeeAllowedFields.POSITION,
            ],
        )
        organization = organization_repository.create(session, organization)
        return organization


@pytest.fixture
def organization_2() -> Organization:
    with connection_pool.open_session() as session:
        organization = Organization(
            name=fake.company(),
            domain=fake.domain_name(),
            column_config=[
                EmployeeAllowedFields.FIRST_NAME,
                EmployeeAllowedFields.LAST_NAME,
                EmployeeAllowedFields.EMAIL,
                EmployeeAllowedFields.DEPARTMENT,
                EmployeeAllowedFields.POSITION,
            ],
        )
        organization = organization_repository.create(session, organization)
        return organization


@pytest.fixture
def department_1(organization_1) -> Department:
    with connection_pool.open_session() as session:
        department = Department(
            name=fake.word(),
            description=fake.sentence(),
            organization_id=organization_1.id,
        )
        return department_repository.create(session, department)


@pytest.fixture
def department_2(organization_2) -> Department:
    with connection_pool.open_session() as session:
        department = Department(
            name=fake.word(),
            description=fake.sentence(),
            organization_id=organization_2.id,
        )
        return department_repository.create(session, department)


@pytest.fixture
def location_1(organization_1) -> Location:
    with connection_pool.open_session() as session:
        location = Location(
            name=fake.city(),
            address=fake.address(),
            city=fake.city(),
            country=fake.country(),
            organization_id=organization_1.id,
        )
        return location_repository.create(session, location)


@pytest.fixture
def location_2(organization_2) -> Location:
    with connection_pool.open_session() as session:
        location = Location(
            name=fake.city(),
            address=fake.address(),
            city=fake.city(),
            country=fake.country(),
            organization_id=organization_2.id,
        )
        return location_repository.create(session, location)


@pytest.fixture
def position_1(organization_1) -> Position:
    with connection_pool.open_session() as session:
        position = Position(
            title=fake.job(),
            level=fake.word(),
            description=fake.sentence(),
            organization_id=organization_1.id,
        )
        return position_repository.create(session, position)


@pytest.fixture
def position_2(organization_2) -> Position:
    with connection_pool.open_session() as session:
        position = Position(
            title=fake.job(),
            level=fake.word(),
            description=fake.sentence(),
            organization_id=organization_2.id,
        )
        return position_repository.create(session, position)


@pytest.fixture
def employee_1(organization_1, department_1, location_1, position_1) -> Employee:
    with connection_pool.open_session() as session:
        employee = Employee(
            email=fake.email(),
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            phone=fake.phone_number(),
            hire_date=fake.date_object(),
            status=EmployeeStatus.ACTIVE,
            organization_id=organization_1.id,
            department_id=department_1.id,
            location_id=location_1.id,
            position_id=position_1.id,
            manager_id=None,
        )
        return employee_repository.create(session, employee)


@pytest.fixture
def employee_2(organization_2, department_2, location_2, position_2) -> Employee:
    with connection_pool.open_session() as session:
        employee = Employee(
            email=fake.email(),
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            phone=fake.phone_number(),
            hire_date=fake.date_object(),
            status=EmployeeStatus.ACTIVE,
            organization_id=organization_2.id,
            department_id=department_2.id,
            location_id=location_2.id,
            position_id=position_2.id,
            manager_id=None,
        )
        return employee_repository.create(session, employee)
