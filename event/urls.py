from django.urls import path
from .views.account.user_creation import create_user
from .views.account.login_user import login_user_with_cpf
from .views.account.login_user import login_user_with_email
from .views.account.get_user import get_user_profile
from .views.account.send_validation_code import email_validation
from .views.account.send_validation_code import verify_email_code
from .views.account.update_account import update_user
from .views.account.delete_account import delete_user
from .views.account.update_account import password_reset
from .views.account.update_account import password_reset_confirm
from .views.account.update_account import password_forgot_change
from .views.account.update_account import forgot_password
from .views.account.user_creation import validate_jwt
from .views.account.user_creation import generate_new_token
from .views.event.create_event import create_event
from .views.event.get_event import get_event
from .views.event.get_all_events import get_user_events
from .views.event.update_event import update_event
from .views.event.delete_event import delete_event
from .views.event.get_event_statistics import get_event_stats
from .views.event.start_event import start_event
from .views.event.end_event import end_event
from .views.event_user.get_event_to_user import get_event_user
from .views.event_user.get_event_to_user import get_event_active
from .views.event.get_event_and_questions import get_event_and_questions
from .views.questions.create_question import create_question
from .views.questions.update_question import update_question
from .views.questions.delete_question import delete_question
from .views.questions.get_all_question import get_questions_and_answers
from .views.answers.delete_answer import delete_answer
from .views.answers.update_answer import update_answer
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    # User
    path('create/',
         create_user, name="create_user"),
    path('login/',
         login_user_with_cpf, name="login_cpf"),
    path('login-email/',
         login_user_with_email, name="login_email"),
    path("user-profile/",
         get_user_profile, name="get-user-profile"),
    path("email-validation/",
         email_validation, name="email-validation"),
    path("verify-email-code/",
         verify_email_code, name="verify-email-code"),
    path("update-user/",
         update_user, name="update-user"),
    path("delete-user/",
         delete_user, name="delete_user"),
    path("validate-token/",
         validate_jwt, name="validate_jwt"),
    path("generate-new-token/",
         generate_new_token, name="generate_new_token"),

    # Password Reset
    path('request-reset/',
         password_reset, name='request-reset'),
    path('reset/',
         password_reset_confirm, name='password-reset-confirm'),
    path('forgot-password/',
         forgot_password, name='forgot-password'),
    path('forgot-password-change/',
         password_forgot_change, name='forgot-password-change'),

    # event
    path('get-event/<int:eventId>/',
         get_event, name="get-event"),
    path('get-all-events/',
         get_user_events, name="get_user_events"),
    path('event-create/',
         create_event, name="create_event"),
    path('update-event/<int:eventId>/',
         update_event, name="update_event"),
    path('delete-event/<int:eventId>/',
         delete_event, name="delete_event"),
    path('get-event-and-question/<int:eventId>/',
         get_event_and_questions, name="get_event_and_questions_and_answers"),
    path('start-event/<int:eventId>/',
         start_event, name="start-event"),
    path('end-event/<int:eventId>/',
         end_event, name="start-event"),
    path('get-event-stats/<int:eventId>/',
         get_event_stats, name="get_event_stats"),
    path('get-event-user/<int:eventId>/',
         get_event_user, name="get_event_user"),
    path('get-event-active/<int:eventId>/',
         get_event_active, name="get_event_user"),

    # question
    path('create-question/<int:eventId>/',
         create_question, name="create_question"),
    path('get-questions/<int:eventId>/',
         get_questions_and_answers, name="get_questions_and_answers"),
    path('update-question/<int:eventId>/<int:questionId>/',
         update_question, name="update_question"),
    path('delete-question/<int:eventId>/<int:questionId>/',
         delete_question, name="delete_question"),

    # answers
    path('delete-answer/<int:eventId>/<int:answerId>/',
         delete_answer, name="delete_answer"),
    path('update-answers/<int:eventId>/<int:questionId>/',
         update_answer, name="update-answers")

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
