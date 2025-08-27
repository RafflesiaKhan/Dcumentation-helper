# FastAPI Documentation Sample

## Getting Started

FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints.

### Key Features

- **Fast**: Very high performance, on par with NodeJS and Go
- **Fast to code**: Increase the speed to develop features by about 200% to 300%
- **Fewer bugs**: Reduce about 40% of human (developer) induced errors
- **Intuitive**: Great editor support. Completion everywhere. Less time debugging
- **Easy**: Designed to be easy to use and learn. Less time reading docs
- **Short**: Minimize code duplication. Multiple features from each parameter declaration
- **Robust**: Get production-ready code. With automatic interactive documentation

## Installation

Install FastAPI with pip:

```bash
pip install fastapi
```

You'll also need an ASGI server for production such as Uvicorn:

```bash
pip install "uvicorn[standard]"
```

## First Steps

Create a file `main.py` with:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}
```

Run the server with:

```bash
uvicorn main:app --reload
```

## API Documentation

FastAPI automatically generates interactive API documentation:

- **Swagger UI**: Available at `http://127.0.0.1:8000/docs`
- **ReDoc**: Available at `http://127.0.0.1:8000/redoc`

## Path Parameters

You can declare path parameters with the same syntax used by Python format strings:

```python
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}
```

## Query Parameters

Query parameters are automatically parsed when they are not part of the path parameters:

```python
@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}
```

## Request Body

You can declare request bodies using Pydantic models:

```python
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: float
    is_offer: bool = None

@app.post("/items/")
async def create_item(item: Item):
    return item
```

## Configuration

FastAPI provides several configuration options:

### Environment Variables

- `DEBUG`: Enable debug mode
- `HOST`: Server host (default: 127.0.0.1)
- `PORT`: Server port (default: 8000)

### Settings

Use Pydantic Settings for configuration management:

```python
from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = "My FastAPI App"
    debug: bool = False
    
    class Config:
        env_file = ".env"

settings = Settings()
```

## Database Integration

FastAPI works well with any database. Here's an example with SQLAlchemy:

```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
```

## Testing

FastAPI provides excellent testing support:

```python
from fastapi.testclient import TestClient

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}
```

## Deployment

### Production Considerations

- Use a production ASGI server like Uvicorn or Hypercorn
- Configure proper logging
- Set up error monitoring
- Use environment variables for configuration
- Implement proper security measures

### Docker Deployment

```dockerfile
FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
```

## Security

FastAPI provides several security utilities:

### OAuth2 with JWT

```python
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/users/me")
async def read_users_me(token: str = Depends(oauth2_scheme)):
    return decode_token(token)
```

### CORS

Enable CORS for frontend integration:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Best Practices

1. **Use Type Hints**: Always use Python type hints for better IDE support
2. **Validate Input**: Use Pydantic models for request/response validation
3. **Handle Errors**: Implement proper error handling with HTTP exceptions
4. **Document APIs**: Use docstrings and tags for better documentation
5. **Test Everything**: Write comprehensive tests for all endpoints
6. **Monitor Performance**: Use profiling tools to optimize bottlenecks

## Common Patterns

### Dependency Injection

```python
from fastapi import Depends

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/items/")
async def read_items(db: Session = Depends(get_db)):
    return db.query(Item).all()
```

### Background Tasks

```python
from fastapi import BackgroundTasks

def write_notification(email: str, message=""):
    with open("log.txt", mode="w") as email_file:
        content = f"notification for {email}: {message}"
        email_file.write(content)

@app.post("/send-notification/")
async def send_notification(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(write_notification, email, message="notification")
    return {"message": "Notification sent in the background"}
```

## Troubleshooting

### Common Issues

1. **Import Errors**: Check Python path and virtual environment
2. **Port Already in Use**: Use different port or kill existing process
3. **CORS Errors**: Configure CORS middleware properly
4. **Validation Errors**: Check Pydantic model definitions

### Performance Tips

- Use async/await for I/O operations
- Implement connection pooling for databases
- Use caching for expensive operations
- Monitor and profile your application

