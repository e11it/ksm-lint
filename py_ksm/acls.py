from csv import DictReader

from pydantic import ValidationError
from pydantic_common_models.ksm.csv_acl import KSM_CSV_HEADERS, KafkaACLCSV
import textwrap


class LintError(Exception):
    def __init__(self, message, error, detail=None):
        # Call the base class constructor with the parameters it needs
        super().__init__(message)
        self.error = error
        self.detail = detail


class KsmAcls:
    def __init__(self, file=None):
        self._acls = list()

        if file is not None:
            self.load(file)

    def load(self, file: str, lint_only=False):
        with open(file, 'r') as in_stream:
            csv_reader = DictReader(in_stream)
            if csv_reader.fieldnames != KSM_CSV_HEADERS:
                raise LintError(f"CSV Headers doesnt match expected",
                                textwrap.fill(textwrap.dedent(f"""
                                    Expected headers: {KSM_CSV_HEADERS}
                                    Actual headers: {csv_reader.fieldnames}
                """)))


            for idx, line in enumerate(csv_reader):
                try:
                    line = KafkaACLCSV.from_orm(line)
                    if not lint_only:
                        self._acls.append(line)
                except ValidationError as e:
                    raise LintError(f"Error validate model",
                                    f"Line {idx + 2}\n{line}",
                                    e.json())

    @property
    def acls(self) -> list[KafkaACLCSV]:
        return self._acls
