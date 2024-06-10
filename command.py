import subprocess
import sys
import pyautogui
import pyperclip
import time
from weather import *
import dialog_log
import tts
import webbrowser
import datetime
import g4f
from g4f.Provider import(Bing, OpenaiChat, ChatgptAi)
import inflect

def help_cmd():
    text = "Я можу: ...\n"
    text += "сказати скільки зараз часу ...\n"
    text += "сказати яка зараз погода в місті Дніпро та кількісті градусів на цей день ...\n"
    text += "сказати погоду в місті Дніпро на завтра ...\n"
    text += "відкрити гугл хром...\n"
    text += "надати змогу переглянути які програми або додатки активні...\n"
    text += "надати змогу переглянути характеристики комп'ютера...\n"
    text += "відкрити нову вкладку в Опері ...\n"
    text += "знайти відео на Ютубі ...\n"
    text += "знайти інформацію у вікіпедії ...\n"
    text += "за допомогою ГПТ чату спілкуватися з вами ...\n"
    text += "відкрити провідник, щоб користувач міг знайти файли ...\n"
    text += "та вийти з програми"
    dialog_log.write_to_file(f"Кирило: {text}")
    tts.va_speak(text)

def ctime_cmd():
    now = datetime.datetime.now()
    text = "Зараз " + num2words(now.hour, lang='ru') + " " + num2words(now.minute, lang='ru')
    dialog_log.write_to_file(text)
    tts.va_speak(text)

def open_browser_Chrome_cmd():
    chrome_path = 'C:\Program Files\Google\Chrome\Application\chrome.exe'
    webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))
    webbrowser.get('chrome').open("http://python.org")
    dialog_log.write_to_file("open_browser_Chrome")

def get_weather_cmd():
    api_key = '676102c011ad9b625785526f6057eac8'
    city = 'Дніпро'

    weather_data = load_weather_from_json()
    internet_available = check_internet_connection()

    if internet_available:
        weather_description, temperature_text, data = get_weather(api_key, city)
        if weather_description is not None:
            save_weather_to_json(data, None)  # Передаємо лише сьогоднішні дані
            weather_info = f"Погода в місті {city}: {weather_description}. Температура: {temperature_text} градусів Цельсія..."
            tts.va_speak(weather_info)
            return weather_info
        else:
            result = "Помилка отримання даних про погоду..."
            tts.va_speak(result)
            return result
    else:
        if weather_data and "today" in weather_data:
            last_update = datetime.datetime.fromtimestamp(weather_data["today"]["dt"])
            current_time = datetime.datetime.now()
            if (current_time - last_update).days < 1:
                weather_description = weather_data["today"]['weather'][0]['description']
                temperature = weather_data["today"]['main']['temp']
                temperature_text = num2words(int(temperature), lang='ru')
                weather_info = f"Немає підключення до інтернету, але останній прогноз погоди у місті {city}: {weather_description}. Температура: {temperature_text} градусів Цельсія..."
                tts.va_speak(weather_info)
                return weather_info
            else:
                result = "Немає підключення до інтернету, і прогноз на цей тиждень не був завантажений..."
                tts.va_speak(result)
                return result
        else:
            result = "Немає підключення до інтернету, і прогноз на цей тиждень не був завантажений..."
            tts.va_speak(result)
            return result

def get_weather_tomorrow_cmd():
    api_key = '676102c011ad9b625785526f6057eac8'
    city = 'Дніпро'
    internet_available = check_internet_connection()

    if internet_available:
        weather_description, temperature_text, tomorrow_data = get_weather_tomorrow(api_key, city)
        if weather_description is not None:
            # Завантажити поточний стан файлу
            weather_data = load_weather_from_json()
            if weather_data is None:
                weather_data = {}
            # Додати або оновити прогноз на завтра
            weather_data["tomorrow"] = tomorrow_data
            save_weather_to_json(weather_data["today"], tomorrow_data)  # Передаємо дані за сьогодні і за завтра
            weather_info = f"Прогноз погоди на завтра {city}: {weather_description}. Температура: {temperature_text} градусів Цельсія..."
            tts.va_speak(weather_info)
            return weather_info
        else:
            result = "Помилка отримання даних про погоду завтра..."
            tts.va_speak(result)
            return result
    else:
        weather_data = load_weather_from_json()
        if weather_data and "tomorrow" in weather_data:
            weather_description = weather_data["tomorrow"]['weather'][0]['description']
            temperature = weather_data["tomorrow"]['main']['temp']
            temperature_text = num2words(int(temperature), lang='ru')
            weather_info = f"Немає підключення до інтернету, але останній прогноз погоди на завтра у місті {city}: {weather_description}. Температура: {temperature_text} градусів Цельсія..."
            tts.va_speak(weather_info)
            return weather_info
        else:
            result = "Немає підключення до інтернету, і прогноз на завтра не був завантажений..."
            tts.va_speak(result)
            return result

def open_page_cmd():
    webbrowser.open_new_tab("https://www.google.com")
    dialog_log.write_to_file("open_page")

def find_video_cmd(query):
    search_query = " ".join(query.split(" ")[3:]).strip()
    if search_query:
        url = f"https://www.youtube.com/results?search_query={search_query}"
        webbrowser.open(url)
        dialog_log.write_to_file(f"Пошук відео на YouTube: {search_query}")
        tts.va_speak(f"Шукаю відео на Ютубі: {search_query}...")
    else:
        tts.va_speak("Будь ласка, уточніть запит для пошуку відео...")

def search_wikipedia_cmd(query):
    search_query = " ".join(query.split(" ")[3:]).strip()
    if search_query:
        url = f"https://uk.wikipedia.org/wiki/{search_query.replace(' ', '_')}"
        webbrowser.open(url)
        dialog_log.write_to_file(f"Пошук на Вікіпедії: {search_query}")
        tts.va_speak(f"Шукаю інформацію на Вікіпедії про: {search_query}...")
    else:
        tts.va_speak("Будь ласка, уточніть запит для пошуку на Вікіпедії...")

def open_task_manager_cmd():
    subprocess.run(["powershell", "Start-Process", "taskmgr"], shell=True)
    dialog_log.write_to_file("Відкриваття менеджер завдань для перегляду активних програм")
    tts.va_speak("Відкриваю менеджер завдань для перегляду активних програм...")

def open_system_properties_cmd():
    try:
        dialog_log.write_to_file("Відкриття відомостей/характеристик системи ПК")
        tts.va_speak("Відкриваю відомості комп'ютера...")
        subprocess.run(["msinfo32"])
    except Exception as e:
        print(f"Помилка при відкриті відомосте про систему: {e}")

def find_file_cmd(query):
    search_query = " ".join(query.split(" ")[2:])  # Извлекаем запрос из команды
    if query:
        pyperclip.copy(search_query)
        os.startfile('explorer.exe')
        time.sleep(1)
        pyautogui.hotkey('ctrl', 'f')
        time.sleep(0.5)
        pyautogui.hotkey('ctrl', 'v')
        pyautogui.press('enter')
        return f"Шукає файл за запитом '{search_query}'..."
    else:
        return "Будь ласка, вкажіть запит для пошуку файла..."

def ask_gpt(prompt: str) -> str:
    response_text = g4f.ChatCompletion.create(
        model="gpt-4",
        #model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        #provider=ChatgptAi
    )
    return response_text

def speak_with_numbers(text):
    words = text.split()
    for i, word in enumerate(words):
        if word.replace(',', '').isdigit():  # Перевірка наявності числа
            num = int(word.replace(',', ''))  # Конвертація рядка у число
            words[i] = num2words(num, lang='ru')  # Заміна числа на його словесний еквівалент
    corrected_text = ' '.join(words)
    return corrected_text

def ask_gpt_cmd(prompt: str):
    response = ask_gpt(prompt)  # Получаем ответ от GPT на запрос
    corrected_response = speak_with_numbers(response)  # Преобразуем числа в слова
    dialog_log.write_to_file(f"GPT: {corrected_response}")  # Записываем ответ в логи
    #tts.va_speak(corrected_response)  # Произносим ответ
    return response  # Возвращаем исходный ответ для возможного дальнейшего использования

def Quit_cmd():
    goodbye_text = "Прощавайте, мій любий користувач!..."
    dialog_log.write_to_file(goodbye_text)
    tts.va_speak(goodbye_text)
    sys.exit()