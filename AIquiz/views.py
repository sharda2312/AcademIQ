from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
import os
import json
from groq import Groq
import re

# Create your views here.
def ai(request):
    
    client = Groq(
        api_key = os.getenv("GROQ_API_KEY"),
    )
    
    question_count = 4
    grade = 5
    topics = "science"
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"""write {question_count} mcq questions for {grade} grade student for {topics} in json format
                json format should be
                        "question": "What do plants use from the sun to make their own food?",
                        "options": [
                        "Sunlight",
                        "Water",
                        "Air",
                        "Soil"
                        ],
                        "correct": "1"
                    """,
            }
        ],
        model="deepseek-r1-distill-llama-70b",
    )

    # Get AI-generated response
    ai_response = chat_completion.choices[0].message.content

    try:
        # Extract the JSON part using regex
        match = re.search(r"\[\s*{.*}\s*\]", ai_response, re.DOTALL)
        if match:
            json_string = match.group(0)  # Extract JSON content
            questions_data = json.loads(json_string)  # Convert to Python list
            return render(request, 'ai.html', {"questions":questions_data})
        else:
            return HttpResponse("Could not extract JSON from AI response", status=500)

    except json.JSONDecodeError:
        return HttpResponse("Invalid JSON received from AI", status=500)