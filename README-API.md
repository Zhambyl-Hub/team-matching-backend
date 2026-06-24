Документация API для фронтенд-разработки (Matching Hub)

1. Авторизация (JWT)
Базовый URL для авторизации: /api/v1/auth/

Все запросы к защищенным эндпоинтам должны содержать заголовок:
Authorization: Bearer <access_token>

Регистрация пользователя
URL: /api/v1/auth/register/

Метод: POST
Тело запроса (JSON):

JSON
{
  "email": "user@example.com",
  "password": "secure_password_min_8_chars"
}

Успешный ответ (210 Created):
JSON
{
  "message": "Пользователь успешно зарегистрирован",
  "user_id": 1
}

Примечание: При успешной регистрации на бэкенде автоматически создается пустой профиль пользователя.

Авторизация (Вход)
URL: /api/v1/auth/login/

Метод: POST
Тело запроса (JSON):

JSON
{
  "email": "user@example.com",
  "password": "secure_password"
}

Успешный ответ (200 OK):
JSON
{
  "refresh": "eyJhbGciOiJIUzI1NiIsIn...",
  "access": "eyJhbGciOiJIUzI1NiIsIn..."
}

Обновление токена
URL: /api/v1/auth/token/refresh/
Метод: POST
Тело запроса (JSON):
JSON
{
  "refresh": "refresh_token_string"
}

Успешный ответ (200 OK):
JSON
{
  "access": "new_access_token_string"
}

2. Справочники (Общие данные)
Доступны без авторизации. Используются для заполнения выпадающих списков и тегов в формах.
Получение списка навыков (Skills)

URL: /api/v1/skills/

Метод: GET
Успешный ответ (200 OK):
JSON
[
  { "id": 1, "name": "Python" },
  { "id": 2, "name": "React" }
]

Получение списка сфер бизнеса (Interests)
URL: /api/v1/interests/

Метод: GET
Успешный ответ (200 OK):
JSON
[
  { "id": 1, "name": "FinTech" },
  { "id": 2, "name": "EdTech" }
]

3. Профили пользователей
Все эндпоинты, кроме получения справочников, требуют JWT-токен.

Получение и редактирование собственного профиля

URL: /api/v1/profiles/me/
Метод: GET | PUT | PATCH
Возможные значения полей-выборов (Choices):

stage: idea (Есть только идея), 
prototype (Прототип / MVP), 
traction (Есть пользователи / первые продажи), 
business (Работающий бизнес), 
looking (Пока просто ищу проект).
commitment: hobby (Хобби), 
part_time (Part-time), 
full_time (Full-time).

Тело запроса при обновлении (PATCH):
JSON
{
  "bio": "Бэкенд разработчик на Django.",
  "portfolio_url": "https://portfolio.com",
  "github_url": "https://github.com/username",
  "telegram_username": "@username_tg",
  "stage": "looking",
  "commitment": "full_time",
  "location": "Тараз",
  "skills_have": [1],
  "skills_want": [2],
  "interests": [1]
}

Успешный ответ (200 OK):
JSON
{
  "id": 1,
  "email": "user@example.com",
  "bio": "Бэкенд разработчик на Django.",
  "portfolio_url": "https://portfolio.com",
  "github_url": "https://github.com/username",
  "telegram_username": "@username_tg",
  "stage": "looking",
  "commitment": "full_time",
  "location": "Тараз",
  "skills_have": [1],
  "skills_want": [2],
  "interests": [1],
  "is_approved": false
}

Примечание: Поле is_approved доступно только для чтения. Оно переключается администратором в панели модерации.
Лента рекомендаций (Умный скоринг)
Выдает список профилей, отсортированных по количеству совпадений навыков (те, чьи skills_have соответствуют вашим skills_want). Исключает самого пользователя и тех, кого он уже лайкнул.
URL: /api/v1/profiles/recommendations/

Метод: GET
Успешный ответ (200 OK):
JSON
[
  {
    "id": 2,
    "email": "partner@example.com",
    "bio": "Фронтендер на React.",
    "portfolio_url": "",
    "github_url": "https://github.com/partner",
    "telegram_username": "",
    "stage": "idea",
    "commitment": "part_time",
    "location": "Тараз",
    "skills_have": [2],
    "skills_want": [1],
    "interests": [1],
    "is_approved": true
  }
]

Важно: Поле telegram_username в этом эндпоинте возвращается пустым до тех пор, пока не случится взаимный матч.

4. Взаимодействия и Матчи
Проявление интереса (Лайк)
Отправляется, когда текущий пользователь нажимает кнопку интереса на карточке из ленты рекомендаций.

URL: /api/v1/interactions/like/

Метод: POST
Тело запроса (JSON):
JSON
{
  "to_profile": 2
}

Успешный ответ (201 Created):
JSON
{
  "message": "Интерес успешно зафиксирован",
  "is_match": true
}

Примечание: Если is_match возвращает true, значит лайк был взаимным. На бэкенде автоматически создалась запись совпадения.
Список взаимных матчей (Совпадений)
Выводит список всех пользователей, с которыми совпал интерес. В этом списке раскрывается защищенное поле контактов.

URL: /api/v1/interactions/matches/

Метод: GET
Успешный ответ (200 OK):
JSON
[
  {
    "id": 12,
    "partner_profile": {
      "id": 2,
      "email": "partner@example.com",
      "bio": "Фронтендер на React.",
      "portfolio_url": "",
      "github_url": "https://github.com/partner",
      "telegram_username": "@partner_tg_username",
      "stage": "idea",
      "commitment": "part_time",
      "location": "Тараз",
      "skills_have": [2],
      "skills_want": [1],
      "interests": [1],
      "is_approved": true
    },
    "created_at": "2026-06-22T07:00:00Z"
  }
]