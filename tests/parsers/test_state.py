import pytest

from ciprs_reader.const import Section
from ciprs_reader.parser import lines


@pytest.mark.parametrize(
    "Parser",
    [
        lines.CaseStatus,
        lines.OffenseDate,
        lines.OffenseDateTime,
        lines.CaseWasServedOnDate,
        lines.OffenseRecordRowWithNumber,
        lines.OffenseRecordRow,
    ],
)
def test_parser__disabled_by_default(Parser, report, state):
    parser = Parser(report, state)
    assert not parser.is_enabled()


def test_case_details__disabled(report, state):
    state.section = "Not Header"
    parser = lines.CaseDetails(report, state)
    assert not parser.is_enabled()


@pytest.mark.parametrize(
    "Parser",
    [
        lines.CaseStatus,
        lines.OffenseDate,
        lines.OffenseDateTime,
        lines.CaseWasServedOnDate,
    ],
)
def test_case_information_parsers__enabled(Parser, report, state):
    state.section = Section.CASE_INFORMATION
    assert Parser(report, state).is_enabled()


@pytest.mark.parametrize(
    "section", [Section.DISTRICT_OFFENSE, Section.SUPERIOR_OFFENSE],
)
def test_offense_record_row_with_number__enabled(section, report, state):
    state.section = section
    assert lines.OffenseRecordRowWithNumber(report, state).is_enabled()


def test_offense_record_row__enabled(report, state):
    state.offense_num = 1
    state.section = Section.DISTRICT_OFFENSE
    assert lines.OffenseRecordRow(report, state).is_enabled()
