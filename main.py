from pygame import *

font.init()

class Cell(sprite.Sprite):
    def __init__(self, x, y, size, is_alive=False):
        super().__init__()

        self.image = Surface((size, size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.is_alive = is_alive

    def update(self):
        fill_color = (125, 125, 125)
        if self.is_alive:
            fill_color = (0, 125, 0)

        self.image.fill(fill_color)
        win.blit(self.image, self.rect)


def update_state_cells(matrix: list[list[Cell]]):
    len_col = len(matrix)
    len_row = len(matrix[0])  # используем 0, так как предполагаем, что все строки одной длины

    next_state = [[cell.is_alive for cell in row] for row in matrix]

    for i in range(len_col):
        for j in range(len_row):
            count = sum([
                matrix[(i - 1) % len_col][(j - 1) % len_row].is_alive,
                matrix[i % len_col][(j - 1) % len_row].is_alive,
                matrix[(i + 1) % len_col][(j - 1) % len_row].is_alive,
                matrix[(i - 1) % len_col][j % len_row].is_alive,
                matrix[(i + 1) % len_col][j % len_row].is_alive,
                matrix[(i - 1) % len_col][(j + 1) % len_row].is_alive,
                matrix[i % len_col][(j + 1) % len_row].is_alive,
                matrix[(i + 1) % len_col][(j + 1) % len_row].is_alive
            ])

            if matrix[i][j].is_alive:
                next_state[i][j] = count == 2 or count == 3
            else:
                next_state[i][j] = count == 3

    for i in range(len_col):
        for j in range(len_row):
            matrix[i][j].is_alive = next_state[i][j]


def count_alive_cells(matrix: list[list[Cell]]) -> int:
    count_alive = 0
    for row in matrix:
        for cell in row:
            count_alive += cell.is_alive
    return count_alive

width, height = 500, 500
cell_size = 9
margin = 1
update_state = 0
speed = 10

win = display.set_mode((width, height))
display.set_caption("Game of life")
win.fill((255, 255, 255))

game, pause = True, True

cells = []
for i in range(height // (cell_size + margin)):
    row = []
    y = (cell_size + margin) * i
    for j in range(width // (cell_size + margin)):
        row.append(Cell((cell_size + margin) * j, y, cell_size))
    cells.append(row)

len_col = len(cells)
len_row = len(cells[-1])

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN and e.key == K_p:
            pause = not pause
        if e.type == KEYDOWN and e.key == K_PLUS:
            speed += 2
        if e.type == KEYDOWN and e.key == K_MINUS:
            speed = max(speed - 1, 1)
        if e.type == MOUSEBUTTONDOWN and e.button == BUTTON_LEFT:
            col = min(e.pos[1] // (cell_size + margin), len_col)
            row = min(e.pos[0] // (cell_size + margin), len_row)
            cells[col][row].is_alive = not cells[col][row].is_alive

    win.fill((255, 255, 255))

    for row in cells:
        for cell in row:
            cell.update()

    if not pause:
        update_state_cells(cells)
        if count_alive_cells(cells) > 0:
            update_state += 1
    else:
        win.blit(
            font.SysFont("Arial", 32).render("PAUSE", True, (255, 0, 0)),((width//2)-30, height//2)
        )

    win.blit(
        font.SysFont("Arial", 26).render(f"Кол-во поколений: {update_state}", True, (0, 255, 0)), (25, 25)
    )

    display.update()
    time.Clock().tick(speed)
