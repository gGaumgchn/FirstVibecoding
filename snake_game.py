import pygame
import sys
import random
import time

# 初始化pygame
pygame.init()

# 游戏窗口设置
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE

# 颜色定义
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
DARK_GREEN = (0, 150, 0)
GRAY = (128, 128, 128)

# 游戏速度（帧率）
FPS = 10

class Snake:
    """贪吃蛇类"""
    def __init__(self):
        self.length = 1
        self.positions = [((GRID_WIDTH // 2), (GRID_HEIGHT // 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = GREEN
        self.score = 0

    def get_head_position(self):
        """获取蛇头的位置"""
        return self.positions[0]

    def update(self):
        """更新蛇的位置"""
        cur = self.get_head_position()
        x, y = self.direction
        new = (((cur[0] + x) % GRID_WIDTH), (cur[1] + y) % GRID_HEIGHT)
        if new in self.positions[2:]:
            return False  # 撞到自己，游戏结束
        self.positions.insert(0, new)
        if len(self.positions) > self.length:
            self.positions.pop()
        return True

    def reset(self):
        """重置蛇的状态"""
        self.length = 1
        self.positions = [((GRID_WIDTH // 2), (GRID_HEIGHT // 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.score = 0

    def render(self, surface):
        """绘制蛇"""
        for p in self.positions:
            pygame.draw.rect(surface, self.color, (p[0] * GRID_SIZE, p[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, DARK_GREEN, (p[0] * GRID_SIZE + 4, p[1] * GRID_SIZE + 4, GRID_SIZE - 8, GRID_SIZE - 8))

class Food:
    """食物类"""
    def __init__(self):
        self.position = (0, 0)
        self.color = RED
        self.randomize_position()

    def randomize_position(self):
        """随机生成食物位置"""
        self.position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))

    def render(self, surface):
        """绘制食物"""
        pygame.draw.rect(surface, self.color, (self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

class Game:
    """游戏主类"""
    def __init__(self):
        self.surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('贪吃蛇游戏')
        self.clock = pygame.time.Clock()

        # 尝试使用系统字体，如果失败则使用默认字体
        try:
            self.font = pygame.font.SysFont('Arial', 30)
            self.small_font = pygame.font.SysFont('Arial', 20)
        except:
            # 如果Arial不可用，使用默认字体
            self.font = pygame.font.Font(None, 30)
            self.small_font = pygame.font.Font(None, 20)

        self.reset()

    def reset(self):
        """重置游戏"""
        self.snake = Snake()
        self.food = Food()
        self.score = 0
        self.game_over = False

    def handle_keys(self):
        """处理键盘输入"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if self.game_over:
                    if event.key == pygame.K_r:
                        self.reset()
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()
                else:
                    if event.key == pygame.K_UP and self.snake.direction != DOWN:
                        self.snake.direction = UP
                    elif event.key == pygame.K_DOWN and self.snake.direction != UP:
                        self.snake.direction = DOWN
                    elif event.key == pygame.K_LEFT and self.snake.direction != RIGHT:
                        self.snake.direction = LEFT
                    elif event.key == pygame.K_RIGHT and self.snake.direction != LEFT:
                        self.snake.direction = RIGHT

    def draw_grid(self):
        """绘制网格线（可选）"""
        for y in range(0, int(GRID_HEIGHT)):
            for x in range(0, int(GRID_WIDTH)):
                if (x + y) % 2 == 0:
                    pygame.draw.rect(self.surface, GRAY, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    def run(self):
        """运行游戏主循环"""
        while True:
            self.handle_keys()

            if not self.game_over:
                # 更新蛇的位置
                if not self.snake.update():
                    self.game_over = True

                # 检查是否吃到食物
                if self.snake.get_head_position() == self.food.position:
                    self.snake.length += 1
                    self.snake.score += 10
                    self.food.randomize_position()

                # 绘制游戏画面
                self.surface.fill(BLACK)
                self.draw_grid()
                self.snake.render(self.surface)
                self.food.render(self.surface)

                # 显示分数
                score_text = self.font.render(f'分数: {self.snake.score}', True, WHITE)
                self.surface.blit(score_text, (10, 10))

                # 显示操作提示
                controls_text = self.small_font.render('方向键控制移动 | R:重新开始 | Q:退出', True, WHITE)
                self.surface.blit(controls_text, (10, WINDOW_HEIGHT - 30))
            else:
                # 游戏结束画面
                self.surface.fill(BLACK)
                game_over_text = self.font.render('游戏结束', True, RED)
                score_text = self.font.render(f'最终得分: {self.snake.score}', True, WHITE)
                restart_text = self.small_font.render('按 R 重新开始 | 按 Q 退出', True, WHITE)

                self.surface.blit(game_over_text, (WINDOW_WIDTH // 2 - 60, WINDOW_HEIGHT // 2 - 50))
                self.surface.blit(score_text, (WINDOW_WIDTH // 2 - 70, WINDOW_HEIGHT // 2))
                self.surface.blit(restart_text, (WINDOW_WIDTH // 2 - 120, WINDOW_HEIGHT // 2 + 50))

            pygame.display.update()
            self.clock.tick(FPS)

# 方向常量
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# 游戏说明
def print_instructions():
    """打印游戏安装和运行说明"""
    print("=" * 50)
    print("贪吃蛇游戏 - 安装和运行说明")
    print("=" * 50)
    print("\n1. 安装依赖:")
    print("   pip install pygame")
    print("\n2. 运行游戏:")
    print("   python snake_game.py")
    print("\n3. 游戏控制:")
    print("   - 方向键: 控制蛇的移动方向")
    print("   - R 键: 游戏结束后重新开始")
    print("   - Q 键: 退出游戏")
    print("\n4. 游戏规则:")
    print("   - 蛇会自动向前移动")
    print("   - 吃到红色食物得分并变长")
    print("   - 撞墙或撞到自己游戏结束")
    print("=" * 50)

if __name__ == '__main__':
    print_instructions()
    game = Game()
    game.run()