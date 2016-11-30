# coding: utf-8
'''Command line interface for cfdilib
'''

import json

import click

from . import cfdv32


class Config(object):

    def __init__(self):
        self.verbose = False

PASS_CONFIG = click.make_pass_decorator(Config, ensure=True)


@click.group()
@click.option('--verbose', is_flag=True,
              help='Pass the result to the standard out')
@click.option('--out_file', type=click.File('wb'),
              default='document.xml')
@click.option('--in_file', type=click.File('rb'),
              default="document.json")
@PASS_CONFIG
def cli(config, in_file, out_file, verbose):
    """Main Interface to generate xml documents
    from custom dictionaries using legal xsd files
    complying with legal documents in all countires
    around the world.
    """
    config.out_file = out_file
    config.verbose = verbose
    config.in_file = in_file
    config.out_file = out_file


@cli.command()
@PASS_CONFIG
def cfdv32mx(config):
    """Format cfdi v3.2 for Mexico.

    \b
    File where the files will be written document.xml.
        cfdicli --in_file /path/to/yout/json/documnt.json cfdv32mx

    \b
    File where the files will be written from document.json.
        cfdicli --out_file ./document.xml cfdv32mx
    """
    dict_input = dict(json.load(config.in_file))
    invoice = cfdv32.get_invoice(dict_input)
    if invoice.valid:
        config.out_file.write(invoice.document)
        config.out_file.flush()
        click.echo('Document %s has been created.' % config.out_file.name)
    else:
        click.echo(invoice.ups.message)
