VA_NAME = 'Стелларон'

VA_VER = "1.8(TEST)"

#VA_ALIAS = ('стела', 'стеларон', 'стелл', 'стелаж', 'стайло', 'стало', 'стайла', 'ставив', 'стояла', 'стоїло', 'стоїл', 'стала' , 'стайла', 'стела')
VA_ALIAS = ('кирило', 'кириле', 'кирилл',)

VA_TBR = ('скажи', 'покажи', 'відповідь', 'вимов', 'розкажи', 'скільки', 'виведи')

#'', '', '',
VA_CMD_LIST = {
    "help": ('список команд', 'команди', 'що ти вмієш', 'твої навички', 'навички'),
    "ctime": ('час', 'поточний час', 'зараз часу', 'котра година'),
    #"joke": ('розкажи анекдот', 'розсміши', 'жарт', 'розкажи жарт', 'пожартуй', 'розвішали'),
    "get_weather":("погода сьогодні","яка погода сьогодні","яка погода зараз","яка зараз погода"),
    "get_weather_tomorrow": ('погода завтра', 'яка погода завтра', 'прогноз на завтра'),
    "open_browser_Chrome": ('відкрий хром', 'запусти хром', 'відкрий гугл',),
    "open_page":('відкрий вкладку', 'відкрий нову вкладку'),
    "find_video":('найди мені відео', 'мені потрібно відео', 'найди відео'),
    "open_task_manager":('активні програми', 'активні програми', "активність комп'ютера",'які програми активні'),
    "open_system_properties":("інформацію про комп'ютер", 'властивості системи', "характеристики комп'ютера",),
    "search_wikipedia": ('знайди у вікіпедії', 'пошук у вікіпедії',),
    "find_files":('знайди файл','мені потрібен файл','де файл'),
    "ask_gpt":('знайди таку інформацію','мені цікаво','а що буде', 'хочу посміятися', 'а розповіси'),
    "Quit": ("вийти", "закінчити роботу", "прощай", "вихід"),
}