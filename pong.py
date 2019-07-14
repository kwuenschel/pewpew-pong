import pew

SCREEN_HEIGHT = 8
SCREEN_WIDTH = 8
DEFAULT_PADDLE_SIZE = 2
DEFAULT_Y_POS = (SCREEN_HEIGHT - DEFAULT_PADDLE_SIZE) // 2


class Direction:
    UP = -1
    DOWN = 1


class Axis:
    X = 1
    Y = 2
    BOTH = 3


class BallOut(Exception):
    def __init__(self, x_location):
        self.x_location = x_location


class Paddle:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size

    def move(self, diff):
        if self.y + self.size + diff > SCREEN_HEIGHT:
            self.y = SCREEN_HEIGHT - self.size
        elif self.y + diff >= 0:
            self.y += diff

    def get_range(self):
        return range(self.y, self.y + self.size)


class Ball:
    def __init__(self, x, y, x_speed, y_speed):
        self.x = x
        self.y = y
        self.x_speed = x_speed
        self.y_speed = y_speed

    def move(self):
        self.x += self.x_speed
        self.y += self.y_speed

        if self.x >= SCREEN_WIDTH:
            raise BallOut(self.x)
        elif self.x < 0:
            raise BallOut(self.x)

    def bounce(self, axis):
        if axis & Axis.X:
            self.x_speed *= -1
        if axis & Axis.Y:
            self.y_speed *= -1


class Board:
    def __init__(self, screen):
        self.screen = screen
        self.left_paddle = Paddle(0, DEFAULT_Y_POS, DEFAULT_PADDLE_SIZE)
        self.right_paddle = Paddle(SCREEN_WIDTH - 1, DEFAULT_Y_POS, DEFAULT_PADDLE_SIZE)
        self.ball = Ball(4, 2, -1, -1)
        self.draw()

    def move_paddle(self, paddle, direction):
        if direction == Direction.UP:
            self.screen.pixel(paddle.x, paddle.y + 1, 0)
        elif direction == Direction.DOWN:
            self.screen.pixel(paddle.x, paddle.y, 0)

        paddle.move(direction)

    def draw_ball(self):
        self.screen.pixel(self.ball.x, self.ball.y, 3)

    def draw_paddle(self, paddle):
        for y in range(paddle.size):
            self.screen.pixel(paddle.x, paddle.y + y, 2)

    def draw(self):
        self.draw_paddle(self.left_paddle)
        self.draw_paddle(self.right_paddle)
        self.draw_ball()
        pew.show(self.screen)

    def check_ball_touches_border(self):
        if self.ball.y == 0 or self.ball.y == SCREEN_HEIGHT - 1:
            self.ball.bounce(Axis.Y)

    def check_ball_touches_paddle(self):
        next_y = self.ball.y + self.ball.y_speed

        if self.ball.x == 1:
            if self.ball.y in self.left_paddle.get_range():
                self.ball.bounce(Axis.X)
            elif next_y in self.left_paddle.get_range():
                self.ball.bounce(Axis.BOTH)
        elif self.ball.x == SCREEN_WIDTH - 2:
            if self.ball.y in self.right_paddle.get_range():
                self.ball.bounce(Axis.X)
            elif next_y in self.right_paddle.get_range():
                self.ball.bounce(Axis.BOTH)

    def refresh(self):
        self.screen.pixel(self.ball.x, self.ball.y, 0)
        self.ball.move()

        self.check_ball_touches_border()
        self.check_ball_touches_paddle()

        self.draw()


def main():
    pew.init()
    screen = pew.Pix()

    while True:
        screen.box(0, 0, 0)
        board = Board(screen)
        board.draw()

        while not pew.keys():
            pew.tick(0.25)

        while True:
            pew.tick(0.25)

            keys = pew.keys()
            if keys & pew.K_UP:
                board.move_paddle(board.left_paddle, Direction.UP)
            if keys & pew.K_DOWN:
                board.move_paddle(board.left_paddle, Direction.DOWN)
            if keys & pew.K_O:
                board.move_paddle(board.right_paddle, Direction.UP)
            if keys & pew.K_X:
                board.move_paddle(board.right_paddle, Direction.DOWN)

            try:
                board.refresh()
            except BallOut:
                break


main()
