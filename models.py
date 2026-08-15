import uuid
from datetime import datetime, timezone
from typing import List, Dict, Optional
from pydantic import BaseModel, Field


class CurrentState(BaseModel):
    activities: List[str] = Field(
        ..., 
        description="Sequential list of current manual activities/steps",
        examples=[["Receive PDF invoice via email", "Manually enter data into ERP", "Send for manager signature"]]
    )
    roles: List[str] = Field(
        ..., 
        description="Human job titles involved in the current state",
        examples=[["Accounts Payable Clerk", "Finance Manager"]]
    )
    systems: List[str] = Field(
        ..., 
        description="Legacy tools, software, or paper systems currently used",
        examples=[["Legacy ERP", "Email", "Excel"]]
    )
    problems: List[str] = Field(
        ..., 
        description="Bottlenecks, error rates, delays, or compliance risks",
        examples=[["Data entry errors cause payment delays", "Manual approvals take 3-5 days"]]
    )


class AIOpportunity(BaseModel):
    title: str = Field(..., description="Short name of the AI intervention")
    target_problem: str = Field(..., description="Which current problem this addresses")
    technology_type: str = Field(..., description="e.g., OCR, LLM Agent, Computer Vision, Anomaly Detection")
    description: str = Field(..., description="Detailed explanation of how technology transforms the step")


class HumanVsAIResponsibility(BaseModel):
    ai_responsibilities: List[str] = Field(
        ..., 
        description="Tasks fully automated or orchestrated by AI agents"
    )
    human_responsibilities: List[str] = Field(
        ..., 
        description="High-level oversight, exception handling, and strategic decision making"
    )


class FutureState(BaseModel):
    activities: List[str] = Field(
        ..., 
        description="New streamlined sequence of steps in the AI-driven process"
    )
    roles: List[str] = Field(
        ..., 
        description="Transformed or new roles required in the future state"
    )
    systems: List[str] = Field(
        ..., 
        description="New stack including AI models, APIs, and modern platforms"
    )
    human_vs_ai: HumanVsAIResponsibility = Field(
        ..., 
        description="Division of responsibility between automation and human workers"
    )


class ExpectedBenefit(BaseModel):
    metric: str = Field(..., description="e.g., Processing Time, Error Rate, Cost per Invoice")
    current_value: str = Field(..., description="Baseline value in current state")
    future_value: str = Field(..., description="Projected value in future state")
    impact_description: str = Field(..., description="Qualitative summary of business impact")


class ProcessModel(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    process_name: str = Field(..., description="Name of the business process (e.g., Accounts Payable Invoice Processing)")
    industry: str = Field(default="Finance", description="Target industry segment")
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    
    # Core reasoning chain steps
    current_state: CurrentState
    ai_opportunities: List[AIOpportunity]
    future_state: FutureState
    expected_benefits: List[ExpectedBenefit]
    
    # Traceability feature requirement
    reasoning_trace: Optional[str] = Field(
        None, 
        description="Raw AI generation transcript or logic chain justifying the transformation"
    )


class ProcessCreateRequest(BaseModel):
    process_name: str = Field(..., description="Name or brief description of the process to re-engineer")
    industry: Optional[str] = Field(default="Finance", description="Industry context")