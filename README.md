# WhatsApp Message Analyzer

A Python tool for analyzing and visualizing WhatsApp chat exports, featuring interactive data processing and animated bar chart race generation.

**Read this in Portuguese | Leia em português:** [Português](README.pt.md)

## Installation

### Prerequisites

- Python 3.10 or higher
- Required dependencies (install via pip or uv):

```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

Run the analyzer with interactive prompts:

```bash
python main.py
```

### Command Line Options

```bash
python main.py [OPTIONS]
```

#### Options

| Option | Short | Description | Example |
|--------|-------|-------------|---------|
| `--name` | `-n` | Project name for output files | `-n "Family Chat"` |
| `--data` | `-d` | Path to WhatsApp export file | `-d "chat.txt"` |
| `--config` | `-c` | Path to YAML configuration file | `-c "config.yaml"` |
| `--map` | `-m` | Path to name mapping YAML file | `-m "names.yaml"` |
| `--start-date` | `-sd` | Start date for analysis (YYYY-MM-DD) | `-sd 2023-01-01` |
| `--period` | `-p` | Time period filter | `-p 6m`, `-p 1y`, `-p 30d` |
| `--video` | `-v` | Generate bar chart race video | `-v` |
| `--anon` | | Anonymize names in output | `--anon` |
| `--verbose` | | Enable verbose logging | `--verbose` |
| `--help` | `-h` | Show help message | `-h` |

### Examples

#### Analyze last 6 months with video generation:
```bash
python main.py -n "my_chat" -d "WhatsApp Chat.txt"
```

## Configuration

### Default Configuration File

The tool expects a default configuration file at `configs/default_config.yaml`. This file should contain settings for:

- Chart styling and colors
- Output formats and paths
- Data processing parameters
- Visualization settings

### Name Mapping File

Create a YAML file to map phone numbers to readable names:

```yaml
replace_dict:
  "+1234567890": "John Doe"
  "+0987654321": "Jane Smith"
  "Unknown Contact": "Mystery Person"
```

## Time Period Format

The `--period` option accepts the following formats:

- `Xd` - X days (e.g., `30d` for 30 days)
- `Xm` - X months (e.g., `6m` for 6 months)
- `Xy` - X years (e.g., `1y` for 1 year)

## Project Structure

```
whatsapp-analyzer/
├── main.py                 # Main CLI application
├── read_data.py            # Data reading functionality
├── etl.py                  # Data transformation pipeline
├── dataviz.py              # Visualization generation
├── utils.py                # Utility functions
├── configs/                # Configuration files
│   └── default_config.yaml # General configuration
│   └── map_contacts.yaml   # Name Mapping File
└── README.md
```

## Output

The tool generates:

1. **Processed Data**: Cleaned and transformed message data
2. **Statistics**: Message counts, activity patterns, participant analysis
3. **Bar Chart Race Video**: Animated visualization showing message activity over time (optional)

## WhatsApp Export Format

To export your WhatsApp chat:

1. *In your phone:* Open the chat in WhatsApp
2. Tap the contact/group name at the top
3. Scroll down and tap "Export Chat"
4. Choose "Without Media" for faster processing
5. Save the `.txt` file and use it with this tool

![Export charts](imgs/export_chat.png)

## Privacy and Security

- The tool processes data locally on your machine
- No data is transmitted to external services
- Use the `--anon` flag to anonymize participant names if you need to share
- Name mapping files can help maintain privacy while keeping analysis meaningful

## Troubleshooting

### Common Issues

** Unable to export chat history: if the whatsapp group has enable 'Advanced chat privacy' option. You won't be able to export the chat history.
**"Missing the key: 'replace_dict'"**: Your mapping file should contain a top-level `replace_dict` key.


## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request


## Support

For issues and questions, please [create an issue](link-to-issues) in the repository.

## Aknowledgements
- Using the bar chart race from [dexplo/bar_chart_race](https://github.com/dexplo/bar_chart_race)
