import pytest
from datetime import date
from django.contrib.auth.models import User
from .forms import TaskForm
from .serializers import TaskSerializer


@pytest.mark.django_db
def test_valid_task():
    """
    Перевірка форми з правильними даними
    """
    form_data = {
        'title': 'Заголовок',
        'description': 'Опис',
        'due_date': date.today()
    }
    form = TaskForm(data=form_data)
    assert form.is_valid()


@pytest.mark.django_db
def test_task_empty_fields():
    """
    Перевірка форми з пустими обов'язковими полями
    """
    form_data = {
        'title': '',
        'description': '',
        'due_date': ''
    }
    form = TaskForm(data=form_data)
    assert not form.is_valid()
    assert 'title' in form.errors
    assert 'description' in form.errors
    assert 'due_date' in form.errors


@pytest.mark.django_db
def test_due_date_cannot_be_in_past():
    """
    Перевірка поля due_date на коректність (дата виконання не може бути в минулому)
    """
    form_data = {
        'title': 'Заголовок',
        'description': 'Опис',
        'due_date': date.today().replace(year=2023)  # Помилка
    }
    form = TaskForm(data=form_data)
    assert not form.is_valid()
    assert 'due_date' in form.errors


@pytest.mark.django_db
def test_valid_task_serializer():
    """
    Перевірка з правильними даними
    """
    data = {
        'title': 'Заголовок',
        'description': 'Опис',
        'due_date': date.today()
    }
    serializer = TaskSerializer(data=data)
    assert serializer.is_valid()
    assert serializer.validated_data['title'] == 'Заголовок'
    assert serializer.validated_data['description'] == 'Опис'


@pytest.mark.django_db
def test_task_serializer_missing_title():
    """
    Перевірка, якщо заголовок відсутній
    """
    data = {
        'description': 'Опис',
        'due_date': date.today()
    }
    serializer = TaskSerializer(data=data)
    assert not serializer.is_valid()
    assert 'title' in serializer.errors


@pytest.mark.django_db
def test_due_date_cannot_be_in_past_serializer():
    """
    Перевірка поля due_date на коректність (дата виконання не може бути в минулому)
    """
    data = {
        'title': 'Заголовок',
        'description': 'Опис',
        'due_date': date.today().replace(year=2023)
    }
    serializer = TaskSerializer(data=data)
    assert not serializer.is_valid()
    assert 'due_date' in serializer.errors


@pytest.mark.django_db
def test_valid_with_user_serializer():
    """
    Перевірка з правильними внесеними даними
    """
    user = User.objects.create_user(
        username='user1', email='user1@example.com', password='111')
    data = {
        'title': 'Заголовок',
        'description': 'Опис',
        'due_date': date.today(),
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email
        }
    }
    serializer = TaskSerializer(data=data)
    assert serializer.is_valid()
    assert serializer.validated_data['user']['username'] == 'user1'


@pytest.mark.django_db
def test_task_serializer_invalid_user():
    """
    Дані користувача невірні
    """
    data = {
        'title': 'Заголовок',
        'description': 'Опис',
        'due_date': date.today(),
        'user': {
            'id': 10,  # Помилка
            'username': 'user2',
            'email': 'user2@example.com'
        }
    }
    serializer = TaskSerializer(data=data)
    assert not serializer.is_valid()
    assert 'user' in serializer.errors
