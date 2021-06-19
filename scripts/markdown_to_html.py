import markdown


def main():
    with open(
        "/Users/pfaniel/Projects/private/Cyberculture-and-Social-Justice-Directory/Directory.md",
        "r+",
    ) as f:
        print(markdown.markdown(f.read()))


main()
