# tests/test_books.py
def test_books_crud(client):
    # create
    payload = {
        "title": "Test Driven Development",
        "author": "Kent Beck",
        "description": "TDD book",
        "year": 2002,
    }
    r = client.post("/books/", json=payload)
    assert r.status_code == 200
    created = r.json()
    assert created["title"] == payload["title"]
    book_id = created["id"]

    # get list
    r2 = client.get("/books/")
    assert r2.status_code == 200
    arr = r2.json()
    assert any(b["id"] == book_id for b in arr)

    # get detail
    r3 = client.get(f"/books/{book_id}")
    assert r3.status_code == 200
    assert r3.json()["author"] == payload["author"]

    # update
    update_payload = {"title": "TDD - Refactor", "author": "K. Beck"}
    r4 = client.put(f"/books/{book_id}", json=update_payload)
    assert r4.status_code == 200
    assert r4.json()["title"] == update_payload["title"]

    # delete
    r5 = client.delete(f"/books/{book_id}")
    assert r5.status_code == 200
    assert r5.json()["message"] == "Book deleted successfully"
