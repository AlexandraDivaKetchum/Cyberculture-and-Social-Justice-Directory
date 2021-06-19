import os
import shutil

import arrow
import click
import markdown


def archive_index():
    if not os.path.exists("index.html"):
        click.echo("No existing `index.html` to move")
        return
    archive_name = "{}-index.html".format(arrow.utcnow().timestamp())
    shutil.move("index.html", ".archive/{}".format(archive_name))
    click.echo("Moved old version into {}".format(archive_name))


def set_working_directory():
    os.chdir("..")  # Depends on working directory, might need to move
    click.echo("Current working directory: {}".format(os.getcwd()))


def create_index(file_path):
    with open(file_path, "r+") as markdown_file:
        html = markdown.markdown(markdown_file.read())
        html = "{}\n".format(html)

    with open("index.html", "w+") as html_file:
        html_file.write(html)
    click.echo("Index created!")


@click.command()
@click.option("-f", "--file_path", type=str, default="AboutPage.md")
def main(file_path):
    set_working_directory()
    archive_index()
    create_index(file_path)


if __name__ == "__main__":
    main()
