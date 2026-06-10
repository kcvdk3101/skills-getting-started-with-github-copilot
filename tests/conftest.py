from copy import deepcopy

import pytest
from fastapi.testclient import TestClient

from src.app import app, activities as app_activities


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    original_activities = deepcopy(app_activities)
    yield
    app_activities.clear()
    app_activities.update(original_activities)
