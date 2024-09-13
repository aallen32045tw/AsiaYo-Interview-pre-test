import pytest
import json
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_valid_order_creation(client):
    response = client.post('/api/orders', json={
        'id': 'A12345',
        'name': 'Melody Holiday Inn',
        'address': {
            'city': 'taipei-city',
            'district': 'da-an-district',
            'street': 'fuxing-south-road'
        },
        'price': '1000',
        'currency': 'TWD'
    })
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['message'] == 'Order processed successfully'
    assert data['order']['price'] == '1000'
    assert data['order']['currency'] == 'TWD'

def test_valid_usd_order_creation(client):
    response = client.post('/api/orders', json={
        'id': 'A12345',
        'name': 'Melody Holiday Inn',
        'address': {
            'city': 'taipei-city',
            'district': 'da-an-district',
            'street': 'fuxing-south-road'
        },
        'price': '100',
        'currency': 'USD'
    })
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['message'] == 'Order processed successfully'
    assert data['order']['price'] == '3100.00'
    assert data['order']['currency'] == 'TWD'

def test_name_with_non_english_characters(client):
    response = client.post('/api/orders', json={
        'id': 'A12345',
        'name': 'Melody Holiday Inn 旅館',
        'address': {'city': 'taipei-city', 'district': 'da-an-district', 'street': 'fuxing-south-road'},
        'price': '1000',
        'currency': 'TWD'
    })
    assert response.status_code == 400
    data = json.loads(response.data)
    assert "Name contains non-English characters" in data['error']

def test_name_not_capitalized(client):
    response = client.post('/api/orders', json={
        'id': 'A12345',
        'name': 'melody holiday inn',
        'address': {'city': 'taipei-city', 'district': 'da-an-district', 'street': 'fuxing-south-road'},
        'price': '1000',
        'currency': 'TWD'
    })
    assert response.status_code == 400
    data = json.loads(response.data)
    assert "Name is not capitalized" in data['error']

def test_price_over_2000(client):
    response = client.post('/api/orders', json={
        'id': 'A12345',
        'name': 'Melody Holiday Inn',
        'address': {'city': 'taipei-city', 'district': 'da-an-district', 'street': 'fuxing-south-road'},
        'price': '2500',
        'currency': 'TWD'
    })
    assert response.status_code == 400
    data = json.loads(response.data)
    assert "Price is over 2000" in data['error']

def test_invalid_price(client):
    response = client.post('/api/orders', json={
        'id': 'A12345',
        'name': 'Melody Holiday Inn',
        'address': {'city': 'taipei-city', 'district': 'da-an-district', 'street': 'fuxing-south-road'},
        'price': 'not a number',
        'currency': 'TWD'
    })
    assert response.status_code == 400
    data = json.loads(response.data)
    assert "Price is not a valid number" in data['error']

def test_invalid_currency(client):
    response = client.post('/api/orders', json={
        'id': 'A12345',
        'name': 'Melody Holiday Inn',
        'address': {'city': 'taipei-city', 'district': 'da-an-district', 'street': 'fuxing-south-road'},
        'price': '1000',
        'currency': 'EUR'
    })
    assert response.status_code == 400
    data = json.loads(response.data)
    assert "Currency format is wrong" in data['error']

def test_multiple_errors(client):
    response = client.post('/api/orders', json={
        'id': 'A12345',
        'name': 'melody holiday inn 旅館',
        'address': {'city': 'taipei-city', 'district': 'da-an-district', 'street': 'fuxing-south-road'},
        'price': '2500',
        'currency': 'EUR'
    })
    assert response.status_code == 400
    data = json.loads(response.data)
    assert "Name contains non-English characters" in data['error']
    assert "Name is not capitalized" in data['error']
    assert "Price is over 2000" in data['error']
    assert "Currency format is wrong" in data['error']

def test_missing_required_field(client):
    response = client.post('/api/orders', json={
        'id': 'A12345',
        'name': 'Melody Holiday Inn',
        'address': {'city': 'taipei-city', 'district': 'da-an-district', 'street': 'fuxing-south-road'},
        'price': '1000'
        # missing 'currency' field
    })
    assert response.status_code == 400
    data = json.loads(response.data)
    assert "Invalid form data" in data['error']

