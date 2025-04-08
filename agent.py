import random

class QLearningAgent:
    def __init__(self, epsilon=0.1, difficulty='normal'):
        self.q_table = {}
        self.epsilon = epsilon
        self.alpha = 0.1
        self.gamma = 0.9
        self.difficulty = difficulty  # easy, normal, hard, master


    def get_q(self, state, action):
        state = str(state)  # ✅ 항상 문자열로 변환
        return self.q_table.get((state, action), 0.0)

    def choose_action(self, state, actions):
        import random

        # 쉬운 난이도는 일정 확률로 완전 랜덤
        if self.difficulty == 'easy' and random.random() < 0.3:
            return random.choice(actions)

        if self.difficulty == 'normal' and random.random() < 0.1:
            return random.choice(actions)

        # 원래 Q러닝 방식
        if random.random() < self.epsilon:
            return random.choice(actions)
        
        q_values = [self.q_table.get((state, a), 0) for a in actions]
        max_q = max(q_values)
        max_actions = [a for a, q in zip(actions, q_values) if q == max_q]
        return random.choice(max_actions)


    def learn(self, state, action, reward, next_state, next_actions):
        state = str(state)
        next_state = str(next_state)

        old_q = self.get_q(state, action)
        future_q = max([self.get_q(next_state, a) for a in next_actions]) if next_actions else 0
        new_q = old_q + self.alpha * (reward + self.gamma * future_q - old_q)
        self.q_table[(state, action)] = new_q

    # ✅ (선택) Q값 확인용 함수
    def print_sample_q(self, n=5):
        print("🔍 Q-table 예시:")
        for i, ((state, action), q) in enumerate(self.q_table.items()):
            if i >= n:
                break
            print(f"State: {state}, Action: {action}, Q: {q:.2f}")
