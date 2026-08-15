import os
from llm_service import generate_process_model
from db import db

# 1. Ensure your API key is set before running
if not os.environ.get("GROQ_API_KEY"):
    print("WARNING: GROQ_API_KEY environment variable is not set!")
    os.environ["GROQ_API_KEY"] = "GROQ_API_KEY" # Uncomment and add your key for testing if needed

def run_test():
    test_process = "Manual Payroll Processing"
    test_industry = "Finance"
    
    print(f"Sending prompt to Groq for: {test_process}...")
    
    try:
        # Call the LLM service
        generated_model = generate_process_model(test_process, test_industry)
        
        print("\n✅ SUCCESS: Groq returned valid JSON that matches the Pydantic schema!")
        print(f"\n--- Process: {generated_model.process_name} ---")
        
        print("\nCurrent Problems Identified:")
        for problem in generated_model.current_state.problems:
            print(f"- {problem}")
            
        print("\nAI Opportunities Proposed:")
        for opp in generated_model.ai_opportunities:
            print(f"- {opp.title}: {opp.description}")
            
        print("\nExpected Benefits:")
        for benefit in generated_model.expected_benefits:
            print(f"- {benefit.metric}: {benefit.current_value} -> {benefit.future_value}")
        
        # Save the generated model to your local JSON database to prep for Step 3
        db.save(generated_model)
        print("\n✅ Saved generated process to processes.json")

    except Exception as e:
        print(f"\n❌ ERROR: LLM Generation or Validation failed: {e}")

if __name__ == "__main__":
    run_test()