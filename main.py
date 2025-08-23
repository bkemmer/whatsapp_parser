#!/usr/bin/env python3

import click
from read_data import read_data
from etl import transform
from dataviz import generate_bar_chart_race

from utils import read_yaml_file

@click.command()
@click.option(
    '-n', '--name',
    required=True,
    help='Name of the files to process',
)
@click.option(
    '-d', '--data',
    type=click.Path(exists=True, readable=True),
    required=True,
    help='Filename with whatsapp export data'
)
@click.option(
    '-c', '--config',
    type=click.Path(exists=True, readable=True),
    required=False,
    default='configs/default_config.yaml',
    help='Path to YAML file with configurations',
)
@click.option(
    '-m', '--map',
    type=click.Path(exists=True, readable=True),
    required=False,
    help='Path to YAML file with mapping of unknown numbers to new names'
)
@click.help_option('-h', '--help')
def main(name: str, data: str, config: str, map: str) -> None:
    """
    Whatsapp parser

    This tool processes the messages exported from whatsapp
    """
    click.echo(f"🔧 Project name: '{name}'")
    click.echo(f"📋 Using data file: {data}")
    click.echo(f"📋 Using config file: {config}")
    click.echo(f"🗺️  Using map file: {map}")
    click.echo()

    configs_dict = read_yaml_file(config)

    df = read_data(project_name=name, data_path=data, configs_dict=configs_dict)
    transform(df, map, configs_dict)

    generate_bar_chart_race(configs_dict, project_name=name)



if __name__ == '__main__':
    main()
