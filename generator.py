import argparse
import pytest
import json
import random

def generate2(pfsa: dict[str, dict[str, float]]) -> str:
    currentGram=random.choices(list(pfsa["*"].keys()), weights=tuple(pfsa["*"].values()), k=1)[0]
    result=currentGram
    while True:
        next_char = random.choices(list(pfsa[currentGram].keys()), weights=list(pfsa[currentGram].values()), k=1)[0]
        if next_char[-1]=="*":
            return result
        result = next_char
        currentGram = result
    return ""

def generate(pfsa: dict[str, dict[str, float]], word_count: int) -> str:
    result2=""
    for i in range(word_count):
        result2 +=(generate2(pfsa)+" ")
        print(result2)
    return result2.rstrip(" ")


def main():
    """
    The command for running is `python generator.py text.json 5`. This will
    generate a file `text_sample.txt` which has 5 randomly sampled words.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=str, help="Name of the text file")
    parser.add_argument("count", type=int, help="Sample size to gen")
    args = parser.parse_args()

    with open(args.file, "r") as file:
        data = json.load(file)
        output = generate(data, args.count)

    name = args.file.split(".")[0]

    with open(f"{name}_sample.txt", "w") as file:
        file.write(output)


if __name__ == "__main__":
    main()


DICTIONARIES = [
    {
        "*": {"a": 1.0},
        "a": {"a*": 1.0},
    },
    {
        "*": {"a": 1.0},
        "a": {"a*": 1.0},
    },
    {
        "*": {"a": 1.0},
        "a": {"a*": 1.0},
    },
    {
        "*": {"c": 1.0},
        "c": {"ca": 1.0},
        "ca": {"cat": 1.0},
        "cat": {"cat*": 1.0},
    },
]
STRINGS = [
    "a",
    "a a a a a",
    "",
    "cat cat cat cat",
]
COUNT = [1, 5, 0, 4]

COMBINED = [(d, s, c) for d, (s, c) in zip(DICTIONARIES, zip(STRINGS, COUNT))]


@pytest.mark.parametrize("pfsa, string, count", COMBINED)
def test_output_match(pfsa, string, count):
    """
    To test, install `pytest` beforehand in your Python environment.

    Run `pytest pfsa.py` Your code must pass all tests. There are additional
    hidden tests that your code will be tested on during VIVA.
    """
    result = generate(pfsa, count)
    assert result == string