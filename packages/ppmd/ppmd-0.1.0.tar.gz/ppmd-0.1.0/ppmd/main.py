'''ppmd: converts from pptx to md'''
from models import presentation
import os

import click


@click.command()
@click.argument('pres')
@click.option('--slidesep', default='-----', help='Separator string between slides in generated md.')
@click.option('--headingsfirst/--noheadings', default=True, help='--headingsfirst: assume headings start each slide. --noheadings: make no such assumption.')
@click.option('--includenotes/--excludenotes', default=True, help='Include notes slides in md output?')
@click.option('--notesprefix', default=">>>", help='Sets character used to prefix notes lines')
def run_convert(pres, slidesep, headingsfirst, includenotes, notesprefix):
    '''Manages the conversion process'''
    settings = presentation.Pres_settings(
        slidesep, headingsfirst, pres, includenotes, notesprefix)
    pres = presentation.Presentation(settings)
    pres.fetch()
    pres.write_output()
    return

if __name__ == "__main__":
    run_convert()
