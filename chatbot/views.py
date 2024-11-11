from rest_framework.decorators import api_view
from rest_framework.response import Response
import os
import google.generativeai as genai
from .models import Message

# Configurez l'API avec votre clé
genai.configure(api_key=os.environ["API_KEY"])

@api_view(['POST'])
def chat_view(request):
    user_message = request.data.get('user_message', '')

    if user_message:
        bot_response = generate_hint(user_message)

        # Enregistrer le message et la réponse dans la base de données
        Message.objects.create(user_message=user_message, bot_response=bot_response)
        
        return Response({"user_message": user_message, "bot_response": bot_response})
    
    return Response({"error": "Message utilisateur non fourni"}, status=400)

def generate_hint(question_text):
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = f"Réponds directement à la question suivante : {question_text}"
    response = model.generate_content(prompt)

    if response and hasattr(response, 'text'):
        return response.text
    else:
        return "Aucune réponse générée."
