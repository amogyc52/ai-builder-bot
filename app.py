import streamlit as st
from google import genai
from google.genai import types

# Настройка страницы (вкладка в браузере)
st.set_page_config(page_title="ИИ-Михалыч", page_icon="🔨", layout="centered")

# Шапка сайта
st.title("🔨 Михалыч: твой ИИ-прораб")
st.write("Задай вопрос по стройке или ремонту. Михалыч ответит просто и по делу!")
st.write("---")

# Подключение к Gemini (Вставь сюда свой ключ)
API_KEY = "ТВОЙ_API_КЛЮЧ_ИЗ_GOOGLE_AI_STUDIO"
client = genai.Client(api_key=API_KEY)

# Наш топовый системный промт
SYSTEM_INSTRUCTION = """
Ты — Михалыч, мудрый, опытный и практичный прораб с 25-летним стажем в загородном домостроении, ремонте и отделке. К тебе приходят обычные мужики и парни, которые строят дом или делают ремонт своими руками и хотят сэкономить, но сделать качественно.

Твой тон — дружелюбный, поддерживающий, уверенный, чисто мужской. Говори просто, без заумной академической теории.
Используй строительный сленг (арматура, опалубка, стропила), но кратко объясняй его на пальцах.
Отвечай структурно, по пунктам.

Ты отвечаешь ТОЛЬКО на вопросы, связанные со строительством, ремонтом, инструментами.
Если тебя просят написать код, помочь с домашкой, рассказать рецепт — отказывайся.
Шаблон отказа: «Слушай, брат, я в этом деле круглый ноль. Моё дело — бетон мешать, доски пилить да дома строить. Давай лучше по делу: что у тебя там по ремонту или стройке? Спрашивай, подскажу».
"""

# Инициализируем историю чата, чтобы сообщения не пропадали
if "messages" not in st.session_state:
    st.session_state.messages = []

# Отображаем старые сообщения из истории на экране
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Поле для ввода вопроса (находится внизу экрана)
if user_query := st.chat_input("Спроси Михалыча, например: как выровнять угол фундамента?"):
    
    # Показываем вопрос пользователя
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.write(user_query)

    # Запрашиваем ответ у Михалыча
    with st.chat_message("assistant"):
        with st.spinner("Михалыч чешет репу..."):
            try:
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=user_query,
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_INSTRUCTION,
                        temperature=0.7,
                    ),
                )
                answer = response.text
                st.write(answer)
                # Сохраняем ответ в историю
                st.session_state.messages.append({"role": "assistant", "content": answer})
            except Exception as e:
                st.error(f"Упс, что-то пошло не так. Ошибка: {e}")