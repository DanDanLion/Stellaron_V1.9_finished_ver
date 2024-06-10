import threading
from fuzzywuzzy import fuzz
import dialog_log
import config
import stt
import tts
import command
import os
import sys
import webbrowser
import pystray
from pystray import MenuItem as item
from PIL import Image
import customtkinter as ctk
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

dialog_log.open_log_file()
TOKEN_PATH = 'token.json'
CREDENTIALS_PATH = 'credentials.json'
SCOPES = ['https://www.googleapis.com/auth/userinfo.profile', 'https://www.googleapis.com/auth/userinfo.email']
PDF_PATH = ""

def va_respond(voice: str):
    print(voice)
    cleaned_voice = clean_text(voice)
    if cleaned_voice:
        dialog_log.write_to_file(f"Користувач11: {cleaned_voice}")

    if voice.startswith(tuple(config.VA_ALIAS)):
        filtered_voice = filter_cmd(voice)
        cmd = recognize_cmd(filtered_voice)
        dialog_log.write_to_file(f"Кирило: {cmd['cmd']}")

        if cmd['cmd'] not in config.VA_CMD_LIST.keys():
            tts.va_speak("Що?")
        else:
            if cmd['cmd'] in ['find_video', 'find_file', 'search_wikipedia']:
                query = filter_cmd(filtered_voice)
                result = execute_cmd(cmd['cmd'], query)
            elif cmd['cmd'] == 'ask_gpt':
                prompt = filter_cmd(filtered_voice)
                result = command.ask_gpt_cmd(prompt)
                print(result)
                dialog_log.write_to_file(f"ГПТ: {result}")
            else:
                result = execute_cmd(cmd['cmd'])
            if result:
                dialog_log.write_to_file(f"Кирило: {result}")
                result = command.speak_with_numbers(result)
                tts.va_speak(result)

def clean_text(text: str) -> str:
    clean_text = "".join(char for char in text if char.isalnum() or char.isspace())
    return clean_text

def recognize_cmd(cmd: str):
    rc = {'cmd': '', 'percent': 0}
    for c, v in config.VA_CMD_LIST.items():
        for x in v:
            vrt = fuzz.ratio(cmd, x)
            if vrt > rc['percent']:
                rc['cmd'] = c
                rc['percent'] = vrt
    return rc

def filter_cmd(raw_voice: str) -> str:
    cmd = raw_voice
    for x in config.VA_ALIAS + config.VA_TBR:
        cmd = cmd.replace(x, "").strip()
    return cmd

def execute_cmd(cmd: str, query: str = ""):
    print(f"Executing command: {cmd}")
    if cmd == 'help':
        return command.help_cmd()
    elif cmd == 'ctime':
        return command.ctime_cmd()
    elif cmd == 'open_browser_Chrome':
        return command.open_browser_Chrome_cmd()
    elif cmd == 'get_weather':
        result = command.get_weather_cmd()
        dialog_log.write_to_file(result)
        if result:
            return
    elif cmd == 'get_weather_tomorrow':
        result = command.get_weather_tomorrow_cmd()
        dialog_log.write_to_file(result)
        if result:
            return
    elif cmd == 'open_page':
        return command.open_page_cmd()
    elif cmd == 'find_video':
        return command.find_video_cmd(query)
    elif cmd == 'open_task_manager':
        return command.open_task_manager_cmd()
    elif cmd == 'open_system_properties':
        return command.open_system_properties_cmd()
    elif cmd == 'search_wikipedia':
        return command.search_wikipedia_cmd(query)
    elif cmd == 'find_files':
        return command.find_file_cmd(query)
    elif cmd == 'ask_gpt':
        return command.ask_gpt_cmd(query)
    elif cmd == 'Quit':
        return command.Quit_cmd()
    return None

def open_pdf():
    webbrowser.open(PDF_PATH)

def exit_program(icon, item):
    icon.stop()
    sys.exit()

def start_interface():
    ctk.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
    ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

    class VoiceAssistance(ctk.CTk):
        def __init__(self):
            super().__init__()

            self.title('Голосовий асистент "Стелларон"')
            self.geometry(f"{1000}x{480}")
            self.minsize(550, 250)
            self.maxsize(1000, 480)
            self.grid_rowconfigure(0, weight=1)
            self.grid_rowconfigure(1, weight=0)  # For bottom frame
            self.grid_columnconfigure(0, weight=1)

            # create main frame
            self.main_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
            self.main_frame.grid(row=0, column=0, sticky="nsew")
            self.main_frame.grid_rowconfigure(0, weight=1)
            self.main_frame.grid_columnconfigure(1, weight=1)

            # Load images with light and dark mode image
            image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "image")
            # self.personalized_image = ctk.CTkImage(
            #     light_image=Image.open(os.path.join(image_path, "personalized_dark.png")),
            #     dark_image=Image.open(os.path.join(image_path, "personalized_light.png")),
            #     size=(20, 20))
            # self.home_frame = ctk.CTkImage(
            #     light_image=Image.open(os.path.join(image_path,"")),
            #     dark_image=Image.open(os.path.join(image_path,"")),
            #     size=(20,20)
            # )

            # create navigation frame
            self.navigation_frame = ctk.CTkFrame(self.main_frame, corner_radius=0)
            self.navigation_frame.grid(row=0, column=0, sticky="nsew")
            self.navigation_frame.grid_rowconfigure(4, weight=1)
            self.navigation_frame_label = ctk.CTkLabel(
                self.navigation_frame, text="Налаштування",
                compound="center", font=ctk.CTkFont(size=15, weight="bold"))
            self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

            self.home_button = ctk.CTkButton(
                self.navigation_frame,
                corner_radius=0, height=40, border_spacing=10,
                text="Профіль", fg_color="transparent", text_color=("gray10", "gray90"),
                hover_color=("gray70", "gray30"),
                anchor="w", command=self.home_button_event)
            self.home_button.grid(row=1, column=0, sticky="ew")

            self.frame_3_button = ctk.CTkButton(
                self.navigation_frame, corner_radius=0, height=40,
                border_spacing=10, text="Гучність",
                fg_color="transparent", text_color=("gray10", "gray90"),
                hover_color=("gray70", "gray30"), anchor="w",
                command=self.frame_3_button_event)
            self.frame_3_button.grid(row=3, column=0, sticky="ew")

            # create home frame
            self.home_frame = ctk.CTkFrame(self.main_frame, corner_radius=0, fg_color="transparent")
            self.home_frame.grid(row=0, column=1, sticky="nsew")
            self.home_frame.grid_columnconfigure(0, weight=1)

            # Добавляем заголовок
            self.home_frame_label = ctk.CTkLabel(
                self.home_frame, text="Профіль користувача",
                font=ctk.CTkFont(size=15, weight="bold"))
            self.home_frame_label.grid(row=0, column=0, padx=20, pady=15, sticky="n")

            # Смещаем кнопки вниз и влево
            self.home_frame_button_1 = ctk.CTkButton(self.home_frame, text="Підключитися до Google", command=self.connect_google)
            self.home_frame_button_1.grid(row=1, column=0, padx=(20, 200), pady=(20, 10), sticky="w")
            self.home_frame_button_2 = ctk.CTkButton(self.home_frame, text="Особисті дані", compound="right")
            self.home_frame_button_2.grid(row=2, column=0, padx=(20, 200), pady=10, sticky="w")

            # create third frame (Volume Settings)
            self.third_frame = ctk.CTkFrame(self.main_frame, corner_radius=0, fg_color="transparent")
            self.third_frame.grid(row=0, column=1, sticky="nsew")
            self.third_frame.grid_columnconfigure(0, weight=1)

            # Добавляем заголовок
            self.volume_settings_label = ctk.CTkLabel(
                self.third_frame, text="Налаштування гучності",
                font=ctk.CTkFont(size=15, weight="bold"))
            self.volume_settings_label.grid(row=0, column=0, padx=20, pady=15, sticky="n")

            self.volume_set_slider = ctk.CTkLabel(
                self.third_frame, text="Гучність голосового асистента:",
                font=ctk.CTkFont(size=12)
            )
            self.volume_set_slider.grid(row=1, column=0, padx=20, pady=20, sticky="nw")

            self.volume_slider = ctk.CTkSlider(
                self.third_frame, from_=0, to=100, number_of_steps=100,
                command=self.change_volume, width=250, height=15)
            self.volume_slider.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="nw")

            self.volume_value_label = ctk.CTkLabel(
                self.third_frame, text="50%", font=ctk.CTkFont(size=12))
            self.volume_value_label.grid(row=2, column=0, padx=(275, 5), pady=(0, 10), sticky="w")

            # Add bottom frame with home button
            self.bottom_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
            self.bottom_frame.grid(row=1, column=0, sticky="ew")
            self.bottom_frame.grid_rowconfigure(0, weight=1)
            self.bottom_frame.grid_columnconfigure(0, weight=1)

            self.bottom_button = ctk.CTkButton(
                self.bottom_frame,
                corner_radius=0, height=40, border_spacing=10,
                text="Налаштування", fg_color="#EE9B01", text_color=("gray10", "gray90"),
                hover_color=("gray70", "gray30"),
                anchor="center", command=self.bottom_button_event)
            self.bottom_button.grid(row=0, column=0, sticky="ew")

            # create new frame
            self.new_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
            self.new_frame.grid(row=0, column=0, sticky="nsew")
            self.new_frame.grid_rowconfigure(0, weight=1)
            self.new_frame.grid_columnconfigure(0, weight=1)

            # Load and display icon with increased size
            self.icon_image = ctk.CTkImage(light_image=Image.open(os.path.join(image_path, "Trash_Icon.jpg")), size=(200, 200))
            self.icon_label = ctk.CTkLabel(self.new_frame, text="", image=self.icon_image)
            self.icon_label.grid(row=0, column=0)

            # Создание фрейма для настроек в new_frame
            self.new_settings_frame = ctk.CTkFrame(self.new_frame, corner_radius=0, fg_color="transparent")
            self.new_settings_frame.grid(row=1, column=0, padx=20, pady=0, sticky="nw")

            # Создаем виджеты для смены темы и текстовое поле
            self.new_appearance_mode_label = ctk.CTkLabel(
                self.new_settings_frame, text="Змінити тему",
                font=ctk.CTkFont(size=12))
            self.new_appearance_mode_label.grid(row=0, column=0, padx=10, pady=0, sticky="nw")

            # Выпадающее меню для выбора режима отображения
            self.new_appearance_mode_menu = ctk.CTkOptionMenu(
                self.new_settings_frame,
                values=["Light", "Dark", "System"],
                command=self.change_appearance_mode_event
            )
            self.new_appearance_mode_menu.grid(row=1, column=0, padx=10, pady=5, sticky="nw")

            # Текстовое поле
            self.textbox1 = ctk.CTkTextbox(self.new_settings_frame, height=20,width=100, wrap="none")
            self.textbox1.grid(row=0, column=0, padx=210, pady=0, sticky="ew", columnspan=2)
            self.textbox1.grid_columnconfigure(0, weight=100)
            self.textbox1.grid_rowconfigure(0, weight=100)
            self.textbox2 = ctk.CTkTextbox(self.new_settings_frame, height=20, wrap="none")
            self.textbox2.grid(row=1, column=0, padx=210, pady=10, sticky="ew", columnspan=2)
            self.textbox2.grid_columnconfigure(0, weight=100)

            # select default frame
            self.select_frame_by_name("new_home")

        def select_frame_by_name(self, name):
            # Hide all frames
            self.home_frame.grid_forget()
            self.third_frame.grid_forget()
            self.new_frame.grid_forget()

            # Show the selected frame
            if name == "profile":
                self.home_frame.grid(row=0, column=1, sticky="nsew")
            elif name == "frame_3":
                self.third_frame.grid(row=0, column=1, sticky="nsew")
            elif name == "new_home":
                self.new_frame.grid(row=0, column=0, sticky="nsew")

        def connect_google(self):
            creds = None
            if os.path.exists(TOKEN_PATH):
                creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
                    creds = flow.run_local_server(port=0)
                with open(TOKEN_PATH, 'w') as token:
                    token.write(creds.to_json())
            print("Підключення до Google аккаунту успішно виконано!")

        def home_button_event(self):
            self.select_frame_by_name("profile")
            self.bottom_button.configure(text="Домашня сторінка", command=self.bottom_button_event)

        def frame_3_button_event(self):
            self.select_frame_by_name("frame_3")
            self.bottom_button.configure(text="Домашня сторінка", command=self.bottom_button_event)

        def bottom_button_event(self):
            if self.new_frame.winfo_ismapped():
                self.new_frame.grid_forget()
                self.bottom_button.configure(text="Налаштування", command=self.bottom_button_event)
            else:
                self.select_frame_by_name("new_home")
                self.bottom_button.configure(text="Налаштування", command=self.bottom_button_event)

        def change_appearance_mode_event(self, new_appearance_mode):
            ctk.set_appearance_mode(new_appearance_mode)

        def change_volume(self, value):
            self.volume_value_label.configure(text=str(int(value)) + "%")

    app = VoiceAssistance()
    app.mainloop()
    icon_image = Image.open("image\Profile_Picture_Trash_Can.ico")
    icon = pystray.Icon("name", icon_image, "Голосовий асистент 'Стелларон'")
    menu = (item('Інструкція', open_pdf), item('Вихід', exit_program))
    icon.menu = pystray.Menu(*menu)
    icon.run()

def start_listen():
    print(f"{config.VA_NAME} v{config.VA_VER} почав працювати ...")
    dialog_log.write_to_file("Доброго часу доби, любий користуваче!")
    tts.va_speak("Доброго часу доби, любий користуваче!...")
    print("Доброго часу доби, любий користуваче!")
    stt.va_listen(va_respond)

if __name__ == '__main__':
    va = threading.Thread(target=start_listen, daemon=True)
    va.start()
    start_interface()