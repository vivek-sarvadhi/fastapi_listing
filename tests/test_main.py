from fastapi.testclient import TestClient
from ..api.main import app
from fastapi import status

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "Hello World"}

def test_create_listing_success():
    # 'image': ('/Users/sarvadhi1/Downloads/MicrosoftTeams-image (1).png', 'test image data'),
    image_file = '/Users/sarvadhi1/Downloads/MicrosoftTeams-image (1).png'
    payload = {
        'name': 'Test Listing sd',
        'category_id': 9,
        'brand_id': 9,
        'hsn_code': '123456',
        'dimensions': '10x10x10',
        'price': 100,
    }
    files = {
        'image': ('image.png', image_file, 'image/png')
    }
    response = client.post('/add_listing', data=payload, files=files)
    print(response.json())
    print(response.headers)
    assert response.status_code == 201
    assert response.json() == {'success': True, 'message': 'Listing has been created successfully.'}

# def test_create_listing_existing():
#     image_file = '/Users/sarvadhi1/Downloads/MicrosoftTeams-image (1).png'
#     payload = {
#         'name': 'Test Listing',
#         'category_id': 9,
#         'brand_id': 9,
#         'hsn_code': '123456',
#         'dimensions': '10x10x10',
#         'price': 100,
#     }
#     files = {
#         'image': ('image.png', image_file, 'image/png')
#     }
#     response = client.post('/add_listing', data=payload, files=files)
#     assert response.status_code == 400
#     assert response.json() == {'success': False, 'message': 'Cannot create listing listing ID already available.'}

# def test_create_listing_missing_brand():
#     payload = {
#         'name': 'Test Listing',
#         'category_id': 1,
#         'brand_id': 999,
#         'hsn_code': '123456',
#         'dimensions': '10x10x10',
#         'price': 100.0,
#         'image': ('test.jpg', 'test image data'),
#     }
#     response = client.post('/add_listing', data=payload)
#     assert response.status_code == 400
#     assert response.json() == {'success': False, 'message': 'Cannot create listing brand ID is missing.'}

# def test_create_listing_missing_category():
#     payload = {
#         'name': 'Test Listing',
#         'category_id': 999,
#         'brand_id': 1,
#         'hsn_code': '123456',
#         'dimensions': '10x10x10',
#         'price': 100.0,
#         'image': ('test.jpg', 'test image data'),
#     }
#     response = client.post('/add_listing', data=payload)
#     assert response.status_code == 400
#     assert response.json() == {'success': False, 'message': 'Cannot create listing category ID is missing.'}

