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


def test_default_threshold_setting_only_controls_fallback_for_org(client):
    test_client, _ = client
    headers = signup_and_get_headers(
        client, "settings@example.com", "Settings Store"
    )
    other_headers = signup_and_get_headers(
        client, "other-settings@example.com", "Other Settings Store"
    )

    initial_settings = test_client.get("/api/settings", headers=headers)
    assert initial_settings.status_code == 200
    assert initial_settings.json() == {
        "default_low_stock_threshold": 5,
        "default_low_stock_threshold_enabled": True,
    }

    fallback_product = test_client.post(
        "/api/products",
        headers=headers,
        json={
            "name": "Fallback threshold product",
            "sku": "FALLBACK",
            "quantity_on_hand": 4,
        },
    )
    explicit_product = test_client.post(
        "/api/products",
        headers=headers,
        json={
            "name": "Explicit threshold product",
            "sku": "EXPLICIT",
            "quantity_on_hand": 4,
            "low_stock_threshold": 4,
        },
    )
    zero_stock_product = test_client.post(
        "/api/products",
        headers=headers,
        json={
            "name": "Empty fallback product",
            "sku": "EMPTY-FALLBACK",
            "quantity_on_hand": 0,
        },
    )
    assert fallback_product.json()["is_low_stock"] is True
    assert explicit_product.json()["is_low_stock"] is True

    updated = test_client.put(
        "/api/settings",
        headers=headers,
        json={
            "default_low_stock_threshold": 3,
            "default_low_stock_threshold_enabled": False,
        },
    )
    assert updated.status_code == 200
    assert updated.json() == {
        "default_low_stock_threshold": 3,
        "default_low_stock_threshold_enabled": False,
    }

    products = test_client.get("/api/products", headers=headers).json()
    products_by_sku = {product["sku"]: product for product in products}
    assert products_by_sku["FALLBACK"]["effective_low_stock_threshold"] is None
    assert products_by_sku["FALLBACK"]["is_low_stock"] is False
    assert products_by_sku["EXPLICIT"]["effective_low_stock_threshold"] == 4
    assert products_by_sku["EXPLICIT"]["is_low_stock"] is True
    assert products_by_sku["EMPTY-FALLBACK"]["is_low_stock"] is False

    summary = test_client.get("/api/dashboard/summary", headers=headers)
    assert {
        product["sku"] for product in summary.json()["low_stock_items"]
    } == {"EXPLICIT"}
    assert test_client.get(
        "/api/settings",
        headers=other_headers,
    ).json() == {
        "default_low_stock_threshold": 5,
        "default_low_stock_threshold_enabled": True,
    }

    enabled_settings = test_client.put(
        "/api/settings",
        headers=headers,
        json={
            "default_low_stock_threshold": 4,
            "default_low_stock_threshold_enabled": True,
        },
    )
    assert enabled_settings.status_code == 200
    enabled_products = {
        product["sku"]: product
        for product in test_client.get("/api/products", headers=headers).json()
    }
    assert enabled_products["FALLBACK"]["effective_low_stock_threshold"] == 4
    assert enabled_products["FALLBACK"]["is_low_stock"] is True


def test_settings_require_auth_and_reject_negative_threshold(client):
    test_client, _ = client
    assert test_client.get("/api/settings").status_code == 401

    headers = signup_and_get_headers(
        client, "settings-validation@example.com", "Validation Store"
    )
    invalid = test_client.put(
        "/api/settings",
        headers=headers,
        json={
            "default_low_stock_threshold": -1,
            "default_low_stock_threshold_enabled": True,
        },
    )
    assert invalid.status_code == 422
