# wichteln

> v2026.1

## Usage

After publication, the package can be run directly with `uvx`:

```shell
uvx wichteln draw working_dir/schaerer.yaml --print-draw
```

For local development, run the project entry point with `uv run`:

```shell
uv run wichteln --version
uv run wichteln draw working_dir/schaerer.yaml --no-email --save-draw
```

`uvx wichteln` downloads a published package version from the configured package index. Display the available options with `wichteln draw --help`. Check the version with `wichteln --version` or `wichteln -v`.

## `draw` command

The command creates a valid Secret Santa assignment without self-assignments and respects the specified constraints.

- `--no-email`: Do not send emails.
- `--print-draw`: Print the assignment to stdout as `giver: receiver`.
- `--save-draw`: Save a YAML file next to the configuration file, for example `schaerer_draw_20260909_120000.yaml`.
- `--save-individual-draw`: Create a `draw_20260909_120000` folder next to the configuration file and write a `{giver}.txt` file for each giver containing only the receiver's name.

Without `--no-email`, emails are sent for all assignments if every participant has an email address. If an address is missing, a warning is displayed and the individual draw is saved automatically.

## Configuration file

The YAML file uses the following keys:

- `participants`: A list containing at least two participant objects.
- `name`: Unique name of a participant.
- `email`: Optional email address of the participant.
- `constraints`: A list of constraints.
- `giver`: Name of the participant to whom a constraint applies.
- `forbidden`: List of receivers that this giver cannot draw.
- `email_config`: Mapping containing the email configuration; `{}` is valid when no additional settings are needed.

Example:

```yaml
participants:
  - name: Yanis
    email: y.schaerer@proton.me
  - name: Hanna
    email: hanna.weber2000@bluewin.ch

constraints: []

email_config: {}
```

Files saved with `--save-draw` contain a flat mapping from giver to receiver:

```yaml
Yanis: Hanna
Hanna: Yanis
```