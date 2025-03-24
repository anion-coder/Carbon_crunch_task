from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, List
import os
from .analyzer.python_analyzer import PythonAnalyzer
from .analyzer.javascript_analyzer import JavaScriptAnalyzer

app = FastAPI(title="Code Quality Analyzer")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/analyze-code")
async def analyze_code(file: UploadFile = File(...)) -> Dict:
    """
    Analyze the uploaded code file and return quality metrics and recommendations.
    """
    # Validate file extension
    file_extension = os.path.splitext(file.filename)[1].lower()
    if file_extension not in ['.py', '.js', '.jsx']:
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Only .py, .js, and .jsx files are supported."
        )

    # Read file content
    content = await file.read()
    code = content.decode('utf-8')

    # Select appropriate analyzer based on file type
    if file_extension == '.py':
        analyzer = PythonAnalyzer()
    else:
        analyzer = JavaScriptAnalyzer()

    # Analyze code
    try:
        result = analyzer.analyze(code)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error analyzing code: {str(e)}"
        )

@app.get("/api/health")
async def health_check():
    """
    Health check endpoint
    """
    return {"status": "healthy"} 