import logging
import os
import re
import shutil
from time import time

import markdown


INDEX_PAGE_INFO = {
    "markdown_file_name": "Cyberculture and Social Justice Directory.md",
    "html_file_name": "index.html",
    "opening_tags_path": "templates/index_opening_tags.txt",
    "closing_tags_path": "templates/index_closing_tags.txt",
    "transform": True,
}


ABOUT_PAGE_INFO = {
    "markdown_file_name": "AboutPage.md",
    "html_file_name": "about.html",
    "opening_tags_path": "templates/about_opening_tags.txt",
    "closing_tags_path": "templates/about_closing_tags.txt",
    "transform": False,
}
PAGES = [INDEX_PAGE_INFO, ABOUT_PAGE_INFO]


def _transform_html(raw_html) -> str:
    html = _transform_tags_into_labels(raw_html)
    html = _make_links_open_in_new_tabs(html)
    return _split_articles_into_divs(html)


def _make_links_open_in_new_tabs(html):
    return html.replace("<a href=", '<a target="_blank" href=')


def _split_articles_into_divs(raw_html) -> str:
    html = ""
    # Split without losing separator
    for raw_article in [
        "<h1>{}".format(element) for element in raw_html.split("<h1>") if element
    ]:
        article = _format_article(raw_article)
        html = "{}<article>\n{}</article>\n".format(html, article)
    return html


def _format_article(raw_article) -> str:
    return raw_article.replace("<h1>", '<header class="heading">\n<h1>').replace(
        "</h3>", '</h3>\n</header>\n<div class="content">'
    )


def _transform_tags_into_labels(raw_html) -> str:
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


def create_html_from_markdown(page_info):
    with open(page_info["opening_tags_path"], "r+") as opening_tags_template:
        opening_tags = opening_tags_template.read()

    with open(page_info["closing_tags_path"], "r+") as closing_tags_template:
        closing_tags = closing_tags_template.read()

    with open(page_info["markdown_file_name"], "r+") as markdown_file:
        html = markdown.markdown(markdown_file.read())
        if page_info["transform"]:
            html = _transform_html(html)
        html = "{}{}{}".format(opening_tags, html, closing_tags)

    with open(page_info["html_file_name"], "w+") as html_file:
        html_file.write(html)
    logging.info("`{}` created!".format(page_info["html_file_name"]))


def main():
    logging.basicConfig(level=logging.INFO)
    create_html_from_markdown(INDEX_PAGE_INFO)
    create_html_from_markdown(ABOUT_PAGE_INFO)


if __name__ == "__main__":
    main()
