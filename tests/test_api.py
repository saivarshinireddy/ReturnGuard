
def create_test_customer(client):
    response = client.post(
        "/api/v1/customers",
        json={
            "name": "Rahul Sharma",
            "email": "rahul@example.com",
        },
    )

    assert response.status_code == 201
    return response.json()


def create_test_order(client, customer_id):
    response = client.post(
        "/api/v1/orders",
        json={
            "customer_id": customer_id,
            "product_name": "Wireless Headphones",
            "amount": "2499.00",
        },
    )

    assert response.status_code == 201
    return response.json()


# -------------------------
# Health API tests
# -------------------------

def test_health_check(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


# -------------------------
# Customer API tests
# -------------------------

def test_create_customer(client):
    response = client.post(
        "/api/v1/customers",
        json={
            "name": "Rahul Sharma",
            "email": "rahul@example.com",
        },
    )

    assert response.status_code == 201
    assert response.json()["name"] == "Rahul Sharma"


def test_get_customers(client):
    create_test_customer(client)

    response = client.get("/api/v1/customers")

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_duplicate_customer_email(client):
    create_test_customer(client)

    response = client.post(
        "/api/v1/customers",
        json={
            "name": "Another Customer",
            "email": "rahul@example.com",
        },
    )

    assert response.status_code == 409


def test_invalid_customer_email(client):
    response = client.post(
        "/api/v1/customers",
        json={
            "name": "Rahul Sharma",
            "email": "invalid-email",
        },
    )

    assert response.status_code == 422


# -------------------------
# Order API tests
# -------------------------

def test_create_order(client):
    customer = create_test_customer(client)

    order = create_test_order(client, customer["id"])

    assert order["product_name"] == "Wireless Headphones"
    assert order["status"] == "delivered"


def test_get_orders(client):
    customer = create_test_customer(client)
    create_test_order(client, customer["id"])

    response = client.get("/api/v1/orders")

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_order_for_nonexistent_customer(client):
    response = client.post(
        "/api/v1/orders",
        json={
            "customer_id": 9999,
            "product_name": "Keyboard",
            "amount": "1500.00",
        },
    )

    assert response.status_code == 404


# -------------------------
# Return API tests
# -------------------------

def test_create_return_request(client):
    customer = create_test_customer(client)
    order = create_test_order(client, customer["id"])

    response = client.post(
        "/api/v1/returns",
        json={
            "order_id": order["id"],
            "reason": "The headphones are not working.",
        },
    )

    assert response.status_code == 201
    assert response.json()["status"] == "pending"


def test_duplicate_return_request(client):
    customer = create_test_customer(client)
    order = create_test_order(client, customer["id"])

    payload = {
        "order_id": order["id"],
        "reason": "The headphones are not working.",
    }

    first_response = client.post("/api/v1/returns", json=payload)
    second_response = client.post("/api/v1/returns", json=payload)

    assert first_response.status_code == 201
    assert second_response.status_code == 400


def test_get_return_requests(client):
    customer = create_test_customer(client)
    order = create_test_order(client, customer["id"])

    client.post(
        "/api/v1/returns",
        json={
            "order_id": order["id"],
            "reason": "The headphones are not working.",
        },
    )

    response = client.get("/api/v1/returns")

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_short_return_reason(client):
    customer = create_test_customer(client)
    order = create_test_order(client, customer["id"])

    response = client.post(
        "/api/v1/returns",
        json={
            "order_id": order["id"],
            "reason": "Bad",
        },
    )

    assert response.status_code == 422
