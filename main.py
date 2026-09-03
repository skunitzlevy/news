import requests
from bs4 import BeautifulSoup


def main():
    url = "https://www.nytimes.com/"

    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    for heading in soup.find_all(["h2", "h3"]):
        text = heading.get_text(" ", strip=True)

        if text:
            print(text)


if __name__ == "__main__":
    main()
