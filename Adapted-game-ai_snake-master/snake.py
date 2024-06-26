#
# 本代码是基于pyzero中example/snake代码，进行了修改
# pyzero下载地址：https://github.com/lordmauve/pgzero
# 修改的内容为：（1）建立一个进程，添加网络socket通信，获取上下左右控制键，
#               本程序通过我的人体行为分析获取，双手的位置，给出上下左右控制键；
#              （2）获取到按键后，更新小蛇的运动状态
#              （3）有中文注释的，是我新增的代码


import random
from enum import Enum
from collections import deque
from itertools import islice

from pygame.transform import flip, rotate

#新增的python库，包含进程、消息队列、时间库和网络通信库
from multiprocessing import Process, Queue
import multiprocessing
import time
import socket
import math
import os

TILE_SIZE = 24

#修改了窗口的大小
TILES_W = 50
TILES_H = 35

WIDTH = TILE_SIZE * TILES_W
HEIGHT = TILE_SIZE * TILES_H


def screen_rect(tile_pos):
    """Get the screen rectangle for the given tile coordinate."""
    x, y = tile_pos
    return Rect(TILE_SIZE * x, TILE_SIZE * y, TILE_SIZE, TILE_SIZE)


class Direction(Enum):
    RIGHT = (1, 0)
    UP = (0, -1)
    LEFT = (-1, 0)
    DOWN = (0, 1)

    def opposite(self):
        x, y = self.value
        return Direction((-x, -y))


class Crashed(Exception):
    """The snake has crashed into itself."""


class Snake:
    def __init__(self, pos=(TILES_W // 2, TILES_H // 2)):
        self.pos = pos
        self.dir = Direction.LEFT
        self.length = 4
        self.tail = deque(maxlen=self.length)

        x, y = pos
        for i in range(self.length):
            p = (x + i, y)
            segment = p, self.dir
            self.tail.append(segment)

    @property
    def lastdir(self):
        return self.tail[0][1]

    def move(self):
        dx, dy = self.dir.value
        px, py = self.pos
        px = (px + dx) % TILES_W
        py = (py + dy) % TILES_H

        self.pos = px, py
        segment = self.pos, self.dir
        self.tail.appendleft(segment)
        for t, d in islice(self.tail, 1, None):
            if t == self.pos:
                raise Crashed(t)

    def __len__(self):
        return self.length

    def __contains__(self, pos):
        return any(p == pos for p, d in self.tail)

    def grow(self):
        self.length += 1
        self.tail = deque(self.tail, maxlen=self.length)

    def draw(self):
        for pos in self.tail:
            screen.draw.filled_rect(screen_rect(pos), 'green')


class SnakePainter:
    def __init__(self):
        right, up, left, down = (d.value for d in Direction)
        straight = images.snake_straight
        corner = images.snake_corner
        corner2 = flip(corner, True, False)
        self.tiles = {
            # Straight sections in each direction
            (right, right): straight,
            (up, up): rotate(straight, 90),
            (left, left): rotate(straight, 180),
            (down, down): rotate(straight, 270),

            # Corner sections in the anticlockwise direction
            (right, up): corner,
            (up, left): rotate(corner, 90),
            (left, down): rotate(corner, 180),
            (down, right): rotate(corner, 270),

            # Corner sections in the clockwise direction
            (left, up): corner2,
            (up, right): rotate(corner2, -90),
            (right, down): rotate(corner2, -180),
            (down, left): rotate(corner2, -270),
        }

        head = images.snake_head
        self.heads = {
            right: head,
            up: rotate(head, 90),
            left: rotate(head, 180),
            down: rotate(head, 270),
        }

        tail = images.snake_tail
        self.tails = {
            right: tail,
            up: rotate(tail, 90),
            left: rotate(tail, 180),
            down: rotate(tail, 270),
        }

    def draw(self, snake):
        for i, (pos, dir) in enumerate(snake.tail):
            if not i:
                # draw head
                tile = self.heads[snake.dir.value]
            elif i >= len(snake.tail) - 1:
                # draw tail
                nextdir = snake.tail[i - 1][1]
                tile = self.tails[nextdir.value]
            else:
                nextdir = snake.tail[i - 1][1]
                key = dir.value, nextdir.value
                try:
                    tile = self.tiles[key]
                except KeyError:
                    tile = self.tiles[dir.value, dir.value]

            r = screen_rect(pos)
            screen.blit(tile, r)


class Apple:
    def __init__(self):
        self.pos = 0, 0

    def draw(self):
        screen.blit(images.apple_72, screen_rect(self.pos))


KEYBINDINGS = {
    keys.LEFT: Direction.LEFT,
    keys.RIGHT: Direction.RIGHT,
    keys.UP: Direction.UP,
    keys.DOWN: Direction.DOWN,
}


snake = Snake()
snake.alive = True

snake_painter = SnakePainter()

apple = Apple()

#定义一个进程间通信的共享变量，用于传递方向按键
mydict=multiprocessing.Manager().dict()
mydict['dir'] = "left"

def place_apple():
    """Randomly place the apple somewhere that isn't currently occupied.

    We will generate coordinates at random until we find some that are not on
    top of the snake.

    """
    if len(snake) == TILES_W * TILES_H:
        raise ValueError("No empty spaces!")

    while True:
        pos = (
            random.randrange(TILES_W - 2),
            random.randrange(TILES_H - 2)
        )

        if pos not in snake:
            apple.pos = pos
            return


def on_key_down(key):
    if not snake.alive:
        return

    dir = KEYBINDINGS.get(key)
    if dir and dir != snake.lastdir.opposite():
        snake.dir = dir
        return

def tick():
    if not snake.alive:
        return

    try:
	#新建根据获取的方向控制键，来更新小蛇的的运动状态
        if mydict['dir'] == 'up':
            dir = Direction.UP
            if dir and dir != snake.lastdir.opposite():
                snake.dir = dir
        elif mydict['dir'] == 'left':
            dir = Direction.LEFT
            if dir and dir != snake.lastdir.opposite():
                snake.dir = dir
        elif mydict['dir'] == 'right':
            dir = Direction.RIGHT
            if dir and dir != snake.lastdir.opposite():
                snake.dir = dir
        elif mydict['dir'] == 'down':
            dir = Direction.DOWN
            if dir and dir != snake.lastdir.opposite():
                snake.dir = dir
        else:
            pass
    
        snake.move()
    except Crashed:
        snake.alive = False
        stop()
    else:
        snake_x,snake_y = snake.pos
        apple_x,apple_y = apple.pos
        if ((snake_x >= apple_x) and (snake_y >= apple_y)) and \
                ((math.pow(snake_y - apple_y,2) + math.pow(snake_x - apple_x,2)) < 9):
        # if snake.pos == apple.pos:
            snake.grow()
            start()
            place_apple()

def start():
    """Set/update the tick interval.

    This is called whenever the snake grows to make the game run faster.

    """
    #interval = max(0.1, 0.4 - 0.03 * (len(snake) - 3))
    interval = 0.4
    clock.unschedule(tick)
    clock.schedule_interval(tick, interval)

def stop():
    """Stop the game from updating."""
    clock.unschedule(tick)


def draw():
    screen.clear()
    snake_painter.draw(snake)
    apple.draw()

    screen.draw.text(
        'Score: %d' % len(snake),
        color='white',
        topright=(WIDTH - 5, 5)
    )

    if not snake.alive:
        screen.draw.text(
            "You died!",
            color='white',
            center=(WIDTH/2, HEIGHT/2)
        )



#接收其他模块发送方向信息进程，从127.0.0.1:20163这个socket中接收
def get_direction_func(task_name, mydict):
    #　给出提示信息
    print(task_name + "任务启动")

    try:
        #创建udp的socket
        udpSocket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

        # 绑定端口号
        udpSocket.bind(("127.0.0.1", 20163))

        #获取按键信息
        while True:
            recvData = udpSocket.recvfrom(1024)
            content, destInfo = recvData

            #获取按键值
            direct_key = content.decode("utf-8")

            #根据按键，执行动作
            if direct_key == "上键":
                mydict['dir'] = 'up'
            elif direct_key == "左键":
                mydict['dir'] = 'left'
            elif direct_key == "右键":
                mydict['dir'] = 'right'
            elif direct_key == "下键":
                mydict['dir'] = 'down'
            else:
                pass


    except KeyboardInterrupt:
        #释放套接字
        udpSocket.close()


#创建获取其他模块发送方向信息的进程
get_direction = Process(target=get_direction_func, args=("获取方向程序", mydict))

#启动该进程
get_direction.start()

#播放背景音乐
#music.play("music_one.mp3")

#贪吃蛇原来的功能启动
place_apple()
start()
