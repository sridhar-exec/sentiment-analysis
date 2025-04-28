def get_prompt_template(conversation_type="monologue"):
    if conversation_type == "conversation":
        return """You are a senior conversation analysis expert for customer service calls.

Given the following transcript:
{transcript_text}

Please provide a detailed analysis including:
- A clear and concise summary of the conversation.
- The main concerns or issues raised by the customer.
- How the agent responded to the customer's concerns.
- Overall sentiment of the customer (positive, negative, neutral).
- Risk of escalation (low, medium, high) and why.
- Actionable suggestions to improve future customer experiences.

Focus on being accurate, structured, and insightful."""
    else:  # monologue
        return """You are a senior analyst specialized in voicemail and monologue evaluation for businesses.

Given the following transcript:
{transcript_text}

Please extract and structure the following:
- The speaker's key points and topics discussed.
- Overall sentiment (positive, negative, or neutral).
- Any specific complaints, issues, or requests mentioned.
- Actionable recommendations for improving service based on the content.

Limit your response to 250–300 words. Ensure clarity, precision, and actionable insights."""