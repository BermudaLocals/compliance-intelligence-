from pydantic import BaseModel

class Settings(BaseModel):
    app_name: str = "Compliance Intelligence API"
    api_prefix: str = "/v1"

settings = Settings()
