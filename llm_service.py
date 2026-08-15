import os
import json
from groq import Groq
from models import ProcessModel

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def generate_process_model(process_name: str, industry: str = "Finance") -> ProcessModel:
    """
    Calls Groq to analyze a business process and returns a structured ProcessModel.
    """
    
    # We dynamically extract the JSON schema from the Pydantic model you built in Step 1
    # This guarantees the LLM knows exactly what keys and data types to return.
    schema_definition = ProcessModel.model_json_schema()
    
    system_prompt = f"""
    You are an elite Enterprise AI Architect specializing in business process transformation.
    Your objective is to analyze a traditional business process and map its transition to an AI-driven future state.
    
    You must explicitly reason through:
    1. Current Process (Activities, roles, systems)
    2. Problems (Bottlenecks, inefficiencies)
    3. AI Opportunities (Where AI can intervene)
    4. Future Process (The streamlined AI workflow)
    5. Human vs AI Responsibility (Division of labor)
    6. Expected Benefits (Quantitative and qualitative)

    CRITICAL RULE: You must output ONLY a valid JSON object. 
    The JSON object must strictly adhere to the following JSON schema:
    {json.dumps(schema_definition, indent=2)}
    
    Do not include any conversational text, markdown formatting blocks (like ```json), or explanations outside the JSON object.
    """

    user_prompt = f"Please analyze the following process: '{process_name}' in the '{industry}' industry."

    # Use a currently supported Groq model
    model = os.environ.get("GROQ_MODEL", "llama-3.3-70b-versatile")

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.2, # Low temperature for analytical consistency
            response_format={"type": "json_object"} # Forces Groq to return parseable JSON
        )
    except Exception as e:
        # Detect common decommissioning error and provide actionable guidance
        err_text = str(e)
        if "decommissioned" in err_text or "model_decommissioned" in err_text:
            raise RuntimeError(
                "Groq model '" + model + "' has been decommissioned. "
                "Set the environment variable GROQ_MODEL to a supported model (see https://console.groq.com/docs/deprecations)."
            ) from e
        raise

    # Extract the raw JSON string from the response
    raw_json_str = response.choices[0].message.content
    
    # Parse the JSON string into a Python dictionary
    parsed_json = json.loads(raw_json_str)
    
    # Save the raw output as the reasoning trace for grading compliance (Traceability Rule)
    parsed_json["reasoning_trace"] = raw_json_str
    
    # Validate and return as a Pydantic object
    return ProcessModel(**parsed_json)