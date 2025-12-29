from django.http import JsonResponse
from django.shortcuts import render
from .chatbot import get_answer

def chat_hx(request):
    if request.method == "POST":
        user_input = request.POST.get("user-message", "")
        answer = get_answer(user_input)
        # Return a small partial HTML for HTMX to swap
        return render(request, "components/chat-message.html", {
            "user": user_input,
            "answer": answer
        })
    return render(request, "/components/chat-element.html")

def main_page(request):
    return render(request,"main.html")
