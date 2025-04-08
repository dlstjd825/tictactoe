import pygame
import sys
import pickle
from game import TicTacToe
from agent import QLearningAgent

# 기본 설정
pygame.init()
WIDTH, HEIGHT = 360, 440
CELL_SIZE = WIDTH // 3
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🧠 Q러닝 틱택토")

# 색상
WHITE = (245, 245, 245)
BLACK = (0, 0, 0)
LINE_COLOR = (30, 30, 30)
BG_COLOR = (200, 200, 200)
CIRCLE_COLOR = (0, 170, 255)
CROSS_COLOR = (255, 90, 90)
TURN_COLOR = (230, 230, 230)
WIN_COLOR = (80, 250, 123)

# 폰트
FONT = pygame.font.SysFont("arial", 28)
LARGE_FONT = pygame.font.SysFont("arial", 40, bold=True)

def draw_board(board):
    screen.fill(BG_COLOR)

    # 선 긋기
    for i in range(1, 3):
        pygame.draw.line(screen, LINE_COLOR, (0, CELL_SIZE * i), (WIDTH, CELL_SIZE * i), 6)
        pygame.draw.line(screen, LINE_COLOR, (CELL_SIZE * i, 0), (CELL_SIZE * i, WIDTH), 6)

    # 말 그리기
    for i in range(3):
        for j in range(3):
            x = j * CELL_SIZE + CELL_SIZE // 2
            y = i * CELL_SIZE + CELL_SIZE // 2
            if board[i][j] == 1:
                pygame.draw.circle(screen, CIRCLE_COLOR, (x, y), 40, 8)
            elif board[i][j] == 2:
                pygame.draw.line(screen, CROSS_COLOR, (x - 35, y - 35), (x + 35, y + 35), 8)
                pygame.draw.line(screen, CROSS_COLOR, (x + 35, y - 35), (x - 35, y + 35), 8)

def show_turn(player):
    text = f"Your turn" if player == 1 else "AI thinking.."
    render = FONT.render(text, True, TURN_COLOR)
    screen.blit(render, (20, WIDTH + 10))

def show_result(winner):
    if winner == 1:
        msg = "You win!!"
    elif winner == 2:
        msg = "You lose.."
    else:
        msg = "Draw!"

    pygame.draw.rect(screen, BG_COLOR, (0, WIDTH, WIDTH, 80))
    text = LARGE_FONT.render(msg, True, WIN_COLOR)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, WIDTH + 10))

    pygame.display.flip()
    pygame.time.wait(1500)

def get_action_from_click(pos):
    x, y = pos
    return y // CELL_SIZE, x // CELL_SIZE

def start_game(agent):
    env = TicTacToe()
    state = env.reset()

    running = True
    while running:
        draw_board(env.board)
        show_turn(env.current_player)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            if env.current_player == 1 and event.type == pygame.MOUSEBUTTONDOWN:
                action = get_action_from_click(event.pos)
                if action in env.available_actions():
                    state, reward, done = env.step(action)
                    if done:
                        draw_board(env.board)
                        show_result(env.get_winner())
                        state = env.reset()

        if env.current_player == 2:
            pygame.time.wait(400)
            action = agent.choose_action(state, env.available_actions())
            state, reward, done = env.step(action)
            if done:
                draw_board(env.board)
                show_result(env.get_winner())
                state = env.reset()

def show_difficulty_menu():
    screen.fill(BG_COLOR)
    options = [("easy", "q_easy.pkl"), ("normal", "q_normal.pkl"),
               ("hard", "q_hard.pkl"), ("master", "q_master.pkl")]

    buttons = []
    for idx, (label, file) in enumerate(options):
        rect = pygame.Rect(80, 60 + idx * 80, 200, 50)
        pygame.draw.rect(screen, (100, 100, 100), rect, border_radius=10)
        text = FONT.render(label, True, WHITE)
        screen.blit(text, (rect.x + 60, rect.y + 10))
        buttons.append((rect, file))

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for rect, file in buttons:
                    if rect.collidepoint(event.pos):
                        return file

def main():
    filename = show_difficulty_menu()
    with open(filename, "rb") as f:
        q_table = pickle.load(f)
    agent = QLearningAgent(epsilon=0.0)
    agent.q_table = q_table
    start_game(agent)

if __name__ == "__main__":
    main()
