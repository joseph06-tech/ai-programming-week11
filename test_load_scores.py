import pytest

from load_scores import load_scores


def test_valid_rows_are_kept_and_duplicate_names_are_preserved(tmp_path):
    csv_file = tmp_path / "scores.csv"
    csv_file.write_text(
        'name,score\n김하나,88\n  이두리  , 75 \n김하나,91\n"최,네번",77\n',
        encoding="utf-8",
    )

    kept, skipped = load_scores(csv_file)

    assert kept == [
        ("김하나", 88),
        ("이두리", 75),
        ("김하나", 91),
        ("최,네번", 77),
    ]
    assert skipped == []


def test_header_only_file_returns_empty_lists(tmp_path):
    csv_file = tmp_path / "scores.csv"
    csv_file.write_text("name,score\n", encoding="utf-8")

    assert load_scores(csv_file) == ([], [])


def test_utf8_bom_and_quoted_comma_in_name_are_parsed(tmp_path):
    csv_file = tmp_path / "scores.csv"
    csv_file.write_text('name,score\n"최,네번",77\n', encoding="utf-8-sig")

    kept, skipped = load_scores(csv_file)

    assert kept == [("최,네번", 77)]
    assert skipped == []


def test_missing_file_raises_file_not_found_error(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_scores(tmp_path / "missing.csv")


@pytest.mark.parametrize(
    ("row", "reason"),
    [
        ("박세찬", "열 개수가 2가 아님"),
        ("장미르,72,비고", "열 개수가 2가 아님"),
        (",90", "이름이 비어 있음"),
        ("   ,90", "이름이 비어 있음"),
        ("서한별,", "점수가 비어 있음"),
        ("서한별,   ", "점수가 비어 있음"),
        ("한겨울,결석", "점수가 정수가 아님"),
    ],
)
def test_invalid_rows_are_recorded_with_line_number_and_reason(
    tmp_path, row, reason
):
    csv_file = tmp_path / "scores.csv"
    csv_file.write_text(f"name,score\n{row}\n", encoding="utf-8")

    kept, skipped = load_scores(csv_file)

    assert kept == []
    assert skipped == [(2, row, reason)]


@pytest.mark.parametrize(
    ("score", "is_valid"),
    [
        (-1, False),
        (0, True),
        (1, True),
        (99, True),
        (100, True),
        (101, False),
    ],
)
def test_score_boundaries(tmp_path, score, is_valid):
    csv_file = tmp_path / "scores.csv"
    csv_file.write_text(f"name,score\n학생,{score}\n", encoding="utf-8")

    kept, skipped = load_scores(csv_file)

    if is_valid:
        assert kept == [("학생", score)]
        assert skipped == []
    else:
        assert kept == []
        assert skipped == [(2, f"학생,{score}", "점수가 0~100 밖")]


def test_blank_lines_are_ignored_but_line_numbers_are_preserved(tmp_path):
    csv_file = tmp_path / "scores.csv"
    csv_file.write_text("name,score\n학생,80\n\n,90\n", encoding="utf-8")

    kept, skipped = load_scores(csv_file)

    assert kept == [("학생", 80)]
    assert skipped == [(4, ",90", "이름이 비어 있음")]
