import sys

import click
import os

from format_converter.serializers import Serializer


@click.command()
@click.option("--input", "-i", type=click.Path(), required=True, help="The input file.")
@click.option("--input-formatter", "-if", type=str, required=True, help="The input formatter.")
@click.option("--output", "-o", type=click.Path(), required=True, help="The output file.")
@click.option("--output-formatter", "-of", type=str, required=True, help="The output formatter.")
@click.option("--stdin", type=bool, is_flag=True, required=False, default=False, help="The input should be read in the standard input")
@click.option("--stdout", type=bool, is_flag=True, required=False, default=False, help="The output should be write in the standard output")
def convert(input: os.PathLike, input_formatter: str, output: os.PathLike, output_formatter: str, stdin: bool, stdout: bool) -> None:
    # TODO: add logger
    input_file = sys.stdin if stdin else open(input, "r")
    output_file = sys.stdout if stdout else open(output, "w+")
    input_data = input_file.read()
    input_serializer = Serializer.serializers[input_formatter]
    output_serializer = Serializer.serializers[output_formatter]
    serialized_input = input_serializer.deserialize(input_data)
    data = output_serializer.serialize(serialized_input)
    output_file.write(data)

    if input_file is not sys.stdin:
        input_file.close()

    if output_file is not sys.stdout:
        output_file.close()



convert()
