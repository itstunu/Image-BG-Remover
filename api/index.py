from fastapi import FastAPI, UploadFile, File, Response, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import io

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load rembg ONLY when first request comes (lazy loading)
_session = None

def get_session():
    global _session
    if _session is None:
        from rembg import new_session
        # Use the tiny "u2netp" model (only ~4.7 MB!)
        _session = new_session("u2netp")
    return _session

@app.get("/api/")
def read_root():
    return {"message": "Background Remover API is running"}

@app.post("/api/remove-bg")
async def remove_background(image: UploadFile = File(...)):
    try:
        from rembg import remove
        
        input_data = await image.read()
        session = get_session()
        
        output_data = remove(input_data, session=session)
        
        return Response(content=output_data, media_type="image/png")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")