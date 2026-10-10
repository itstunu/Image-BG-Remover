from fastapi import FastAPI, UploadFile, File, Response
from fastapi.middleware.cors import CORSMiddleware
from rembg import remove
import io

app = FastAPI()

# Allow your frontend to communicate with the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins. You can restrict this later.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Background Remover API is running"}

@app.post("/api/remove-bg")
async def remove_background(image: UploadFile = File(...)):
    # Read the uploaded image file
    input_data = await image.read()
    
    # Process the image with rembg to remove the background
    output_data = remove(input_data)
    
    # Return the result as a PNG file
    return Response(content=output_data, media_type="image/png")