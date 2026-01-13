from django.http import JsonResponse
from django.shortcuts import render
from .chatbot import get_answer

def chat_messages(request):
    if request.method == "POST":
        user_input = request.POST.get("user-message", "")
        answer = get_answer(user_input)
        # Return a small partial HTML for HTMX to swap
        return render(request, "components/chat-message.html", {
            "user": user_input,
            "answer": answer
        })

def chat_forms(request):
    return render(request,"components/chat-window.html")
