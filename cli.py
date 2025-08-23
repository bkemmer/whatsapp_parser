import click

@click.command()
@click.option(
    '-n', '--name',
    required=True,
    help='Name of the files to process',
)
@click.option(
    '-d', '--data',
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
    required=True,
    help='Path to YAML file with mapping of unknown numbers to new names'
)
@click.help_option('-h', '--help')
def main(name: str, data: str, config: str, map: str) -> None:
    """
    Whatsapp parser

    This tool processes the messages exported from whatsapp
    """
    click.echo(f"🔧 Processing files with name pattern: '{name}'")
    click.echo(f"📋 Using data file: {data}")
    click.echo(f"📋 Using config file: {config}")
    click.echo(f"🗺️  Using map file: {map}")
    click.echo()

if __name__ == '__main__':
    main()
