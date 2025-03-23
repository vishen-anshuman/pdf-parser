from fastapi import FastAPI

from route_table.pdf_routes import router

app = FastAPI()

# Register API routes
app.include_router(router)
