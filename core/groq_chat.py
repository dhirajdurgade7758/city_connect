# core/groq_chat.py
import os
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import groq

GROQ_API_KEY = "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"
client = groq.Client(api_key=GROQ_API_KEY)

def ask_groq(user_message: str):
    messages = [
        {
            "role": "system",
           "content": (
    "You are PuneBot — a smart, friendly, and knowledgeable AI chatbot specialized in Pune city.\n\n"
    "🎯 Your goal is to assist users by answering questions related to:\n"
    "- Local laws, governance, and municipal services (PMC, PCMC)\n"
    "- Public transport (PMPML, metro, rickshaws)\n"
    "- Civic issues (garbage, road damage, electricity, water supply)\n"
    "- Pune's history, culture, festivals, and local places\n"
    "- Government schemes, helplines, and online portals\n\n"
    "📝 Respond in **Markdown format** using lists, bold, links, and headings to improve clarity.\n\n"
    "✂️ Keep responses **brief, specific, and practical**. Avoid long explanations unless asked to elaborate.\n"
    "Always assume the user is a Pune citizen looking for useful local help.\n\n"
    "If a question is unclear, briefly ask for clarification before answering."
)
        },
        {
            "role": "user",
            "content": user_message
        }
    ]
    resp = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages
    )
    content = resp.choices[0].message.content
    return content

@csrf_exempt
def chat_api(request):
    if request.method == "POST" and request.user.is_authenticated:
        data = request.POST
        user_msg = data.get('message', '')
        reply = ask_groq(user_msg)
        return JsonResponse({"reply": reply})
    return JsonResponse({"error": "Invalid request"}, status=400)
