from engine import Game
from matplotlib import pyplot as plt
import numpy as np

n_games = 1000
n_shots = []
n_wins1 = 0
n_wins2 = 0

# Проведення ігор
for i in range(n_games):
    game = Game(human1=False, human2=False)
    while not game.over:
        if game.player1_turn:
            game.converging_search_ai()
        else:
            game.converging_search_ai()
    n_shots.append(game.n_shots)
    if game.result == 1:
        n_wins1 += 1
    elif game.result == 2:
        n_wins2 += 1

# Виведення результатів
print(f"Перемог гравця 1: {n_wins1}")
print(f"Перемог гравця 2: {n_wins2}")
print(f"Середня кількість пострілів: {np.mean(n_shots):.2f}")
print(f"Медіана кількості пострілів: {np.median(n_shots)}")
print(f"Мінімум: {min(n_shots)}, Максимум: {max(n_shots)}")

# Побудова гістограми розподілу пострілів
plt.figure(figsize=(12, 6))
plt.hist(n_shots, bins=range(min(n_shots), max(n_shots) + 1), color='skyblue', edgecolor='black')
plt.title("Розподіл кількості пострілів")
plt.xlabel("Кількість пострілів")
plt.ylabel("Кількість ігор")
plt.grid(True)
plt.show()

# Boxplot для пострілів
plt.figure(figsize=(8, 5))
plt.boxplot(n_shots, vert=False)
plt.title("Boxplot кількості пострілів")
plt.xlabel("Кількість пострілів")
plt.grid(True)
plt.show()

# Лінійний графік середнього значення з кумулятивним підрахунком
cumulative_mean = [np.mean(n_shots[:i]) for i in range(10, n_games, 10)]
plt.figure(figsize=(10, 5))
plt.plot(range(10, n_games, 10), cumulative_mean, label='Кумулятивна середня')
plt.title("Зміна середньої кількості пострілів по іграх")
plt.xlabel("Кількість ігор")
plt.ylabel("Середня кількість пострілів")
plt.grid(True)
plt.legend()
plt.show()

# Діаграма перемог
plt.figure(figsize=(6, 6))
plt.pie([n_wins1, n_wins2], labels=['Гравець 1', 'Гравець 2'], autopct='%1.1f%%', startangle=90, colors=['#66b3ff', '#ff9999'])
plt.title("Відсоток перемог кожного гравця")
plt.show()
