import argparse
import logging
import textwrap
from csv import DictReader
from typing import Iterable
from pydantic import ValidationError
from pydantic_common_models.ksm.csv_acl import KSM_CSV_HEADERS, KafkaACLCSV


logging.basicConfig(format='%(name)s:%(levelname)s:%(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class LintError(Exception):
    def __init__(self, message, error, detail=None):
        # Call the base class constructor with the parameters it needs
        super().__init__(message)
        self.error = error
        self.detail = detail


def lint(file_stream: Iterable[str]):
    csv_reader = DictReader(file_stream)
    if csv_reader.fieldnames != KSM_CSV_HEADERS:
        raise LintError(f"CSV Headers doesnt match expected",
                        textwrap.fill(textwrap.dedent(f"""
                        Expected headers: {KSM_CSV_HEADERS}
                        Actual headers: {csv_reader.fieldnames}
        """)))

    result = list()
    for idx, line in enumerate(csv_reader):
        try:
            result.append(KafkaACLCSV.from_orm(line))
        except ValidationError as e:
            raise LintError(f"Error validate model",
                            f"Line {idx+2}\n{line}",
                            e.json())


def lint_cli() -> ():
    parser = argparse.ArgumentParser(
        prog='lint_cli',
        description='Lint csv file with Kafka ACL for KSM')
    parser.add_argument('filename',
                        type=argparse.FileType('r', encoding='UTF-8'))
    args = parser.parse_args()

    try:
        lint(args.filename)
    except LintError as e:
        logger.error(f"{e}")
        logger.error(e.error)
        if e.detail is not None:
            logger.error(f"Error details:\n{e.detail}")
        return 1


if __name__ == '__main__':
    lint_cli()