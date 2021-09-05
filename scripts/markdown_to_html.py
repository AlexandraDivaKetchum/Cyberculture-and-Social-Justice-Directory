import os
import shutil
import re
from time import time
import click
import markdown


OPENING_TAGS = """
<!doctype html>

<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">

  <title>Cyberculture and Social Justice Directory</title>
  <!--<meta name="description" content="A simple HTML5 Template for new projects.">-->
  <!--<meta name="author" content="SitePoint">-->

  <!--<meta property="og:title" content="A Basic HTML5 Template">-->
  <!--<meta property="og:type" content="website">-->
  <!--<meta property="og:url" content="https://www.sitepoint.com/a-basic-html5-template/">-->
  <!--<meta property="og:description" content="A simple HTML5 Template for new projects.">-->
  <!--<meta property="og:image" content="image.png">-->

  <!--<link rel="icon" href="/favicon.ico">-->
  <!--<link rel="icon" href="/favicon.svg" type="image/svg+xml">-->
  <!--<link rel="apple-touch-icon" href="/apple-touch-icon.png">-->

  <link rel="stylesheet" href="css/styles.css?v=1.0">

</head>

<body>
"""


CLOSING_TAGS = """
</body>
</html>
"""


def archive_index():
    if not os.path.exists("index.html"):
        click.echo("No existing `index.html` to move")
        return
    archive_name = "{}-index.html".format(time())
    shutil.move("index.html", ".archive/{}".format(archive_name))
    click.echo("Moved old version into {}".format(archive_name))


def create_index(file_path):
    with open(file_path, "r+") as markdown_file:
        raw_html = markdown.markdown(markdown_file.read())
        transformed_html = transform_html(raw_html)
        final_html = "{}{}{}".format(OPENING_TAGS, transformed_html, CLOSING_TAGS)

    with open("index.html", "w+") as html_file:
        html_file.write(final_html)
    click.echo("Index created!")


def transform_html(raw_html) -> str:
    html = transform_tags_into_labels(raw_html)
    html = make_links_open_in_new_tabs(html)
    return split_articles_into_divs(html)


def make_links_open_in_new_tabs(html):
    return html.replace("<a href=", '<a target="_blank" href=')


def split_articles_into_divs(raw_html) -> str:
    html = ""
    # Split without losing separator
    for raw_article in [
        "<h1>{}".format(element) for element in raw_html.split("<h1>") if element
    ]:
        article = format_article(raw_article)
        html = '{}<div class="article">\n{}</div>\n'.format(html, article)
    return html


def format_article(raw_article) -> str:
    return raw_article.replace("<h1>", '<div class="heading">\n<h1>').replace(
        "</h3>", '</h3>\n</div>\n<div class="content">'
    )


def transform_tags_into_labels(raw_html) -> str:
    """
    Transform all occurrences of `<p>$tagWord1 $tag word 2 </p>`
    into `<p><label>tagWord1</label><label>tag word 2</label></p>`
    :param raw_html: HTML body with raw tag words
    :return: HTML body with properly formatted tags
    """

    def remove_p_tags(text) -> str:
        return re.sub(re.compile("<.*?>"), "", text)

    for tags in re.findall(r"<p>\$[\$a-zA-Z\-()\/#' ]+<\/p>", raw_html):
        remove_p_tags(tags).split("$")
        paragraph = '<p class="tags">'
        for word in remove_p_tags(tags).split("$"):
            if word != "":
                paragraph = "{}<label>{}</label>".format(paragraph, word.rstrip())

        raw_html = raw_html.replace(tags, "{}</p>\n</div>".format(paragraph))
    return raw_html


@click.command()
@click.option(
    "-f",
    "--file_path",
    type=str,
    default="Cyberculture and Social Justice Directory.md",
)
def main(file_path):
    archive_index()
    create_index(file_path)


if __name__ == "__main__":
    main()
