
Цей проєкт реалізує гру "Морський бій" між двома гравцями, керованими штучним інтелектом. Основна мета — протестувати та порівняти ефективність різних стратегій AI-гравців.


battleshipAI/
├── .idea/                  
├── .venv/                 
├── engine.py               
├── main.py                  
├── tournament.py           
        
AI-алгоритми
Усередині engine.py реалізовані такі алгоритми:

random_ai() — випадкові постріли по всьому полю

basic_ai() — стрільба за шаблоном "шахівниця" + добивання

probability_ai() — оцінка ймовірностей можливих розташувань кораблів

hunting_targeting_ai() — перемикання між режимом пошуку і цілеспрямованої атаки

smart_hunting_ai() — покращений варіант з аналізом напрямку

converging_search_ai() — найпросунутіша стратегія з аналізом шаблонів і вузького пошуку

Встановлення
 Рекомендовано використовувати віртуальне середовище venv.

1. Клонування або розпакування проєкту:
git clone https://github.com/Yurii8830/BATTLESHIP_AI
cd battleshipAI
або розпакуйте battleshipAI.zip.

2. Встановлення залежностей:

pip install -r requirements.txt
(Якщо файл requirements.txt відсутній, вручну встановіть: matplotlib, pygame, numpy)

Запуск
Головна симуляція:
python main.py
Цей файл симулює серію ігор між двома AI-гравцями. За замовчуванням виконується 1000 ігор, після чого виводиться статистика:

Середня кількість пострілів

Медіана

Мінімум / максимум

Відсоток перемог

Запуск турніру:
python tournament.py
Цей скрипт дозволяє порівняти кілька AI один з одним та побудувати розширену статистику.

Виведення результатів
Виводяться у консоль та будуються такі графіки:

Гістограма розподілу кількості пострілів

Boxplot розподілу

Кумулятивна середня

Кругова діаграма перемог


