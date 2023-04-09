import pytest

from maze import make_maze, ellers_algorithm, lee_algorithm


class TestEllersAlgorithm:
    def test_maze_with_height_and_width_greater_than_one(self):
        maze = [[' ' for _ in range(2 * 3 + 1)] for _ in range(2 * 4 + 1)]
        result = ellers_algorithm(maze, 4, 3)
        assert len(result) == 9
        assert len(result[0]) == 7

    def test_maze_with_height_or_width_equal_to_one(self):
        maze = [[' ' for _ in range(2 * 1 + 1)] for _ in range(2 * 4 + 1)]
        result = ellers_algorithm(maze, 4, 1)
        assert len(result) == 9
        assert len(result[0]) == 3

    def test_maze_with_height_equal_to_one_and_width_greater_than_one(self):
        maze = [[' ' for _ in range(2 * 3 + 1)] for _ in range(2 * 1 + 1)]
        result = ellers_algorithm(maze, 1, 3)
        assert len(result) == 3
        assert len(result[0]) == 7

    def test_maze_with_height_or_width_equal_to_zero(self):
        maze = [[' ' for _ in range(2 * 0 + 1)] for _ in range(2 * 4 + 1)]
        result = ellers_algorithm(maze, 4, 0)
        assert len(result) == 1
        assert len(result[0]) == 1

    def test_maze_with_height_or_width_less_than_zero(self):
        maze = [[' ' for _ in range(2 * -1 + 1)] for _ in range(2 * -4 + 1)]
        with pytest.raises(ValueError):
            result = ellers_algorithm(maze, -4, -1)

    def test_maze_with_odd_height_or_width(self):
        maze = [[' ' for _ in range(2 * 5 + 1)] for _ in range(2 * 7 + 1)]
        result = ellers_algorithm(maze, 7, 5)
        assert len(result) == 15
        assert len(result[0]) == 11


class TestMakeMaze:
    def test_positive_dimensions(self):
        maze = make_maze(5, 5)
        assert len(maze) == 11
        assert len(maze[0]) == 11

    def test_single_dimension(self):
        maze = make_maze(1, 1)
        assert len(maze) == 3
        assert len(maze[0]) == 3

    def test_zero_dimension(self):
        with pytest.raises(ValueError):
            make_maze(0, 5)

    def test_negative_dimension(self):
        with pytest.raises(ValueError):
            make_maze(-5, 5)

    def test_single_path(self):
        global current
        maze = make_maze(5, 5)
        start = (1, 1)
        end = (9, 9)
        visited = set()
        queue = [start]
        while queue:
            current = queue.pop(0)
            if current == end:
                break
            visited.add(current)
            row, col = current
            if row > 1 and maze[row - 1][col] == ' ' and (row - 2, col) not in visited:
                queue.append((row - 2, col))
            if row < len(maze) - 2 and maze[row + 1][col] == ' ' and (row + 2, col) not in visited:
                queue.append((row + 2, col))
            if col > 1 and maze[row][col - 1] == ' ' and (row, col - 2) not in visited:
                queue.append((row, col - 2))
            if col < len(maze[0]) - 2 and maze[row][col + 1] == ' ' and (row, col + 2) not in visited:
                queue.append((row, col + 2))
        assert current == end

    def test_non_integer_dimensions(self):
        with pytest.raises(TypeError):
            make_maze(5.5, 5)


class TestLeeAlgorithm:
    def test_no_path(self):
        maze = "##########\n#        #\n# ###### #\n# #     ##\n# # ######\n#   #    #\n##########"
        assert lee_algorithm(maze) == []

    def test_one_point_maze(self):
        maze = "#"
        assert lee_algorithm(maze) == []

    def test_walled_maze(self):
        maze = "#########\n#       #\n#       #\n#       #\n#       #\n#       #\n#########"
        assert lee_algorithm(maze) == []

    def test_entry_on_wall(self):
        maze = "##########\n#        #\n# ###### #\n# #     ##\n# # ######\n#   #    #\n##########"
        assert lee_algorithm(maze) == []
