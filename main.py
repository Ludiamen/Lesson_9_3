import requests
from datetime import datetime


def get_questions(days_ago, tag):
    """ Функция, которая выводит все новые посты, содержащие заданный тэг,
        за указанноое от текущей даты количество дней
        с сайта https://stackoverflow.com/questions """

    # Определяем переменную счетчика постов
    counter = 0
    # Получаем текующую дату в секундах
    todate = int(datetime.timestamp(datetime.today()))
    # Определяем начальную дату для поиска
    fromdate = todate - days_ago * 86400
    # Вызаваем функцию для получения первых 30-ти постов. Функция возвращает дату 30-го поста и значение счетчика
    question_create_time, counter = get_next_questions(fromdate, todate, tag, counter)
    # Снова вызываем функцию для получения следующих постов пока дата поледнего поста не достигнет текущей даты
    while question_create_time < todate:
        # Передаем в функцию время последнего поста с предыдущей итерации. Возвращаем время поста после новой итерации
        question_create_time, counter = get_next_questions(question_create_time, todate, tag, counter)
        # Увеличиваем значение переменной для последнего поста на одну секунду, чтобы последний пост не дублировался
        question_create_time += 1
    # Функция возвращает строку с количеством постов
    return f'За {days_ago} дня(-ей) опубликовано {counter} новых вопросов.'


def get_next_questions(fromdate, todate, tag, counter):
    """ Функция, которая выводит в консоль и записывает в файл новые посты, содержащие заданный тэг,
        за указанный интервал времени (не более 30-ти постов за одну итерацию)
        с сайта https://stackoverflow.com/questions """

    # Определяем начальное значение переменной для хранения начала временного интервала
    question_create_time = todate
    # Определяем начальные параметры запроса
    params = {
        'fromdate': fromdate,
        'todate': todate,
        'order': 'asc',
        'sort': 'creation',
        'tagged': tag,
        'site': 'stackoverflow'
    }
    # Отправляем запрос с указанными параметрами
    responce = requests.get('https://api.stackexchange.com/2.3/questions', params=params)
    # Получаем статус отправки запроса
    responce.raise_for_status()
    # # Проверяем успешность отправки по полученному статусу. Если неуспешно, то выводим код ошибки запроса
    if responce.status_code != 200:
        print(f"Ошибка обработки запроса! Код ошибки: {responce.status_code}")
        return question_create_time, counter
    # Поочередно выводим заголовки вопросов с указанными тегами
    for question in responce.json().get('items'):
        counter += 1  # Увеличиваем значение счетчика
        question_create_time = question['creation_date']
        # Записываем построчно в файл очередные заголовки и теги постов с отметкой о дате создания
        with open(f'last_questions_{datetime.fromtimestamp(todate)}.txt', 'a') as file:
            file.write(f'Question # {counter}: {question["title"]}\n'
                       f'Tags: {str(question["tags"])}\n '
                       f'Creation Date {datetime.fromtimestamp(question_create_time)}\n'
                       f'____________________________________\n')
        # Выводим в консоль построчно очередные заголовки и теги постов с отметкой о дате создания
        print(f'Question # {counter}: {question["title"]}')
        print(f'Tags: {str(question["tags"])}')
        print(f'Creation Time: {datetime.fromtimestamp(question_create_time)}')
        print('____________________________________')
    # Возвращаем время последенго поста в очередной итерации и занчение счетчика
    return question_create_time, counter


if __name__ == '__main__':
    # Получаем список вопросов за последние два дня с тэгом 'python'
    print(get_questions(2, 'python'))
