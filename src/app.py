from robyn import Robyn
from config.env import settings 

app = Robyn(__file__)

@app.get("/")
def main():
    return {"message": "Hello!"}

app.start(
    port=settings.APP_PORT,
    host=settings.APP_HOST
)
