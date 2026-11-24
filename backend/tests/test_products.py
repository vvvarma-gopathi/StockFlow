def signup_and_get_headers(client, email: str, organization_name: str):
    test_client, _ = client
    signup = test_client.post(
        "/api/auth/signup",
        json={
            "email": email,
            "password": "secure-password",
            "organization_name": organization_name,
        },
    )
    assert signup.status_code == 201

    login = test_client.post(
        "/api/auth/login",
        json={"email": email, "password": "secure-password"},
    )
    assert login.status_code == 200
    return {"Authorization": f"Bearer {login.json()['access_token']}"}


def product_data(**overrides):
    return {
        "name": "Wireless Mouse",
        "sku": "WM-001",
        "description": "Wireless office mouse",
        "quantity_on_hand": 4,
        "cost_price": "12.50",
        "selling_price": "24.99",
        "low_stock_threshold": None,
        **overrides,
    }


def test_product_crud_is_scoped_to_the_authenticated_organization(client):
    test_client, _ = client
    owner_headers = signup_and_get_headers(
        client, "owner@example.com", "Owner Store"
    )
    other_headers = signup_and_get_headers(
        client, "other@example.com", "Other Store"
    )

    created = test_client.post(
        "/api/products",
        json=product_data(),
        headers=owner_headers,
    )
    other_product = test_client.post(
        "/api/products",
        json=product_data(name="Other Mouse"),
        headers=other_headers,
    )

    assert created.status_code == 201
    assert created.json()["organization_id"] != other_product.json()["organization_id"]
    assert created.json()["is_low_stock"] is True
    assert created.json()["effective_low_stock_threshold"] == 5
    assert other_product.status_code == 201

    product_id = created.json()["id"]
    assert len(test_client.get("/api/products", headers=owner_headers).json()) == 1
    assert test_client.get(
        f"/api/products/{product_id}", headers=other_headers
    ).status_code == 404

    update = test_client.put(
        f"/api/products/{product_id}",
        json=product_data(
            name="Wireless Mouse Pro",
            sku="WM-002",
            quantity_on_hand=10,
            low_stock_threshold=9,
        ),
        headers=owner_headers,
    )
    assert update.status_code == 200
    assert update.json()["name"] == "Wireless Mouse Pro"
    assert update.json()["is_low_stock"] is False

    duplicate_sku = test_client.post(
        "/api/products",
        json=product_data(name="Duplicate Mouse", sku="WM-002"),
        headers=owner_headers,
    )
    assert duplicate_sku.status_code == 409

    assert test_client.delete(
        f"/api/products/{product_id}", headers=other_headers
    ).status_code == 404
    assert test_client.delete(
        f"/api/products/{product_id}", headers=owner_headers
    ).status_code == 204
    assert test_client.get(
        f"/api/products/{product_id}", headers=owner_headers
    ).status_code == 404


def test_dashboard_totals_and_low_stock_are_organization_scoped(client):
    test_client, _ = client
    owner_headers = signup_and_get_headers(
        client, "dashboard@example.com", "Dashboard Store"
    )
    other_headers = signup_and_get_headers(
        client, "dashboard-other@example.com", "Another Dashboard Store"
    )

    for data in (
        product_data(name="Default threshold", sku="DEFAULT", quantity_on_hand=5),
        product_data(
            name="Custom threshold",
            sku="CUSTOM",
            quantity_on_hand=5,
            low_stock_threshold=4,
        ),
        product_data(
            name="Zero stock",
            sku="ZERO",
            quantity_on_hand=0,
            low_stock_threshold=0,
        ),
    ):
        response = test_client.post(
            "/api/products",
            json=data,
            headers=owner_headers,
        )
        assert response.status_code == 201

    other_product = test_client.post(
        "/api/products",
        json=product_data(name="Other Product", sku="OTHER", quantity_on_hand=100),
        headers=other_headers,
    )
    assert other_product.status_code == 201

    summary = test_client.get(
        "/api/dashboard/summary",
        headers=owner_headers,
    )
    assert summary.status_code == 200
    assert summary.json()["total_products"] == 3
    assert summary.json()["total_quantity"] == 10
    assert {item["sku"] for item in summary.json()["low_stock_items"]} == {
        "DEFAULT",
        "ZERO",
    }

    other_summary = test_client.get(
        "/api/dashboard/summary",
        headers=other_headers,
    )
    assert other_summary.status_code == 200
    assert other_summary.json()["total_products"] == 1
    assert other_summary.json()["total_quantity"] == 100
    assert other_summary.json()["low_stock_items"] == []


def test_product_routes_require_authentication_and_reject_negative_values(client):
    test_client, _ = client
    assert test_client.get("/api/products").status_code == 401
    assert test_client.get("/api/dashboard/summary").status_code == 401

    headers = signup_and_get_headers(
        client, "validation@example.com", "Validation Store"
    )
    invalid_product = test_client.post(
        "/api/products",
        json=product_data(quantity_on_hand=-1, cost_price="-1"),
        headers=headers,
    )
    assert invalid_product.status_code == 422