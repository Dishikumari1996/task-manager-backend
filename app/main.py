from fastapi import FastAPI, Request
from app.db.database import engine, Base
from app.models.user import User
from app.routes import user_routes
from app.models.task import Task
from app.routes import task_routes
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse


Base.metadata.create_all(bind=engine)

app = FastAPI()
origins = [
    "http://localhost:4200",  # Angular
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
def read_root():
    return {"message": "API is running"}

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "Something went wrong",
            "error": str(exc)
        }
    )

app.include_router(user_routes.router)
app.include_router(task_routes.router)