from enum import Enum


class EmployeeStatus(str, Enum):
    ACTIVE = 'active'
    NOT_STARTED = 'not_started'
    TERMINATED = 'terminated'


class EmployeeAllowedFields(str, Enum):
    FIRST_NAME = 'first_name'
    LAST_NAME = 'last_name'
    EMAIL = 'email'
    PHONE = 'phone'
    DEPARTMENT = 'department'
    POSITION = 'position'
    LOCATION = 'location'
    STATUS = 'status'
