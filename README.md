# Code Quality Analyzer

A full-stack application that analyzes React (JavaScript) and FastAPI (Python) code files for clean code practices and provides recommendations for improvement.

## Features

- File upload interface for .js, .jsx, and .py files
- Code analysis with scoring across multiple categories:
  - Naming conventions (10 points)
  - Function length and modularity (20 points)
  - Comments and documentation (20 points)
  - Formatting/indentation (15 points)
  - Reusability and DRY (15 points)
  - Best practices in web dev (20 points)
- Detailed recommendations for code improvement
- GitHub Actions integration (optional)

## Project Structure

```
.
├── backend/           # FastAPI backend
│   ├── app/
│   │   ├── main.py
│   │   ├── analyzer/
│   │   │   ├── __init__.py
│   │   │   ├── python_analyzer.py
│   │   │   └── javascript_analyzer.py
│   │   └── utils/
│   │       └── __init__.py
│   ├── requirements.txt
│   └── tests/
├── frontend/         # React frontend
│   ├── src/
│   │   ├── components/
│   │   ├── App.js
│   │   └── index.js
│   ├── package.json
│   └── public/
└── .github/         # GitHub Actions workflow
    └── workflows/
        └── code-quality.yml
```

## Setup Instructions

### Backend Setup

1. Create a virtual environment:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the FastAPI server:
```bash
uvicorn app.main:app --reload
```

### Frontend Setup

1. Install dependencies:
```bash
cd frontend
npm install
```

2. Start the development server:
```bash
npm start
```

## API Endpoints

- POST `/api/analyze-code`: Accepts code file and returns analysis results
  - Request: Multipart form data with file
  - Response: JSON with analysis results

## Usage

1. Open the frontend application in your browser
2. Upload a .js, .jsx, or .py file
3. Submit for analysis
4. View the detailed analysis results and recommendations

## Development

- Backend: FastAPI with Python 3.8+
- Frontend: React with TypeScript
- Code Analysis: Custom analyzers for Python and JavaScript
- Testing: pytest for backend, Jest for frontend

## License

MIT 