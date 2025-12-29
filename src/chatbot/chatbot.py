# chatbot.py
from rapidfuzz import process, fuzz
from .models import ChatbotKnowledge

def get_answer(user_input: str) -> str:
    # 1. Fetch all questions from DB
    knowledge_items = ChatbotKnowledge.objects.all()
    if not knowledge_items:
        return "Maaf, saya belum punya informasi apa pun."

    choices = {item.id: item.question for item in knowledge_items}

    # 2. Find the best match using fuzzy matching
    # extractOne returns (string, score, index/key)
    best_match = process.extractOne(
        user_input,
        choices,
        scorer=fuzz.token_ratio
    )

    # 3. Check if the match is good enough (score > 60)
    score = best_match[1]
    if score > 60:
        match_id = best_match[2]
        return ChatbotKnowledge.objects.get(id=match_id).answer

    return "Saya tidak yakin tentang itu. Bisakah Anda mengulanginya?"
