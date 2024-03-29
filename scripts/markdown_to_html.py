import logging
from jinja2 import Environment, BaseLoader
import markdown
import re


INDEX_PAGE_INFO = {
    "markdown_file_name": "Cyberculture and Social Justice Directory.md",
    "file_name": "index.html",
    "transform": True,
}


ABOUT_PAGE_INFO = {
    "markdown_file_name": "AboutPage.md",
    "file_name": "about.html",
    "transform": False,
}
PAGES = [INDEX_PAGE_INFO, ABOUT_PAGE_INFO]


def _transform_html(raw_html) -> str:
    html, tag_list = _transform_tags_into_labels(raw_html)
    html = _make_links_open_in_new_tabs(html)
    return _split_articles_into_divs(html), tag_list


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
    :return: 
        - HTML body with properly formatted tags
        - List of all the tags in the body
    """
    all_tags = []

    def remove_p_tags(text) -> str:
        return re.sub(re.compile("<.*?>"), "", text)

    def all_tags_to_string(tags) -> str:
        unique_tags = sorted(list(set(tags)))
        return ",".join(unique_tags)

    for tags in re.findall(r"<p>\$[\$a-zA-Z\-()\/#' ]+<\/p>", raw_html):
        remove_p_tags(tags).split("$")
        paragraph = '<p class="tags">'
        for word in remove_p_tags(tags).split("$"):
            if word != "":
                word = word.rstrip().title()
                all_tags.append(word)
                paragraph = "{}<label>{}</label>".format(paragraph, word)

        raw_html = raw_html.replace(tags, "{}</p>\n</div>".format(paragraph))
    
    return raw_html, all_tags_to_string(all_tags)


def create_html_from_markdown(page_info, jinja_env):
    """
    Use python markdown library to create html files from markdown files
    :param page_info: dict of information about the markdown file to transform
    :param jinja_env: Jinja environment object
    """
    with open("templates/{}".format(page_info["file_name"])) as html_template:
        template_str = html_template.read()
        jinja_template = jinja_env.from_string(template_str)

    with open(page_info["markdown_file_name"], "r+") as markdown_file:
        html = markdown.markdown(markdown_file.read())
        render_data = {}
        
        if page_info["transform"]:
            html, tag_list = _transform_html(html)
            render_data["keyword_list"] = tag_list

        render_data["main_content"] = html

        html = jinja_template.render(**render_data)

    with open(page_info["file_name"], "w+") as html_file:
        html_file.write(html)

    logging.info("`{}` created!".format(page_info["file_name"]))


def main():
    logging.basicConfig(level=logging.INFO)
    jinja_env = Environment(loader=BaseLoader())
    create_html_from_markdown(INDEX_PAGE_INFO, jinja_env)
    create_html_from_markdown(ABOUT_PAGE_INFO, jinja_env)


if __name__ == "__main__":
    main()
