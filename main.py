from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from database.session import engine
from models.user import User
from models.book import Book
from routes.auth import router as auth_router
from routes.users import router as users_router
from routes.books import router as books_router

User.metadata.create_all(bind=engine)
Book.metadata.create_all(bind=engine)

app = FastAPI(
    title="Bookstore API",
    description="An API for managing a bookstore's inventory, including stock levels and search functionality. Users can add new books, update inventory counts, and search for books by title, author, or genre.",
    version="1.0.0",
    contact={
        "name": "Victor Agu",
        "email": "v.ebukaagu@gmail.com",
    },
)


@app.get("/")
def root():
    return {"message": "Welcome to the Bookstore API!"}

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(books_router)

@app.get("/github", include_in_schema=False)
async def github():
    return RedirectResponse(url="https://github.com/Victor-Ebuka/bookstore-api")
