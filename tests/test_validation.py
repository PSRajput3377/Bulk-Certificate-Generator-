def test_empty_recipients(client):
    response = client.post(
        "/jobs",
        json={
            "course_name": "Python Bootcamp",
            "recipients": [],
        },
    )

    assert response.status_code == 422


def test_invalid_email(client):
    response = client.post(
        "/jobs",
        json={
            "course_name": "Python Bootcamp",
            "recipients": [
                {
                    "name": "Prashant Singh",
                    "email": "invalid-email",
                }
            ],
        },
    )

    assert response.status_code == 422


def test_empty_recipient_name(client):
    response = client.post(
        "/jobs",
        json={
            "course_name": "Python Bootcamp",
            "recipients": [
                {
                    "name": "",
                    "email": "prashant@example.com",
                }
            ],
        },
    )

    assert response.status_code == 422


def test_empty_course_name(client):
    response = client.post(
        "/jobs",
        json={
            "course_name": "",
            "recipients": [
                {
                    "name": "Prashant Singh",
                    "email": "prashant@example.com",
                }
            ],
        },
    )

    assert response.status_code == 422