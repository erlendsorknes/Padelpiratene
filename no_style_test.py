from html.parser import HTMLParser


class NoStyleException(Exception):
    pass


class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):

        a = {attr[0]: attr[1] for attr in attrs}

        if a.get("rel", "") == "stylesheet":
            raise NoStyleException("No stylesheets allowed")

        if a.get("href", "").endswith(".css"):
            raise NoStyleException("No css links allowed")

        if "style" in a:
            raise NoStyleException(
                f"No styles allowed, style found in <{tag}> tag: {a}"
            )


import subprocess

result = subprocess.run(
    "git ls-files '*.html' | grep .", shell=True, capture_output=True, text=True
)
file_list = result.stdout.splitlines()

for file in file_list:
    with open(file) as f:
        parser = MyHTMLParser()
        parser.feed(f.read())
