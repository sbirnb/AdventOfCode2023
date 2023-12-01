import re
import sys
from typing import Iterable

DIGIT_NAMES = {
    **{name: str(value) for value, name in enumerate(
        ('one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine'), 1
    )},
    **{str(value): str(value) for value in range(1, 10)}
}
MATCH_DIGIT_NAME = '|'.join(rf'(?<=({name}))' for name in DIGIT_NAMES)


def solve(input_: Iterable[str], digit_pattern: str) -> int:
    return sum(
        int(''.join(DIGIT_NAMES[name] for name in filter(bool, re.search(digit_pattern, row).groups())))
        for row in input_
    )


if __name__ == '__main__':
    input_ = tuple(sys.stdin)
    print(solve(input_, r'(?<=(\d)).*(?<=(\d))[a-z]*$'))
    print(solve(input_, rf'(?:{MATCH_DIGIT_NAME}).*(?:{MATCH_DIGIT_NAME})[a-z]*$'))
