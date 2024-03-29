def read(loc: str) -> tuple[list[tuple[int, int]], list[tuple[str, int]]]:
    with open(loc) as f:
        r = f.readlines()
        split = r.index("\n")
        points, folds = r[:split], r[split+1:]

        points = [row.split(",") for row in points]
        points = [(int(row[0]), int(row[1])) for row in points]

        folds = [row[11:].split("=") for row in folds]
        folds = [(axis, int(pos)) for axis, pos in folds]

    return points, folds


def fold(grid: list[list[bool]], axis: str, pos: int) -> list[list[bool]]:
    if axis == 'y':
        # print(f"Dimensions:, y:{len(grid)}, x:{len(grid[0])}")
        poss = [(pos, k) for k, x in enumerate(grid[0])]
        # print(poss)
        new_grid = [[False for _ in range(len(grid[0]))] for _ in range(pos)]
        for y, x in poss:
            matches = [((y-k, x), (y+k, x)) for k in range(1, pos+1)]
            # print(matches)
            try:
                for a, b in matches:
                    new_grid[a[0]][a[1]] = grid[a[0]][a[1]] or grid[b[0]][b[1]]
            except IndexError:
                pass
        return new_grid

    else:
        assert axis == 'x'
        grid = list(map(list, zip(*grid)))
        new_grid = fold(grid, 'y', pos)
        new_grid = list(map(list, zip(*new_grid)))
        return new_grid


def build_grid(points: list[tuple[int, int]]) -> list[list[bool]]:
    n = max(points, key=lambda p: p[0])[0]
    m = max(points, key=lambda p: p[1])[1]
    grid = [[False for _ in range(n + 1)] for _ in range(m + 1)]
    for x, y in points:
        grid[y][x] = True
    return grid


def print_grid(grid: list[list[bool]]):
    if not grid:
        grid = [[]]
    prnt = ""
    trs = {
        True: '#',
        False: '.'
    }
    for row in grid:
        prnt += "".join([trs[x] for x in row])
        prnt += "\n"
    print(prnt)
    print(f"Number of dots: {prnt.count('#')}")


def first(loc: str = "./data/13.txt"):
    points, folds = read(loc)
    grid = build_grid(points)
    grid = fold(grid, folds[0][0], folds[0][1])
    print_grid(grid)


def second(loc: str = "./data/13.txt"):
    points, folds = read(loc)
    grid = build_grid(points)
    for axis, pos in folds:
        grid = fold(grid, axis, pos)
    print_grid(grid)


if __name__ == '__main__':
    first()
    second()

