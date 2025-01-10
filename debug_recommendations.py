from recommendation_engine import generate_recommendation, get_prospect_data
import os

# Mock a recommendation for debugging
if __name__ == "__main__":
    api_key = os.getenv("OPENAI_API_KEY")
    prospect_name = "Tom Thomas"  # Replace with a name from your dataset

    prospect_data = get_prospect_data(prospect_name)
    if not prospect_data:
        print(f"Error: Prospect {prospect_name} not found.")
    else:
        recommendation = generate_recommendation(api_key, prospect_data)
        print("Prospect Data:", prospect_data)
        print("Generated Recommendation:", recommendation)