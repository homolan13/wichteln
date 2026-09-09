from datetime import datetime
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

import typer

from wichteln.models import Config
from wichteln.services import draw as draw_assignments
from wichteln.services import load_yaml, save_yaml, send_email

app = typer.Typer(add_completion=False, invoke_without_command=True)


def _version() -> str:
	try:
		return version('wichteln')
	except PackageNotFoundError:
		return '2026.1'


def _save_individual_draw(config_path: Path, assignments: dict[str, str], timestamp: str) -> Path:
	draw_directory = config_path.parent / f'draw_{timestamp}'
	draw_directory.mkdir(exist_ok=False)
	for giver, receiver in assignments.items():
		(draw_directory / f'{giver}.txt').write_text(receiver, encoding='utf-8')
	return draw_directory


@app.callback()
def _main_callback(
	version_flag: bool = typer.Option(False, '--version', '-v', help='Print the version and exit.'),
) -> None:
	if version_flag:
		typer.echo(_version())
		raise typer.Exit()


def main() -> None:
	app()


@app.command()
def draw(
	config_path: Path = typer.Argument(..., exists=True, dir_okay=False, readable=True),
	no_email: bool = typer.Option(False, '--no-email', help='Do not send emails.'),
	print_draw: bool = typer.Option(False, '--print-draw', help='Print the draw to stdout.'),
	save_draw: bool = typer.Option(False, '--save-draw', help='Save the draw as a YAML file.'),
	save_individual_draw: bool = typer.Option(
		False,
		'--save-individual-draw',
		help='Save one receiver name per giver in a timestamped folder.',
	),
) -> None:
	try:
		config: Config = load_yaml(str(config_path))
		participants = [participant.name for participant in config.participants]
		constraints = {
			constraint.giver: constraint.forbidden
			for constraint in config.constraints
		}
		assignments = draw_assignments(participants, constraints)
		timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

		if print_draw:
			for giver in participants:
				typer.echo(f'{giver}: {assignments[giver]}')

		if save_draw:
			draw_path = config_path.with_name(
				f'{config_path.stem}_draw_{timestamp}{config_path.suffix}'
			)
			save_yaml(str(draw_path), assignments)
			typer.echo(f'Saved draw to {draw_path}')

		needs_individual_draw = save_individual_draw
		if not no_email:
			if all(participant.email for participant in config.participants):
				email_config = config.email_config.model_dump()
				for giver, receiver in assignments.items():
					send_email(giver, receiver, email_config)
			else:
				typer.echo(
					'Warning: not all participants have an email address; '
					'saving the individual draw instead.',
					err=True,
				)
				needs_individual_draw = True

		if needs_individual_draw:
			draw_directory = _save_individual_draw(config_path, assignments, timestamp)
			typer.echo(f'Saved individual draw to {draw_directory}')
	except Exception as error:
		typer.echo(f'Error: {error}', err=True)
		raise typer.Exit(code=1) from error

