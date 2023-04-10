#!/usr/bin/env python3
from random import randint, shuffle


class BrickWall:
    """
    A class to represent a brick wall.

    Wall must consist of 1 one more rows. Each row has at least 1 brick in it.
    Each brick can be any arbitrary length, greater than zero.
    The resulting wall must have a rectangular shape.

    Visualizing a wall:
    | - bricks borders

    +-----------------------+
    |     |     |     |     |
    |   |   |   |       |   |
    |     |         |       |
    |   |   |   |      |    |
    +-----------------------+

    Attributes
    ----------
    wall: list[list[int]]
        matrix containing the bricks length
    crossing_sign: str
        the sign to be drawn when crossing the wall

    Methods
    -------
    get_row_len(self, index: int):
        Returns the length of a brick row by index, including all the brick borders.
    get_max_row_len(self):
        Returns the length of the longest brick row including all the brick borders.
    fill_wall_with_bricks(self, max_row_length: int, shuffle_rows: bool = False):
        Adds random bricks to the existing wall.
    create_wall(self, rows_number: int = None, row_length: int = None):
        Creates a new brick wall with a random bricks length using the given parameters.
        If nothing passed, picks a number of rows and a row length randomly.
    is_valid(self):
        Returns True if the wall is rectangular. Otherwise, False.
    normalize_wall(self):
        Adds the missing bricks to make the wall rectangular.
    find_min_brick_crossline_position(self):
        Returns the index of the wall, where the line crosses minimal number of bricks.
    draw_wall_border(self, crossline_pos: int = None):
        Draws the border of a brick wall. Adds a crossing sign if `crossline_pos` passed.
    draw_wall(self):
        Outputs the brick wall to the terminal.
    draw_wall_crossline(self, position: int):
        Outputs the brick wall with a crossing line to the terminal.

    """

    max_rows_number = 10
    max_row_length = 50
    max_extra_length = 10

    def __init__(self, wall: list[list[int]] = None) -> None:
        """Initializes all the necessary attributes fot the brick wall object."""

        self.wall = wall
        self.crossing_sign = "x"

    @property
    def wall(self):
        return self._wall

    @wall.setter
    def wall(self, value):
        if value is None:
            self.create_wall()
        else:
            if not all(isinstance(brick_len, int) for row in wall for brick_len in row):
                raise TypeError("The wall must be list of lists of integers")
            self._wall = value

    @property
    def crossing_sign(self):
        return self._crossing_sign

    @crossing_sign.setter
    def crossing_sign(self, value):
        if len(value) != 1:
            raise ValueError("`crossline_sign` argument must be 1 character long")
        self._crossing_sign = value

    def get_row_len(self, index: int) -> int:
        """Returns the length of a brick row by index, including all the brick borders."""

        row = self.wall[index]
        return sum(row) + len(row) + 1

    def get_max_row_len(self) -> int:
        """Returns the length of the longest brick row including all the brick borders."""

        return max([self.get_row_len(i) for i in range(len(self.wall))])

    def fill_wall_with_bricks(self, max_row_length: int, shuffle_rows: bool = False) -> None:
        """Adds random bricks to the existing wall."""

        max_row_length -= 2  # subtract 2 symbols for row edges

        for row in self.wall:
            if len(row) == 0:
                count = 0
            else:
                count = sum(row) + len(row)

            while count < max_row_length:
                num = randint(1, max_row_length)
                # row consists of 1 brick
                if (max_row_length - 1 <= num <= max_row_length) and count == 0:
                    row.append(max_row_length)
                    break
                # to increase the efficiency, stop producing random brick length
                # if 3 or less places left, just fill that space with a missing brick length
                if max_row_length - count <= 3:
                    row.append(max_row_length - count)
                    break
                # add a brick to the row if it fits and does not leave 1 extra place after
                if max_row_length - count >= num and max_row_length - count != num + 1:
                    row.append(num)
                    count += num + 1  # +1 to add a brick border sign "|"

        if shuffle_rows:
            for row in self.wall:
                shuffle(row)

    def create_wall(self, rows_number: int = None, row_length: int = None) -> None:
        """
        Creates a new brick wall with a random bricks length using the given parameters.
        If nothing passed, picks a number of rows and a row length randomly.
        """

        # validation
        if rows_number is None:
            rows_number = randint(1, BrickWall.max_rows_number)
        if not isinstance(rows_number, int):
            raise TypeError(f"`rows_number` must be integer, not {type(rows_number)}")
        if rows_number < 1:
            raise ValueError("The wall must consists of at least one row")
        if row_length is None:
            row_length = randint(10, BrickWall.max_row_length)
        if not isinstance(row_length, int):
            raise TypeError(f"`row_length` must be integer, not {type(rows_number)}")
        if row_length < 3:
            raise ValueError("The  row length must be greater than 3 to put at least one brick in")

        self.wall = [[] for row in range(rows_number)]
        self.fill_wall_with_bricks(row_length, shuffle_rows=True)

    def is_valid(self) -> bool:
        """Returns True if the wall is rectangular. Otherwise, False."""

        first_row_length = self.get_row_len(0)
        for row_index in range(1, len(self.wall)):
            row_length = self.get_row_len(row_index)
            if row_length != first_row_length:
                return False
        return True

    def normalize_wall(self) -> None:
        """Adds the missing bricks to make the wall rectangular."""

        if self.is_valid():
            return

        longest_row = self.get_max_row_len()
        self.fill_wall_with_bricks(longest_row)

        # if the wall is filled but there are still rows with less than 3 spaces at the end:
        # if it's NOT possible to fill the row with a brick,
        # add extra bricks to each row to make the wall rectangular
        if not self.is_valid():
            extra_length = randint(3, BrickWall.max_extra_length)
            self.fill_wall_with_bricks(longest_row + extra_length)

    def find_min_brick_crossline_position(self) -> int:
        """Returns the index of the wall, where the line crosses minimal number of bricks."""

        if not self.is_valid():
            self.normalize_wall()

        intersections = {}
        for row in self.wall:
            count = 0
            for brick_length in row[:-1]:
                count += brick_length + 1
                intersections[count] = intersections.get(count, 0) + 1

        # if each row only consists of 1 brick, `intersections` will be empty
        if not intersections:
            return 1
        return max(intersections, key=intersections.get)

    def draw_wall_border(self, crossline_pos: int = None) -> None:
        """Draws the border of a brick wall. Adds a crossing sign if `crossline_pos` passed."""

        # draw '+' sign on the left and right edges of the wall,
        # all other space fill in with a '-' sign
        border_str = "-" * self.get_max_row_len()
        border_str = f"+{border_str[1:-1]}+"

        if crossline_pos is not None:
            border_str = (
                border_str[:crossline_pos] + self.crossing_sign + border_str[crossline_pos + 1 :]
            )
        print(border_str)

    def draw_wall(self) -> None:
        """Outputs the brick wall to the terminal."""

        self.draw_wall_border()
        for row in self.wall:
            row_str = "|"
            for brick_length in row:
                row_str += " " * brick_length + "|"
            print(row_str)
        self.draw_wall_border()

    def draw_wall_crossline(self, position: int) -> None:
        """Outputs the brick wall with a crossing line to the terminal."""

        if position <= 0 or position >= self.get_max_row_len() - 1:
            raise ValueError(
                "The line can not cross the wall at its edges. "
                "Check out the crossline position you passed"
            )

        self.draw_wall_border(position)
        for row in self.wall:
            row_str = "|"
            pos = 1
            for brick_length in row:
                for _ in range(brick_length):
                    row_str += self.crossing_sign if pos == position else " "
                    pos += 1
                row_str += "|"
                pos += 1
            print(row_str)
        self.draw_wall_border(position)


if __name__ == "__main__":
    wall = [
        [5, 5, 5, 5],
        [3, 3, 3, 7, 3],
        [5, 9, 7],
        [3, 3, 3, 6, 4],
    ]
    brick_wall = BrickWall(wall)
    # brick_wall = BrickWall()
    brick_wall.draw_wall()
    index = brick_wall.find_min_brick_crossline_position()
    brick_wall.draw_wall_crossline(index)
