import pygame
import sys
import pickle
from game import TicTacToe
from agent import QLearningAgent

# 기본 설정
pygame.init()
BGWIDTH, BGHEIGHT = 800, 500
WIDTH, HEIGHT = 360, 440
CELL_SIZE = WIDTH // 3
board_origin_x = (BGWIDTH - WIDTH) // 2
board_origin_y = (BGHEIGHT - HEIGHT) // 2

screen = pygame.display.set_mode((BGWIDTH, BGHEIGHT))
pygame.display.set_caption("🧠 Q러닝 틱택토")

# 색상
WHITE = (245, 245, 245)
BLACK = (0, 0, 0)
LINE_COLOR = (30, 30, 30)
BG_COLOR = (220, 220, 220)
CIRCLE_COLOR = (0, 170, 255)
CROSS_COLOR = (255, 90, 90)
TURN_COLOR = (230, 230, 230)
WIN_COLOR = (80, 250, 123)

# 폰트
FONT = pygame.font.SysFont("arial", 28)
LARGE_FONT = pygame.font.SysFont("arial", 40, bold=True)

def draw_board(board):
    screen.fill(BG_COLOR)

    # 선 긋기 (중앙 정렬된 위치 기준)
    for i in range(1, 3):
        pygame.draw.line(screen, LINE_COLOR,
                         (board_origin_x, board_origin_y + CELL_SIZE * i),
                         (board_origin_x + WIDTH, board_origin_y + CELL_SIZE * i), 6)
        pygame.draw.line(screen, LINE_COLOR,
                         (board_origin_x + CELL_SIZE * i, board_origin_y),
                         (board_origin_x + CELL_SIZE * i, board_origin_y + WIDTH), 6)

    # 말 그리기
    for i in range(3):
        for j in range(3):
            x = board_origin_x + j * CELL_SIZE + CELL_SIZE // 2
            y = board_origin_y + i * CELL_SIZE + CELL_SIZE // 2
            if board[i][j] == 1:
                pygame.draw.circle(screen, CIRCLE_COLOR, (x, y), 40, 8)
            elif board[i][j] == 2:
                pygame.draw.line(screen, CROSS_COLOR, (x - 35, y - 35), (x + 35, y + 35), 8)
                pygame.draw.line(screen, CROSS_COLOR, (x + 35, y - 35), (x - 35, y + 35), 8)

def show_turn(player):
    text = f"Your trun" if player == 1 else "AI thinking..."
    render = FONT.render(text, True, BLACK)
    screen.blit(render, (board_origin_x, board_origin_y + WIDTH + 10))

def show_result(winner):
    if winner == 1:
        msg = "You win!!"
    elif winner == 2:
        msg = "You lose.."
    else:
        msg = "Draw!"

    pygame.draw.rect(screen, BG_COLOR, (0, WIDTH, WIDTH, 80))
    text = LARGE_FONT.render(msg, True, WIN_COLOR)
    screen.blit(text, (board_origin_x, board_origin_y + WIDTH + 10))

    pygame.display.flip()
    pygame.time.wait(1500)

def get_action_from_click(pos):
    x, y = pos
    col = (x - board_origin_x) // CELL_SIZE
    row = (y - board_origin_y) // CELL_SIZE
    if 0 <= row < 3 and 0 <= col < 3:
        return row, col
    return None  # 클릭이 보드 밖일 때

def draw_button(rect, text):
    pygame.draw.rect(screen, (100, 100, 100), rect, border_radius=10)
    label = FONT.render(text, True, WHITE)
    screen.blit(label, (
        rect.centerx - label.get_width() // 2,
        rect.centery - label.get_height() // 2
    ))

def show_result_with_buttons(winner):
    if winner == 1:
        msg = "You win!!"
    elif winner == 2:
        msg = "You lose.."
    else:
        msg = "Draw!"

    # 메시지 표시
    pygame.draw.rect(screen, BG_COLOR, (0, board_origin_y + WIDTH, BGWIDTH, 100))
    text = LARGE_FONT.render(msg, True, WIN_COLOR)
    screen.blit(text, (
        BGWIDTH // 2 - text.get_width() // 2,
        board_origin_y + WIDTH + 10
    ))

    # 버튼 생성
    replay_rect = pygame.Rect(BGWIDTH // 2 - 130, board_origin_y + WIDTH + 50, 100, 40)
    quit_rect = pygame.Rect(BGWIDTH // 2 + 30, board_origin_y + WIDTH + 50, 100, 40)

    draw_button(replay_rect, "Replay")
    draw_button(quit_rect, "Quit")

    pygame.display.flip()

    # 클릭 대기
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if replay_rect.collidepoint(event.pos):
                    return "replay"
                elif quit_rect.collidepoint(event.pos):
                    pygame.quit(); sys.exit()

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
                if action and action in env.available_actions():
                    state, reward, done = env.step(action)
                    if done:
                        draw_board(env.board)
                        result = show_result_with_buttons(env.get_winner())
                        if result == "replay":
                            return  # main()에서 다시 시작

        if env.current_player == 2:
            pygame.time.wait(400)
            action = agent.choose_action(state, env.available_actions())
            state, reward, done = env.step(action)
            if done:
                draw_board(env.board)
                result = show_result_with_buttons(env.get_winner())
                if result == "replay":
                    return

def show_difficulty_menu():
    screen.fill(BG_COLOR)
    options = [("easy", "pkl/q_easy.pkl"), ("normal", "pkl/q_normal.pkl"),
               ("hard", "pkl/q_hard.pkl"), ("master", "pkl/q_master.pkl")]

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
    while True:
        filename = show_difficulty_menu()
        with open(filename, "rb") as f:
            q_table = pickle.load(f)
        agent = QLearningAgent(epsilon=0.0)
        agent.q_table = q_table
        start_game(agent)


if __name__ == "__main__":
    main()
