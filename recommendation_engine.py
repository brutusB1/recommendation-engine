import pandas as pd
from openai import OpenAI
from typing import Dict
import os
# Load mock data
DATA_PATH = "expanded_mock_data.csv"
data = pd.read_csv(DATA_PATH)


# Initialize OpenAI client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def generate_recommendation(api_key: str, prospect_data: Dict, transcript: str = None) -> Dict:
    prompt = f"""
You are an AI assistant for a senior living sales representative. Your task is to provide actionable, personalized recommendations to engage with a prospect by leveraging selfie-style video content. Focus on creating scripts that feel warm, authentic, and tailored to the prospect's interests and engagement level. Consider the following details:

- Prospect Name: {prospect_data['name']}
- Video Title: "{prospect_data['video_title']}"
- Engagement Details:
  - Watch Percentage: {prospect_data['watch_percentage']}%
  - Rewatch Count: {prospect_data.get('rewatch_count', 0)}
  - Call-to-Action Clicked: {prospect_data['cta_clicked'] or 'None'}

Video Transcript: "{transcript or 'No transcript provided'}"

Your tasks:
1. Analyze the engagement data and transcript to provide **insights** into the prospect's interests, preferences, and potential needs.
2. Suggest **next steps** for the sales representative to take, focusing on using personalized selfie-style videos to strengthen the relationship.
3. Write a **ready-to-record video script** for the sales representative. The script should:
   - Be engaging and warm.
   - Address the prospect by name.
   - Reference specific details from their engagement and transcript.
   - Include a clear call-to-action (e.g., scheduling a tour, asking a question, etc.).
4. Write a **ready-to-use comment** for the sales rep to post on the video to re-engage the prospect. The comment should:
   - Be short and friendly.
   - Reference the video content or prospect's interest.
   - Invite further interaction (e.g., a question or follow-up suggestion).
5. Write a **call script** for a follow-up conversation. The script should:
   - Be professional yet friendly.
   - Reference the prospect's engagement with the video.
   - Include specific topics to discuss and a clear goal for the call (e.g., scheduling a tour, answering questions).

Structure your response as follows:
- Insights:
  - [Bullet points with insights about the prospect’s engagement and interests]
- Next Steps:
  - [Bullet points with recommended actions]
- Video Script:
  - Hi [Prospect Name], [Introduce yourself briefly].
  - Reference their recent engagement (e.g., "I saw that you watched our video about [Video Title]"). 
  - Highlight a key point or feature mentioned in the transcript or engagement (e.g., "I think you'd love our upcoming [event/tour].").
  - End with a strong, inviting CTA (e.g., "I'd love to show you around our community—let me know a time that works best for you!").
- Comment:
  - [A short, friendly comment to post on the video]
- Call Script:
  - [A concise, professional script for a follow-up call]
"""
    try:
        client = OpenAI(api_key=api_key)
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="gpt-4o",
            max_tokens=700,  # Increased for additional outputs
            temperature=0.8,  # Slightly higher for creative output
        )
        response_text = chat_completion.choices[0].message.content.strip()

        # Return the raw response for debugging
        return {"response_text": response_text}
    except Exception as e:
        return {"error": f"Error: {str(e)}"}

def get_prospect_data(name: str):
    """
    Fetch prospect data by name from the dataset.
    """
    row = data[data["Prospect Name"] == name]
    if row.empty:
        return None
    row = row.iloc[0]
    return {
        "name": row["Prospect Name"],
        "video_title": row["Video Title"],
        "watch_percentage": row["Watch Percentage"],
        "cta_clicked": row["CTA Clicked"],
    }