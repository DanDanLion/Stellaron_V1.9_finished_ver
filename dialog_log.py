import datetime

LOG_FILE_PATH = 'dialogue_log.txt'

def open_log_file():
    global file
    file = open(LOG_FILE_PATH, 'a', encoding='utf-8')

def log_dialogue(speaker, text):
    timestamp = datetime.datetime.now().strftime("%d %b. %H:%M")
    file.write(f"{timestamp} {speaker}: {text}\n")

def close_log_file():
    file.close()

def write_to_file(data):
    if data.strip():
        if data.startswith("Кирило2"):
            log_dialogue("Кирило3", data[len("Кирило4"):].strip())
        else:
            log_dialogue("Програма", data)
        file.flush()