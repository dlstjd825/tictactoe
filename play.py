from game import TicTacToe
from agent import QLearningAgent
import pickle

def print_board(board):
    symbols = {0: '.', 1: 'X', 2: 'O'}
    for row in board:
        print(' '.join(symbols[cell] for cell in row))
    print()

def choose_difficulty():
    print("난이도를 선택하세요:")
    print("1. 쉬움")
    print("2. 보통")
    print("3. 어려움")
    print("4. 최상급")
    choice = input("번호 입력 (1~4): ")

    if choice == '1':
        return 1.0, "q_easy.pkl"
    elif choice == '2':
        return 0.5, "q_normal.pkl"
    elif choice == '3':
        return 0.1, "q_hard.pkl"
    else:
        return 0.0, "q_master.pkl"

def play():
    while True:
        env = TicTacToe()
        epsilon, q_file = choose_difficulty()
        ai = QLearningAgent(epsilon=epsilon)

        try:
            with open(q_file, "rb") as f:
                ai.q_table = pickle.load(f)
            print(f"✅ {q_file} 로딩 성공 (epsilon={epsilon})")
        except FileNotFoundError:
            print(f"❌ {q_file} 파일이 없습니다. 먼저 train.py로 학습시켜 주세요.")
            return
        
        state = env.reset()
        done = False
        print("\n게임 시작! 당신은 X (1P), AI는 O (2P)")
        print_board(env.board)

        while not done:
            if env.current_player == 1:
                try:
                    x, y = map(int, input("당신의 수 (행 열): ").split())
                    if (x, y) not in env.available_actions():
                        print("잘못된 수입니다. 다시 시도하세요.")
                        continue
                except:
                    print("형식이 잘못됐습니다. 예: 0 1")
                    continue
            else:
                actions = env.available_actions()
                action = ai.choose_action(env.get_state(), actions)
                x, y = action
                print(f"AI의 수: {x} {y}")

            state, reward, done = env.step((x, y))
            print_board(env.board)

            if done:
                winner = 3 - env.current_player
                print("플레이어", winner, "승리!" if reward == 1 else "무승부!")

        again = input("다시 하시겠습니까? (y/n): ")
        if again.lower() != 'y':
            break

if __name__ == "__main__":
    play()
 