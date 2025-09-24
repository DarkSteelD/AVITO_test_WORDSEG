import wikipediaapi
import re
from tqdm import tqdm
import nltk
import ssl

def setup_nltk():
    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        pass
    else:
        ssl._create_default_https_context = _create_unverified_https_context

    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        print("Скачиваем NLTK-пакет 'punkt' для токенизации предложений...")
        nltk.download('punkt')
        
    try:
        nltk.data.find('tokenizers/punkt_tab')
    except LookupError:
        print("Скачиваем NLTK-пакет 'punkt_tab' для поддержки русского языка...")
        nltk.download('punkt_tab')


def clean_sentence(sentence: str) -> str:
    sentence = sentence.lower()
    sentence = re.sub(r'[^а-яё\s]', '', sentence)
    sentence = re.sub(r'\s+', ' ', sentence).strip()
    return sentence

def parse_wikipedia_sentences(topics: list, output_file: str, user_agent: str, min_sentence_len: int = 3):
    print("Инициализация API Википедии для русского языка...")
    wiki_api = wikipediaapi.Wikipedia(
        user_agent=user_agent,
        language='ru',
        extract_format=wikipediaapi.ExtractFormat.WIKI
    )
    
    total_sentences_written = 0
    
    print(f"Начинаем парсинг {len(topics)} тем. Результат будет сохранен в '{output_file}'")

    with open(output_file, 'w', encoding='utf-8') as f_out:
        for topic in tqdm(topics, desc="Парсинг тем"):
            page = wiki_api.page(topic)
            if page.exists():
                # Разбиваем весь текст статьи на предложения
                raw_sentences = nltk.sent_tokenize(page.text, language='russian')
                
                for sent in raw_sentences:
                    cleaned = clean_sentence(sent)
                    # Сохраняем только осмысленные предложения
                    if len(cleaned.split()) >= min_sentence_len:
                        f_out.write(cleaned + '\n')
                        total_sentences_written += 1
            else:
                print(f"Предупреждение: статья '{topic}' не найдена.")

    print("\nПарсинг предложений успешно завершен!")
    print(f"Всего предложений записано в корпус: {total_sentences_written}")
    print(f"Корпус сохранен в файл: '{output_file}'")

if __name__ == '__main__':
    setup_nltk()
    
    MY_USER_AGENT = 'WordSegmentationContest/1.0 (justjoke.exe@gmail.com)'
    
    TOPICS_TO_PARSE = [
        "Смартфон", "Ноутбук", "Телевизор", "Компьютер", "Планшетный компьютер",
        "Наушники", "Apple", "Samsung", "Xiaomi", "Honor", "PlayStation 5",
        "Квартира", "Дом", "Аренда", "Ремонт", "Мебель", "Диван", "Шкаф",
        "Холодильник", "Стиральная машина", "Кухня", "Автомобиль", "Велосипед",
        "ВАЗ", "Toyota", "Volkswagen", "BMW", "Работа", "Резюме", "Услуги",
        "Строительство", "Образование", "Репетитор", "Собака", "Кошка",
        "Одежда", "Обувь", "Куртка", "Джинсы", "Книга", "Россия", "Москва",
        "Экономика", "Русский язык", "Литература", "Музыка"
    ]
    
    OUTPUT_CORPUS_FILE = 'external_sentences_corpus.txt'
    
    parse_wikipedia_sentences(TOPICS_TO_PARSE, OUTPUT_CORPUS_FILE, MY_USER_AGENT)
