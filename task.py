## Importing libraries and files
from crewai import Task

from agents import financial_analyst, verifier
from tools import search_tool, financial_document_tool

## Creating a task to help solve user's query
analyze_financial_document = Task(
    description=(
        "Analyze the financial document provided to answer the user's query: {query}\n"
        "Read the financial document carefully using the read_data_tool (the file path is automatically set) to extract relevant information.\n"
        "Provide a comprehensive analysis that includes:\n"
        "- Key financial metrics and ratios\n"
        "- Revenue and profitability trends\n"
        "- Balance sheet analysis\n"
        "- Cash flow assessment\n"
        "- Market position and competitive analysis\n"
        "- Investment insights based on the data\n"
        "Use the search tool to gather additional market context if needed.\n"
        "Ensure all analysis is grounded in the actual data from the document."
    ),

    expected_output=(
        "A comprehensive financial analysis report that includes:\n"
        "- Executive summary of key findings\n"
        "- Detailed analysis of financial metrics\n"
        "- Revenue and profitability analysis\n"
        "- Balance sheet and cash flow insights\n"
        "- Investment recommendations based on the data\n"
        "- Risk assessment\n"
        "- Market outlook and trends\n"
        "The report should be well-structured, accurate, and based on the actual financial document data."
    ),

    agent=financial_analyst,
    tools=[financial_document_tool, search_tool],
    async_execution=False,
)

## Creating an investment analysis task
investment_analysis = Task(
    description=(
        "Conduct a thorough investment analysis based on the financial document data.\n"
        "User query: {query}\n"
        "Analyze key financial metrics including P/E ratios, debt-to-equity, ROE, ROA, and other relevant ratios.\n"
        "Evaluate the company's financial health, growth prospects, and market position.\n"
        "Provide evidence-based investment recommendations considering:\n"
        "- Company valuation metrics\n"
        "- Financial stability and liquidity\n"
        "- Growth potential\n"
        "- Competitive advantages\n"
        "- Risk factors\n"
        "Ensure recommendations are aligned with the actual financial data and market conditions."
    ),

    expected_output=(
        "A structured investment analysis report including:\n"
        "- Company valuation assessment\n"
        "- Key financial ratios analysis\n"
        "- Investment thesis based on financial data\n"
        "- Buy/Hold/Sell recommendation with rationale\n"
        "- Risk factors and considerations\n"
        "- Target price or valuation range (if applicable)\n"
        "- Investment timeline and strategy\n"
        "All recommendations must be supported by data from the financial document."
    ),

    agent=financial_analyst,
    tools=[financial_document_tool, search_tool],
    async_execution=False,
)

## Creating a risk assessment task
risk_assessment = Task(
    description=(
        "Conduct a comprehensive risk assessment based on the financial document.\n"
        "User query: {query}\n"
        "Analyze various risk factors including:\n"
        "- Market risk and volatility\n"
        "- Credit risk and debt levels\n"
        "- Liquidity risk\n"
        "- Operational risk\n"
        "- Regulatory and compliance risks\n"
        "- Industry-specific risks\n"
        "Evaluate the company's risk management practices and financial stability.\n"
        "Provide a balanced assessment that identifies both risks and mitigating factors."
    ),

    expected_output=(
        "A detailed risk assessment report including:\n"
        "- Executive summary of key risks\n"
        "- Quantitative risk metrics (debt ratios, liquidity ratios, etc.)\n"
        "- Qualitative risk factors\n"
        "- Risk rating or score\n"
        "- Risk mitigation strategies\n"
        "- Comparison with industry benchmarks\n"
        "- Recommendations for risk management\n"
        "The assessment should be thorough, accurate, and based on actual financial data."
    ),

    agent=financial_analyst,
    tools=[financial_document_tool, search_tool],
    async_execution=False,
)

    
verification = Task(
    description=(
        "Verify that the uploaded document is a legitimate financial document.\n"
        "Read the document carefully using the read_data_tool to assess:\n"
        "- Document type and format\n"
        "- Presence of financial terminology and metrics\n"
        "- Data quality and completeness\n"
        "- Relevance to financial analysis\n"
        "Provide an accurate assessment of whether the document is suitable for financial analysis."
    ),

    expected_output=(
        "A verification report that includes:\n"
        "- Document type identification\n"
        "- Assessment of financial content relevance\n"
        "- Data quality evaluation\n"
        "- Verification status (approved/rejected/needs review)\n"
        "- Specific observations about the document\n"
        "- Recommendations for document usage\n"
        "The verification should be accurate and based on actual document content."
    ),

    agent=verifier,
    tools=[financial_document_tool],
    async_execution=False
)