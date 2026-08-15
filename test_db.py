from models import ProcessModel, CurrentState, FutureState, HumanVsAIResponsibility, AIOpportunity, ExpectedBenefit
from db import db

# 1. Create a dummy process instance
dummy_process = ProcessModel(
    process_name="Accounts Payable Invoice Verification",
    industry="Finance",
    current_state=CurrentState(
        activities=["Receive paper invoice", "Manual entry into SAP", "Manager approval"],
        roles=["Accounts Payable Clerk", "Finance Manager"],
        systems=["SAP ERP", "Paper Records"],
        problems=["High error rate", "3-day approval delay"]
    ),
    ai_opportunities=[
        AIOpportunity(
            title="Intelligent Document Processing",
            target_problem="High error rate",
            technology_type="OCR + LLM",
            description="Extract line items automatically from digital invoices."
        )
    ],
    future_state=FutureState(
        activities=["Automated OCR Extraction", "AI Anomaly Detection", "Manager Sign-off"],
        roles=["AI Ingestion Agent", "Finance Manager"],
        systems=["SAP ERP", "Groq OCR Engine"],
        human_vs_ai=HumanVsAIResponsibility(
            ai_responsibilities=["Extract invoice data", "Match PO numbers", "Flag anomalies"],
            human_responsibilities=["Approve flagged exceptions", "High-value invoice sign-off"]
        )
    ),
    expected_benefits=[
        ExpectedBenefit(
            metric="Processing Time",
            current_value="3 days",
            future_value="15 minutes",
            impact_description="95% reduction in invoice cycle time."
        )
    ],
    reasoning_trace="Test transcript showing reasoning path."
)

# 2. Save to processes.json
db.save(dummy_process)
print(f"Saved process with ID: {dummy_process.id}")

# 3. Retrieve and verify persistence
loaded = db.get_by_id(dummy_process.id)
assert loaded is not None
print(f"Successfully loaded: '{loaded.process_name}' from processes.json")

# 4. Test Query capability
matching_roles = db.search_by_role("Clerk")
print(f"Found {len(matching_roles)} process(es) matching role 'Clerk'.")