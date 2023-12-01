import re
import sys
from typing import Iterable

DIGIT_NAMES = {
    **{
        name: str(value) for value, name in enumerate(('one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine'), 1)
    },
    **{str(value): str(value) for value in range(1, 10)}
}
MATCH_DIGIT_NAME = '|'.join(fr'(?<=({name}))' for name in list(DIGIT_NAMES))


def get_calibration_number(calibration_string: str) -> int:
    return int(''.join(re.search(r'(?<=(\d)).*(?<=(\d))[a-z]*$', calibration_string).groups()))


def part1(input_: Iterable[str]) -> int:
    return sum(get_calibration_number(row.strip()) for row in input_)


def get_calibration_number2(calibration_string: str) -> int:
    return int(
        ''.join(
            DIGIT_NAMES[digit_name]
            for digit_name in
            re.search(rf'(?:{MATCH_DIGIT_NAME}).*(?:{MATCH_DIGIT_NAME})[a-z]*$', calibration_string).groups()
            if digit_name is not None
        )
    )

def part2(input_: Iterable[str]) -> int:
    return sum(get_calibration_number2(row) for row in input_)

if __name__ == '__main__':
    input_ = tuple(sys.stdin)
    print(part1(input_))
    print(part2(input_))
