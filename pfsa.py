import argparse
import pytest
import json

def construct(file_str: str) -> dict[str, dict[str, float]]:
    """Takes in the string representing the file and returns pfsa
    The given example is for the statement "A cat"
    """
    '''if file_str=="":
        return {
        "*": {},
    }'''
    d={}
    file_str=file_str.lower()
    l=list(file_str.split(" "))
    for i in l:
        for j in range(len(i)):
            if j!=0 and i[0:j] not in d:
                d[i[0:j]]=[]
                d[i[0:j]].append(i[0:j]+i[j])
            elif j==0:
                if "*" not in d:
                    d["*"]=[]
                d["*"].append(i[0:j]+i[j])
            else:
                d[i[0:j]].append(i[0:j]+i[j])
        if i not in d:
            if i=="":
                d["*"]=[]
            else:
                d[i]=[]
        if len(i)!=0:
            d[i].append(i+"*")
    for k,v in d.items():
        r={}
        sums=len(v)
        for i in v:
            if i in r:
                r[i]+=1
            else:
                r[i]=1
        for kr,vr in r.items():
            r[kr]=vr/sums
        d[k]=r
    return d


def main():
    """
    The command for running is `python pfsa.py text.txt`. This will generate
    a file `text.json` which you will be using for generation.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=str, help="Name of the text file")
    args = parser.parse_args()

    with open(args.file, "r") as file:
        contents = file.read()
        output = construct(contents)

    name = args.file.split(".")[0]

    with open(f"{name}.json", "w") as file:
        json.dump(output, file)


if __name__ == "__main__":
    main()


STRINGS = ["A cat", "A CAT", "", "A", "A A A A"]
DICTIONARIES = [
    {
        "*": {"a": 0.5, "c": 0.5},
        "a": {"a*": 1.0},
        "c": {"ca": 1.0},
        "ca": {"cat": 1.0},
        "cat": {"cat*": 1.0},
    },
    {
        "*": {"a": 0.5, "c": 0.5},
        "a": {"a*": 1.0},
        "c": {"ca": 1.0},
        "ca": {"cat": 1.0},
        "cat": {"cat*": 1.0},
    },
    {
        "*": {},
    },
    {
        "*": {"a": 1.0},
        "a": {"a*": 1.0},
    },
    {
        "*": {"a": 1.0},
        "a": {"a*": 1.0},
    },
]


@pytest.mark.parametrize("string, pfsa", list(zip(STRINGS, DICTIONARIES)))
def test_output_match(string, pfsa):
    """
    To test, install `pytest` beforehand in your Python environment.
    Run `pytest pfsa.py` Your code must pass all tests. There are additional
    hidden tests that your code will be tested on during VIVA.
    """
    result = construct(string)
    assert result == pfsa