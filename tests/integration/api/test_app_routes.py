from app.infrastructure.db.models.customer_model import CustomerModel
from app.infrastructure.db.models.pet_model import PetModel


def test_create_pet_endpoint_returns_success_response(client) -> None:
    response = client.post(
        "/create_pet",
        data={
            "type": "dog",
            "gender": "male",
            "size": "small",
            "age": "baby",
            "good_with_children": "true",
        },
        files=[("photos", ("puppy.jpg", b"fake-image-content", "image/jpeg"))],
    )

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "success"
    assert "pet_id" in body["data"]


def test_get_pets_endpoint_merges_local_and_external_results(client) -> None:
    create_response = client.post(
        "/create_pet",
        data={
            "type": "dog",
            "gender": "male",
            "size": "small",
            "age": "young",
            "good_with_children": "true",
        },
        files=[("photos", ("local-dog.jpg", b"dog", "image/jpeg"))],
    )
    assert create_response.status_code == 200

    response = client.get(
        "/get_pets",
        params=[("type", "dog"), ("limit", "2")],
    )

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "success"
    assert len(body["data"]["pets"]) == 2
    assert body["data"]["pets"][0]["source"] == "local"
    assert body["data"]["pets"][1]["source"] == "external"


def test_add_customer_returns_existing_customer_for_duplicate_phone(client) -> None:
    first_response = client.post(
        "/add_customer",
        json={"name": "Naomi", "phone": "0911002200"},
    )
    second_response = client.post(
        "/add_customer",
        json={"name": "Changed Name", "phone": "0911002200"},
    )

    assert first_response.status_code == 200
    assert second_response.status_code == 200
    assert first_response.json()["data"]["customer_id"] == second_response.json()["data"]["customer_id"]


def test_adopt_endpoint_creates_adoption_request_for_local_pet(client, db_session_factory) -> None:
    pet_response = client.post(
        "/create_pet",
        data={
            "type": "cat",
            "gender": "female",
            "size": "small",
            "age": "adult",
            "good_with_children": "false",
        },
        files=[("photos", ("cat.jpg", b"cat", "image/jpeg"))],
    )
    customer_response = client.post(
        "/add_customer",
        json={"name": "Abebe Kebede", "phone": "0911223344"},
    )

    adoption_response = client.post(
        "/adopt",
        json={
            "customer_id": customer_response.json()["data"]["customer_id"],
            "pet_id": pet_response.json()["data"]["pet_id"],
        },
    )

    assert adoption_response.status_code == 200
    body = adoption_response.json()
    assert body["status"] == "success"
    assert "adoption_id" in body["data"]


def test_adopt_endpoint_can_snapshot_external_pet(client, db_session_factory) -> None:
    customer_response = client.post(
        "/add_customer",
        json={"name": "Meron", "phone": "0911334455"},
    )

    adoption_response = client.post(
        "/adopt",
        json={
            "customer_id": customer_response.json()["data"]["customer_id"],
            "pet_id": "external_dog_100",
        },
    )

    assert adoption_response.status_code == 200
    session = db_session_factory()
    try:
        pet = session.get(PetModel, "external_dog_100")
        assert pet is not None
        assert pet.external_id == "100"
    finally:
        session.close()


def test_generate_report_endpoint_returns_expected_structure(client) -> None:
    pet_response = client.post(
        "/create_pet",
        data={
            "type": "dog",
            "gender": "male",
            "size": "medium",
            "age": "young",
            "good_with_children": "true",
        },
        files=[("photos", ("report-dog.jpg", b"dog", "image/jpeg"))],
    )
    customer_response = client.post(
        "/add_customer",
        json={"name": "Tsion", "phone": "0911445566"},
    )
    client.post(
        "/adopt",
        json={
            "customer_id": customer_response.json()["data"]["customer_id"],
            "pet_id": pet_response.json()["data"]["pet_id"],
        },
    )

    response = client.post(
        "/generate_report",
        json={"from_date": "2020-01-01", "to_date": "2030-01-01"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "success"
    assert "adopted_pet_types" in body["data"]
    assert "weekly_adoption_requests" in body["data"]


def test_get_adoption_requests_endpoint_returns_expected_data(client) -> None:
    pet_response = client.post(
        "/create_pet",
        data={
            "type": "dog",
            "gender": "male",
            "size": "large",
            "age": "adult",
            "good_with_children": "true",
        },
        files=[("photos", ("history-dog.jpg", b"dog", "image/jpeg"))],
    )
    customer_response = client.post(
        "/add_customer",
        json={"name": "Lulit", "phone": "0911556677"},
    )
    client.post(
        "/adopt",
        json={
            "customer_id": customer_response.json()["data"]["customer_id"],
            "pet_id": pet_response.json()["data"]["pet_id"],
        },
    )

    response = client.get(
        "/get_adoption_requests",
        params={"from_date": "2020-01-01", "to_date": "2030-01-01"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "success"
    assert len(body["data"]) >= 1
    assert body["data"][0]["customer_name"] == "Lulit"
