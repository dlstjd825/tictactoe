# train_all.py
import pickle
from game import TicTacToe
from agent import QLearningAgent

def train(agent, episodes=10000):
    env = TicTacToe()
    for episode in range(episodes):
        state = env.reset()
        done = False
        while not done:
            player = env.current_player
            actions = env.available_actions()
            action = agent.choose_action(state, actions)
            next_state, reward, done = env.step(action)
            next_actions = env.available_actions()

            # 보상 강화
            if done:
                if reward == 1:
                    reward = 30
                elif reward == -1:
                    reward = -1
                else:
                    reward = 0
            else:
                reward = -0.01

            adjusted_reward = reward if player == 2 else -reward
            agent.learn(state, action, adjusted_reward, next_state, next_actions)

        if (episode + 1) % 1000 == 0:
            print(f"[{agent.epsilon}] Episode {episode + 1} / {episodes}")

def train_all():
    settings = [
        ("easy", 1.0, 10000, "q_easy.pkl"),
        ("normal", 0.5, 20000, "q_normal.pkl"),
        ("hard", 0.1, 30000, "q_hard.pkl"),
        ("master", 0.01, 40000, "q_master.pkl")
        ]

    for difficulty, epsilon, episodes, filename in settings:
        print(f"\n🔧 난이도: {difficulty} ({epsilon}) → {filename}")
        agent = QLearningAgent(epsilon=epsilon, difficulty=difficulty)
        train(agent, episodes)
        with open(filename, "wb") as f:
            pickle.dump(agent.q_table, f)
        print(f"✅ {filename} 저장 완료")

if __name__ == "__main__":
    train_all()
