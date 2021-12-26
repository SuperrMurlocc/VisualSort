import pygame
import random

pygame.init()

HEIGHT = 500
SCREEN_HEIGHT = HEIGHT + 100
WIDTH = 800

GAME_FONT = pygame.font.Font("src/Montserrat-Regular.otf", 20)


def generate_array(_len:int, _max:int=100) -> (list, list):
    _colors = [(255,255,255) for _ in range(_len)]
    _heights = []

    _from = list(range(1, _max))
    for _ in range(_len + 1):
        random.shuffle(_from)
        _heights.append(_from[0])
        del _from[0]

    return _colors, _heights


def generate_rects(_len, _max, _heights):
    segments_num = _len * 2 + 1         # +1 for left margin
    segments_width = WIDTH / segments_num
    segments_heigth_multiplier = HEIGHT / _max
    return [pygame.Rect((1+2*i) * segments_width, HEIGHT-_heights[i]*segments_heigth_multiplier, segments_width, _heights[i]*segments_heigth_multiplier) for i in range(_len)]



def main():
    _len = 20
    _max = 100
    colors, heights = generate_array(_len, _max)
    win = pygame.display.set_mode((WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Visual Sort")
    clock = pygame.time.Clock()

    run = True
    started = False
    finished = False

    switcher = 1

    i_iter = 0
    j_iter = 0

    speed = 15

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    run = False
                if event.key == pygame.K_s:
                    if finished != True:
                        started = not started
                if event.key == pygame.K_r:
                    colors, heights = generate_array(_len, _max)
                    finished = False
                    started = False
                    switcher = 1
                    i_iter = 0
                    j_iter = 0
                if event.key == pygame.K_RIGHT:
                    if speed < 60:
                        speed += 3
                if event.key == pygame.K_LEFT:
                    if speed > 5:
                        speed -= 3
                if event.key == pygame.K_UP:
                    if _len < 80:
                        _len = _len + 5
                        colors, heights = generate_array(_len, _max)
                        finished = False
                        started = False
                        switcher = 1
                        i_iter = 0
                        j_iter = 0
                if event.key == pygame.K_DOWN:
                    if _len > 5:
                        _len = _len - 5
                        colors, heights = generate_array(_len, _max)
                        finished = False
                        started = False
                        switcher = 1
                        i_iter = 0
                        j_iter = 0


        if started:
            if switcher:
                colors = [(255, 255, 255) for _ in range(_len)]            
                for i in range(_len - i_iter, _len):
                    colors[i] = (0, 255, 0)
                colors[j_iter] = (255, 0, 0)
                colors[j_iter + 1] = (255, 0, 0)
            else:
                if heights[j_iter] > heights[j_iter + 1]:
                    heights[j_iter], heights[j_iter + 1] = heights[j_iter + 1], heights[j_iter]
                j_iter += 1
                if j_iter == _len - i_iter - 1:
                    j_iter = 0
                    i_iter += 1
                if i_iter == _len - 1:
                    started = False
                    finished = True
                    colors = [(0, 255, 0) for _ in range(_len)]            

            switcher = (switcher + 1) % 2



        win.fill((0, 0, 0))


        _rects = generate_rects(_len, _max, heights)


        for i in range(_len):
            pygame.draw.rect(win, colors[i], _rects[i])


        #print_options
        options_label_1 = GAME_FONT.render(f"S - start, R - regenerate, Q - quit, LEFT/RIGHT slower/faster, now: {speed} FPS", 1, (255, 255, 255))
        options_label_2 = GAME_FONT.render(f"Creator: SuperrMurlocc, UP/DOWN - more/less elements, now: {_len}", 1, (255, 255, 255))
        win.blit(options_label_1, (20, HEIGHT + 15))
        win.blit(options_label_2, (20, HEIGHT + 45))

        pygame.display.update()
        clock.tick(speed)




if __name__ == "__main__":
    main()
