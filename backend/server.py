from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from authz_helpers import Authz

app = FastAPI()
authz = Authz()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

books = {
    "1": {"title": "harry potter first book"},
    "2": {"title": "harry potter second book"},
    "3": {"title": "harry potter third book"},
}


@app.get("/books")
def list_books():
    subject = "andrej@loka.com"
    action = "read"
    book_resource_ids = ["book/" + bid for bid in books.keys()]
    filtered_book_ids = authz.filter(subject, action, book_resource_ids)
    filtered_books = []
    for f_id in filtered_book_ids:
        book_id = f_id.replace("book/", "")
        filtered_books.append({"id": book_id, "title": books[book_id]["title"]})
    return filtered_books


@app.get("/books/:id")
def get_one_book(book_id):
    subject = "andrej@loka.com"
    action = "read"
    if authz.can(subject, action, "book/" + book_id):
        return books[book_id]
    else:
        return JSONResponse(content={"error": "403 not allowed"}, status_code=403)
