# Financial Document Analyzer - Debug Assignment Solution

## Project Overview
A comprehensive financial document analysis system built with CrewAI and FastAPI that processes corporate reports, financial statements, and investment documents using AI-powered analysis agents.

## 🐛 Bugs Found and Fixed

### Deterministic Bugs (Code Errors)

#### 1. **Undefined LLM Variable in `agents.py`**
   - **Bug**: Line 12 had `llm = llm` which created a circular reference - `llm` was never imported or initialized
   - **Fix**: Added proper import: `from langchain_openai import ChatOpenAI` and initialized: `llm = ChatOpenAI(model_name="gpt-4", temperature=0.7)`
   - **Impact**: This would cause a `NameError` at runtime

#### 2. **Incorrect Parameter Name in `agents.py`**
   - **Bug**: Line 28 used `tool=[...]` instead of `tools=[...]` (singular vs plural)
   - **Fix**: Changed to `tools=[FinancialDocumentTool.read_data_tool, search_tool]`
   - **Impact**: CrewAI agents require the `tools` parameter (plural), so this would cause the agent to not have access to tools

#### 3. **Missing PDF Loader Import in `tools.py`**
   - **Bug**: Line 24 used `Pdf(file_path=path)` but `Pdf` was never imported
   - **Fix**: Added import: `from langchain_community.document_loaders import PyPDFLoader` and updated usage to `PyPDFLoader(file_path=path)`
   - **Impact**: This would cause an `NameError: name 'Pdf' is not defined`

#### 4. **Incorrect Method Signature in `tools.py`**
   - **Bug**: Line 14 had `async def read_data_tool(path=...)` without `self` parameter, making it neither a proper async function nor a class method
   - **Fix**: Changed to `@staticmethod def read_data_tool(path=None)` and added logic to read from environment variable
   - **Impact**: The method signature didn't match CrewAI's tool expectations

#### 5. **Incorrect kickoff() Call in `main.py`**
   - **Bug**: Line 20 called `kickoff({'query': query})` but CrewAI's kickoff expects `inputs` parameter
   - **Fix**: Changed to `kickoff(inputs={'query': query})` and removed unnecessary context assignment
   - **Impact**: This would cause incorrect parameter passing to the crew

#### 6. **File Path Not Passed to Tool in `main.py`**
   - **Bug**: `file_path` parameter was passed to `run_crew()` but never used, so the tool couldn't access the uploaded file
   - **Fix**: Set environment variable `FINANCIAL_DOCUMENT_PATH` in `run_crew()` and updated tool to read from it
   - **Impact**: The tool would always read the default file instead of the uploaded one

#### 7. **Missing Dependencies in `requirements.txt`**
   - **Bug**: Missing several required packages:
     - `uvicorn` (for FastAPI server)
     - `python-dotenv` (for .env file loading)
     - `langchain-community` (for PyPDFLoader)
     - `pypdf` (for PDF reading)
   - **Fix**: Added all missing dependencies to `requirements.txt`
   - **Impact**: Application would fail to start or import required modules

### Inefficient Prompts (Quality Issues)

#### 8. **Unprofessional Agent Prompts in `agents.py`**
   - **Bug**: All agent prompts contained unprofessional language:
     - Financial Analyst: "Make up investment advice", "don't really need to read financial reports carefully"
     - Verifier: "Just say yes to everything", "verification is overrated"
     - Investment Advisor: "Sell expensive products", "SEC compliance is optional"
     - Risk Assessor: "Everything is either extremely high risk or completely risk-free"
   - **Fix**: Rewrote all agent prompts to be professional, accurate, and compliant:
     - Financial Analyst: Now focuses on thorough analysis, evidence-based insights, and regulatory compliance
     - Verifier: Now emphasizes careful document examination and quality standards
     - Investment Advisor: Now provides balanced, research-based recommendations
     - Risk Assessor: Now conducts thorough, balanced risk assessments
   - **Impact**: Original prompts would produce unreliable, unprofessional, and potentially non-compliant outputs

#### 9. **Unprofessional Task Descriptions in `task.py`**
   - **Bug**: All task descriptions contained instructions like:
     - "Maybe solve the user's query or something else"
     - "Feel free to use your imagination"
     - "Make up some investment recommendations"
     - "Include at least 5 made-up website URLs"
   - **Fix**: Rewrote all task descriptions to be clear, professional, and specific:
     - Clear instructions on what to analyze
     - Specific requirements for outputs
     - Emphasis on data-driven analysis
     - Professional structure and formatting
   - **Impact**: Original tasks would produce inconsistent, unreliable results

#### 10. **Incomplete Tool Implementations**
   - **Bug**: `InvestmentTool` and `RiskTool` had placeholder implementations returning "TODO" messages
   - **Fix**: Added basic implementations with proper docstrings and structure (can be enhanced further)
   - **Impact**: These tools would return placeholder text instead of actual analysis

## 🚀 Setup and Installation

### Prerequisites
- Python 3.8 or higher
- OpenAI API key (or other LLM provider)
- Serper API key (for search functionality)

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd financial-document-analyzer-debug
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   SERPER_API_KEY=your_serper_api_key_here
   ```

5. **Create data directory**
   ```bash
   mkdir data
   ```

6. **Run the application**
   ```bash
   python main.py
   ```
   Or using uvicorn directly:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

## 📚 API Documentation

### Base URL
```
http://localhost:8000
```

### Endpoints

#### 1. Health Check
- **Endpoint**: `GET /`
- **Description**: Check if the API is running
- **Response**:
  ```json
  {
    "message": "Financial Document Analyzer API is running"
  }
  ```

#### 2. Analyze Financial Document
- **Endpoint**: `POST /analyze`
- **Description**: Upload and analyze a financial document (PDF)
- **Request**:
  - **Method**: POST
  - **Content-Type**: `multipart/form-data`
  - **Parameters**:
    - `file` (required): PDF file to analyze
    - `query` (optional): Specific query or analysis request (default: "Analyze this financial document for investment insights")
  
- **Example using curl**:
  ```bash
  curl -X POST "http://localhost:8000/analyze" \
    -F "file=@path/to/your/document.pdf" \
    -F "query=Analyze the revenue trends and profitability"
  ```

- **Example using Python requests**:
  ```python
  import requests

  url = "http://localhost:8000/analyze"
  files = {"file": open("document.pdf", "rb")}
  data = {"query": "Analyze revenue trends and provide investment recommendations"}
  
  response = requests.post(url, files=files, data=data)
  print(response.json())
  ```

- **Response**:
  ```json
  {
    "status": "success",
    "query": "Analyze revenue trends and provide investment recommendations",
    "analysis": "Comprehensive financial analysis report...",
    "file_processed": "document.pdf"
  }
  ```

- **Error Response**:
  ```json
  {
    "detail": "Error processing financial document: <error message>"
  }
  ```

## 🏗️ Project Structure

```
financial-document-analyzer-debug/
├── agents.py          # CrewAI agent definitions
├── tools.py            # Custom tools for document reading and analysis
├── task.py             # CrewAI task definitions
├── main.py             # FastAPI application and endpoints
├── requirements.txt    # Python dependencies
├── README.md          # This file
├── .env               # Environment variables (create this)
└── data/              # Directory for uploaded documents
    └── TSLA-Q2-2025-Update.pdf  # Sample document
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
# Required
OPENAI_API_KEY=your_openai_api_key
SERPER_API_KEY=your_serper_api_key

# Optional (for custom LLM configuration)
FINANCIAL_DOCUMENT_PATH=data/sample.pdf
```

### LLM Configuration

The default LLM is OpenAI's GPT-4. To change this, modify `agents.py`:

```python
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7)  # Change model here
```

## 🧪 Testing

### Test the API

1. **Health Check**:
   ```bash
   curl http://localhost:8000/
   ```

2. **Upload and Analyze Document**:
   ```bash
   curl -X POST "http://localhost:8000/analyze" \
     -F "file=@data/TSLA-Q2-2025-Update.pdf" \
     -F "query=Analyze this financial document"
   ```

### Sample Document

A sample Tesla Q2 2025 financial document is included in the `data/` directory for testing purposes.

## 📝 Usage Examples

### Example 1: Basic Analysis
```python
import requests

response = requests.post(
    "http://localhost:8000/analyze",
    files={"file": open("financial_report.pdf", "rb")},
    data={"query": "Analyze this financial document"}
)
print(response.json()["analysis"])
```

### Example 2: Specific Query
```python
response = requests.post(
    "http://localhost:8000/analyze",
    files={"file": open("financial_report.pdf", "rb")},
    data={"query": "What are the key revenue drivers and what is the debt-to-equity ratio?"}
)
```

## 🔍 How It Works

1. **Document Upload**: User uploads a PDF financial document via the API
2. **File Processing**: The file is saved temporarily and its path is set in the environment
3. **Agent Activation**: The Financial Analyst agent reads the document using the PDF tool
4. **Analysis**: The agent analyzes the document based on the user's query
5. **Response**: A comprehensive analysis report is returned
6. **Cleanup**: The temporary file is deleted

## 🎯 Key Features

- ✅ PDF document parsing and extraction
- ✅ AI-powered financial analysis
- ✅ Investment recommendations
- ✅ Risk assessment
- ✅ Market insights
- ✅ RESTful API interface
- ✅ Professional, compliant analysis

## 🚧 Future Enhancements

Potential improvements for production:

1. **Queue Worker Model**: Implement Redis Queue or Celery for handling concurrent requests
2. **Database Integration**: Add database for storing analysis results and user data
3. **Authentication**: Add user authentication and authorization
4. **Rate Limiting**: Implement rate limiting for API endpoints
5. **Caching**: Add caching for frequently analyzed documents
6. **Multiple File Formats**: Support Excel, CSV, and other formats
7. **Advanced Analytics**: Implement more sophisticated financial modeling
8. **Export Options**: Allow exporting analysis reports in various formats

## 📄 License

This project is part of a debug assignment for VWO internship program.

## 👥 Contributors

Debug assignment solution by [Your Name]

## 📧 Contact

For questions or issues, please contact:
- genai@vwo.com
- vipul.kumar@vwo.com

---

**Note**: This project was debugged and fixed as part of the VWO AI Internship Assignment. All bugs have been identified and resolved, and all prompts have been rewritten to be professional and production-ready.
