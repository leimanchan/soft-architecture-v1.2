from adapters.flask.label_generator.app import create_app


def test_index_and_generate_validation():
    app = create_app()
    client = app.test_client()

    response = client.get('/')
    assert response.status_code == 200

    response = client.post('/generate', json={})
    assert response.status_code == 400
