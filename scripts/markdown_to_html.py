import os
import shutil
import re
import arrow
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
    archive_name = "{}-index.html".format(arrow.utcnow().timestamp())
    shutil.move("index.html", ".archive/{}".format(archive_name))
    click.echo("Moved old version into {}".format(archive_name))


def set_working_directory():
    click.echo("Current working directory: {}".format(os.getcwd()))


def create_index(file_path):
    with open(file_path, "r+") as markdown_file:
        raw_html = markdown.markdown(markdown_file.read())
        transformed_html = transform_tags_into_labels(raw_html)
        final_html = "{}{}{}".format(OPENING_TAGS, transformed_html, CLOSING_TAGS)

    with open("index.html", "w+") as html_file:
        html_file.write(final_html)
    click.echo("Index created!")


def transform_tags_into_labels(raw_html) -> str:
    """
    Transform all occurences of `<p>$tagWord1 $tag word 2 </p>`
    into `<p><label>tagWord1</label><label>tag word 2</label></p>`
    :param raw_html: HTML body with raw tag words
    :return: HTML body with properly formatted tags
    """

    def remove_p_tags(text) -> str:
        return re.sub(re.compile("<.*?>"), "", text)

    for tags in re.findall(r"<p>\$[\$a-zA-Z\-()\/#' ]+<\/p>", raw_html):
        remove_p_tags(tags).split("$")
        paragraph = "<p>"
        for word in remove_p_tags(tags).split("$"):
            if word == "":
                continue
            paragraph = "{}<label>{}</label>".format(paragraph, word.rstrip())

        raw_html = raw_html.replace(tags, "{}</p>".format(paragraph))
    return raw_html


@click.command()
@click.option(
    "-f",
    "--file_path",
    type=str,
    default="Cyberculture and Social Justice Directory.md",
)
def main(file_path):
    set_working_directory()
    archive_index()
    create_index(file_path)


if __name__ == "__main__":
    main()
