from fastapi import FastAPI, UploadFile, File, Query
from fastapi.middleware.cors import CORSMiddleware
from services import comprehensive_report_analysis

app = FastAPI()

origins = [
    "https://v0-salesforce-opprtunity-kehsxnvvjsw.vercel.app",  # Your Vercel frontend without trailing slash
    "https://v0-salesforce-opprtunity-kehsxnvvjsw.vercel.app/",  # Your Vercel frontend with trailing slash
    "http://localhost:3000",  # Allow local development
    "http://localhost:3000/"  # Allow local development with trailing slash
]

# ✅ Add CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allow only frontend requests
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

@app.get("/")
def home():
    return {"message": "Hello from FASTAPI on Fly.io"}

@app.post("/api/analyze")
async def analyze_file(
    file: UploadFile = File(...),
    date_range: str = Query('all', enum=['all', 'ytd', 'q1', 'q2', 'q3', 'q4'])
):
    return await comprehensive_report_analysis(file, date_range)