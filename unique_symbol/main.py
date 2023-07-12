import re
from collections import Counter


def find_first_unique(s: str) -> str:
    counts = Counter(s)
    for symbol in s:
        if counts[symbol] == 1:
            return symbol
    return ""


def solution(text: str) -> str:
    words = re.findall(r"[\w'-]+", text)
    symbols = [find_first_unique(word) for word in words]
    return find_first_unique("".join(symbols))


if __name__ == "__main__":
    with open("data.txt", "r", encoding="utf-8") as file:
        text = file.read()

    print(solution(text))
