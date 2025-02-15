from fastapi import FastAPI, UploadFile, File, Query
from fastapi.middleware.cors import CORSMiddleware
from services import comprehensive_report_analysis

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/analyze")
async def analyze_file(
    file: UploadFile = File(...),
    date_range: str = Query('all', enum=['all', 'ytd', 'q1', 'q2', 'q3', 'q4'])
):
    return await comprehensive_report_analysis(file, date_range)