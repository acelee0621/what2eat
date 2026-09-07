from pydantic import BaseModel


class WeatherResponse(BaseModel):
    城市: str
    最低气温: str
    最高气温: str
    天气: str
