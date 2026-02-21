## Importing libraries and files
import os
from dotenv import load_dotenv
load_dotenv()

from crewai_tools import SerperDevTool
from langchain_community.document_loaders import PyPDFLoader
from crewai.tools import BaseTool


## Creating search tool
search_tool = SerperDevTool()


## Creating custom pdf reader helper
class FinancialDocumentTool:
    @staticmethod
    def read_data(path: str | None = None) -> str:
        """Read and clean text from a financial PDF document.

        Args:
            path: Path of the pdf file. If not provided, reads from
                  FINANCIAL_DOCUMENT_PATH env variable or defaults to 'data/sample.pdf'.

        Returns:
            Full cleaned text content of the financial document.
        """
        # Get file path from parameter, environment variable, or default
        if path is None:
            path = os.getenv("FINANCIAL_DOCUMENT_PATH", "data/sample.pdf")

        loader = PyPDFLoader(file_path=path)
        docs = loader.load()

        full_report = ""
        for data in docs:
            content = data.page_content or ""

            # Remove extra blank lines
            while "\n\n" in content:
                content = content.replace("\n\n", "\n")

            full_report += content + "\n"

        return full_report


## CrewAI-compatible Financial Document Tool
class FinancialDocumentReaderTool(BaseTool):
    name: str = "financial_document_reader"
    description: str = (
        "Reads and cleans text from a financial PDF document. "
        "The file path is taken from the FINANCIAL_DOCUMENT_PATH environment "
        "variable unless an explicit path is provided."
    )

    def _run(self, path: str | None = None) -> str:
        return FinancialDocumentTool.read_data(path)


financial_document_tool = FinancialDocumentReaderTool()


## Creating Investment Analysis Tool
class InvestmentTool:
    @staticmethod
    def analyze_investment_tool(financial_document_data):
        """
        Analyze financial document data for investment opportunities.
        """
        processed_data = financial_document_data

        i = 0
        while i < len(processed_data):
            if processed_data[i:i+2] == "  ":
                processed_data = processed_data[:i] + processed_data[i+1:]
            else:
                i += 1

        return (
            f"Investment Analysis:\n{processed_data[:500]}...\n\n"
            "Note: Full investment analysis requires detailed financial modeling."
        )


## Creating Risk Assessment Tool
class RiskTool:
    @staticmethod
    def create_risk_assessment_tool(financial_document_data):
        """
        Assess risks from financial document data.
        """
        return (
            f"Risk Assessment:\n"
            f"Analyzed document length: {len(financial_document_data)} characters.\n\n"
            "Note: Full risk assessment requires detailed quantitative analysis of financial metrics."
        )