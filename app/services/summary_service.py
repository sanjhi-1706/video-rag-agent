from app.services.qa_service import generate_answer

def generate_summary(text, query_type="general"):
    
    if query_type == "beginner":
        instruction = "Explain in very simple terms like teaching a beginner."
    
    elif query_type == "exam":
        instruction = "Give structured key points useful for exam preparation."
    
    elif query_type == "detailed":
        instruction = "Give a detailed explanation with all important concepts."
    
    elif query_type == "bullets":
        instruction = "Summarize in concise bullet points."
    
    else:
        instruction = "Give a general concise summary."

    prompt = f"""
    {instruction}

    Content:
    {text[:3000]}
    """

    return generate_answer(text[:3000], prompt)