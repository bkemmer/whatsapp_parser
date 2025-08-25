#!/usr/bin/env python3

import click
from read_data import read_data
from etl import transform
from dataviz import generate_bar_chart_race
import logging
from utils import read_yaml_file, get_logger

import re
from datetime import timedelta, datetime
from dateutil.relativedelta import relativedelta

logger = get_logger(logger_name="main", log_level=logging.INFO, console=True)


class Duration(click.ParamType):
    name = "duration"

    def convert(self, value, param, ctx):
        if isinstance(value, relativedelta):
            return value

        match = re.match(r"^(\d+)([ymd])$", value.lower())
        if not match:
            self.fail(f"{value!r} must be like: 6m, 1y, 30d", param, ctx)

        amount, unit = int(match.group(1)), match.group(2)

        units = {
            "y": lambda n: relativedelta(years=n),
            "m": lambda n: relativedelta(months=n),
            "d": lambda n: relativedelta(days=n),
        }

        return units[unit](amount)


def check_name_option(name: str | None):
    if name:
        click.echo(f"🔧 Project name: '{name}'")
    else:
        name = click.prompt("Project name")
        name = name.strip().replace(" ", "_")
        click.echo(f"🔧 Project name: '{name}'")
        click.echo()
    return name


def check_data_option(data: str | None):
    if data:
        click.echo(f"📋 Using data file: {data}")
    else:
        data = click.prompt(
            "Enter input file path",
            type=click.Path(exists=True, file_okay=True, readable=True),
        )
        click.echo(f"📋 Using data file: {data}")
        click.echo()
    return data


def check_config_option(config: str | None):
    configs_dict = None
    if config:
        click.echo(f"📋 Using config file: {config}")
    else:
        config = click.prompt(
            "Enter path to YAML file with configurations",
            default="configs/default_config.yaml",
            show_default=True,
            type=click.Path(exists=True, file_okay=True, readable=True),
        )
        click.echo(f"📋 Using config file: {config}")
        click.echo()
    try:
        configs_dict = read_yaml_file(config)
    except Exception as e:
        click.echo(f"Error reading config file: {e}")

    return config, configs_dict


def check_map_option(map: str | None):
    replace_dict = None

    def read_map_file(map_file: str):
        try:
            return read_yaml_file(map_file)["replace_dict"]
        except KeyError:
            click.echo(f"Missing the key: 'replace_dict' on file: {map_file}")
        except Exception as e:
            click.echo(f"Error reading map file: {e}")
        return None

    if not map:
        if click.confirm("Do you want to provide a mapping file?", default=False):
            map = click.prompt(
                "Enter path to YAML file",
                type=click.Path(exists=True, file_okay=True, readable=True),
            )
    if map:
        replace_dict = read_map_file(map)
        click.echo(f"🗺️  Using map file: {map}")
        click.echo()

    return map, replace_dict


def check_period_option(period):
    if not period:
        if click.confirm(
            "Do you want to specify a time limit for the messages?", default=False
        ):
            period = click.prompt(
                'Messages since the last ("3m", "1y", "30d"):',
                type=Duration(),
            )
    return period


def check_video_option(video: bool):
    if video:
        click.echo("Video of bar chart race will be generated.")
    else:
        video = click.confirm(
            "Do you want to generate bar chart race video?", default=True
        )
    return video


@click.command()
@click.option(
    "-n",
    "--name",
    required=False,
    help="Name of the files to process",
)
@click.option(
    "-d",
    "--data",
    type=click.Path(exists=True, readable=True),
    required=False,
    help="Filename with whatsapp export data",
)
@click.option(
    "-c",
    "--config",
    type=click.Path(exists=True, readable=True),
    required=False,
    help="Path to YAML file with configurations",
)
@click.option(
    "-m",
    "--map",
    type=click.Path(exists=True, readable=True),
    required=False,
    help="Path to YAML file with mapping of unknown numbers to new names",
)
@click.option(
    "-sd",
    "--start-date",
    type=click.DateTime(["%Y-%m-%d"]),
    required=False,
    help="Specify a start date in the format %Y-%m-%d",
)
@click.option(
    "-p",
    "--period",
    type=Duration(),
    required=False,
    help="Time period: 6m, 1y, 30d",
)
@click.option(
    "-v",
    "--video",
    is_flag=True,
    required=False,
    help="Generate the video of bar chart race",
)
@click.option(
    "--anon",
    is_flag=True,
    required=False,
    help="Anonymize the names in the data",
)
@click.option("--verbose", is_flag=True)
@click.help_option("-h", "--help")
def main(
    name: str | None,
    data: str | None,
    config: str | None,
    map: str | None,
    start_date: datetime | None,
    period: timedelta | None,
    video: bool,
    anon: bool,
    verbose: bool,
) -> None:
    """
    Whatsapp parser

    This tool processes the messages exported from whatsapp
    """
    project_name = check_name_option(name)
    data_path = check_data_option(data)
    config, configs_dict = check_config_option(config)
    map, replace_dict = check_map_option(map)
    period = check_period_option(period)
    video = check_video_option(video)

    click.echo()

    logger.info("Reading data...")
    df = read_data(project_name, data_path, configs_dict, verbose)

    logger.info("Transforming data...")
    df_transformed = transform(
        df, project_name, replace_dict, configs_dict, start_date, period, anon, verbose
    )

    if video:
        logger.info("Generating bar chart race video...")
        generate_bar_chart_race(df_transformed, configs_dict, project_name, verbose)


if __name__ == "__main__":
    main()
