from fastapi import FastAPI
import uvicorn

class Piro360rest:
    def __init__(self):
        self.app = FastAPI()

    def start(self):
        @self.app.get("/")
        def read_root():
            return {"message": "Welcome to the SimpleApp REST server"}

        @self.app.get("/items/{item_id}")
        def read_item(item_id: int, q: str = None):
            return {"item_id": item_id, "q": q}

        return self.app

    def run_app(self):
        uvicorn.run(self.start(), host="0.0.0.0", port=8000)
        
if __name__ == "__main__":
    app_instance = Piro360rest()
    uvicorn.run(app_instance.start(), host="0.0.0.0", port=8000)

