from rest_framework.decorators import api_view
from django.http import JsonResponse
from rest_framework import status
import os
from models import Event, Plans, NormalUser, Questions, Subscription
import jwt
from dotenv import load_dotenv
load_dotenv()
SECRET_KEY = os.getenv('JWT_SECRET_KEY')


@api_view(['POST'])
def update_answer(request):
    if request.method != "POST":
        return JsonResponse({"success": False,
                             "message": "método invalido"},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)

    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return JsonResponse({
            "success": False,
            "message": "Token de acesso não fornecido ou formato inválido."
        }, status=status.HTTP_401_UNAUTHORIZED)

    token = auth_header.split(' ')[1]

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return JsonResponse({"success": False,
                             "message": "Token expirado."},
                            status=status.HTTP_401_UNAUTHORIZED)
    except jwt.DecodeError:
        return JsonResponse({"success": False,
                             "message": "Erro ao decodificar o token."},
                            status=status.HTTP_401_UNAUTHORIZED)

    user_id = payload.get('id')
    event_id = request.data.get("eventId")

    try:
        event = Event.objects.get(id=event_id)
    except Event.DoesNotExist:
        return JsonResponse({"success": False,
                             "message": "Evento não encontrado."},
                            status=status.HTTP_404_NOT_FOUND)

    try:
        user = NormalUser.objects.get(id=user_id)
    except NormalUser.DoesNotExist:
        return JsonResponse({"success": False,
                             "message": "Usuário não encontrado."},
                            status=status.HTTP_404_NOT_FOUND)

    if user.user_type != "speaker":
        return JsonResponse({"success": False,
                             "message":
                            "Você não tem permissão para editar a pergunta"},
                            status=status.HTTP_400_BAD_REQUEST)

    question_id = request.data.get('questionId')
    question = request.data.get("question", None)
    # question_type = request.data.get("questionType", None)

    existing_events = Event.objects.filter(
        questions__id=question_id).exclude(id=event_id)

    if existing_events.exists():

        subscription = Subscription.objects.get(user=user_id)
        plan = Plans.objects.get(subscription=subscription.id)

        if plan.plan_name == "standard":
            return JsonResponse({"success": False,
                                 "message":
                                "você não pode atualizar"},
                                status=status.HTTP_403_FORBIDDEN)

        new_event = Event.objects.create(
            event_name=event.event_name,
            description=event.description,
            questions=question,
            created_by=user,
        )

        return JsonResponse({"success": True,
                             "message":
                             "Evento duplicado e atualizado com sucesso",
                             "new_event_id": new_event.id,
                             "qr_code": "qr"},
                            status=status.HTTP_200_OK)

    question_db = Questions.objects.filter(id=question_id).first()
    if question_db:
        get_event = Event.objects.get(id=event_id)
        if question_db != get_event.event_creator:
            subscription = Subscription.objects.get(user=user_id)
            plan = Plans.objects.get(subscription=subscription.id)
            if plan.plan_name == "standard":
                return JsonResponse({"success": False,
                                     "message":
                                    "você não pode atualizar esta pergunta."},
                                    status=status.HTTP_403_FORBIDDEN)
            return JsonResponse({"success": True,
                                 "message": "Evento atualizado com sucesso"},
                                status=status.HTTP_200_OK)
        return JsonResponse({"success": True,
                             "message": "Evento atualizado com sucesso",
                             "qr_code": "qr"},
                            status=status.HTTP_200_OK)
    else:
        return JsonResponse({"success": False,
                             "message": "Pergunta não encontrada."},
                            status=status.HTTP_404_NOT_FOUND)
