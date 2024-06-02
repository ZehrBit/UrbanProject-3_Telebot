import random

JOKES = [
    "Почему программисты любят зиму? Потому что это время, когда нет багов.",
    "Почему программисты не любят природу? Слишком много багов.",
    "Что сказал программист, когда его разбудили в 5 утра? 'Простите, у меня еще не скомпилировался сон.'",
    "Почему программисты такие умные? Потому что они знают все переменные в жизни.",
    "Почему программисту нельзя пересекать дорогу? Потому что он всегда будет искать 'переход' и 'переменную'.",
    "Почему программисты всегда путают Рождество и Хэллоуин? Потому что DEC 25 = OCT 31.",
    "Что сказал программист, когда увидел свою первую ошибку? 'Баг? Я думал, это фича!'",
    "Почему программисты такие плохие садоводы? Потому что они не могут найти корень проблемы.",
    "Как программисты предпочитают тестировать свои программы? Сначала запускают код, а потом проверяют, работает ли.",
    "Что сказал программист своему начальнику, когда тот попросил его убрать все ошибки? 'Легко! Просто удалю весь код.'",
    "Почему программисты не могут держать секреты? Потому что они постоянно дебажат.",
    "Почему программисты не любят походы? Слишком много исключений в правилах.",
    "Какой любимый вид транспорта у программистов? Лупинг (looping).",
    "Почему программистам нравятся кошки? Потому что они понимают команды.",
    "Что сказал программист, когда его спросили, почему он пишет комментарии в коде? 'Чтобы понять, что я здесь делал через полгода.'",
    "Почему программисты всегда смотрят налево и направо, прежде чем перейти дорогу? Потому что им нужно проверить оба конца.",
    "Что сказал программист, когда его код сработал с первого раза? 'Я, наверное, что-то упустил.'",
    "Почему программистам не нравится поэзия? Слишком много переменных рифм.",
    "Какой любимый напиток у программистов? Кофе, потому что он сохраняет их в бодром состоянии.",
    "Почему программисты не ходят на свидания? Потому что они боятся выйти из зоны комфорта."
]

COMPLIMENTS = [
    "Ты сегодня выглядишь потрясающе!",
    "Ты умный и талантливый человек!",
    "Ты всегда находишь лучший выход из любой ситуации!",
    "У тебя отличный вкус!",
    "Ты светишься, когда улыбаешься!",
    "Ты всегда находишь нужные слова.",
    "Ты невероятно добрый человек!",
    "Ты всегда знаешь, как поднять настроение.",
    "Ты настоящий друг.",
    "Ты делаешь этот мир лучше.",
    "Ты излучаешь позитив.",
    "Твоя энергия заразительна.",
    "Ты всегда вдохновляешь окружающих.",
    "Ты очень креативный.",
    "Ты всегда готов помочь.",
    "Ты всегда держишь слово.",
    "Ты обладаешь замечательным чувством юмора.",
    "Ты делаешь людей счастливыми.",
    "Ты - уникальный и неповторимый.",
    "Ты - пример для подражания."
]


def random_joke():
    """Отправляет случайную шутку"""
    joke = random.choice(JOKES)
    return joke


def random_compliment():
    """Отправляет случайный комплимент"""
    compliment = random.choice(COMPLIMENTS)
    return compliment


def random_flip_a_coin():
    """Возвращает случайное значение Орёл или Решка"""
    return random.choice(("Орёл", "Решка"))