import pytest

@pytest.fixture
def invalid_str_id_numbers():
    return [
        "",
        "123456789",
        "342343243243244324",
        "3432dfdsf",
    ]

@pytest.fixture
def invalid_date_id_numbers():
    return ["7113245929185", "7405325437186", "7702295556082"]


@pytest.fixture
def male_id_numbers():
    return [
        "0303068942075",
        "1701077451070",
        "5202049057182",
        "5906045026187",
        "8703209120170",
    ]


@pytest.fixture
def female_id_numbers():
    return [
        "2904251790177",
        "1910252128177",
        "8711094861170",
        "5207272628088",
        "2802294751075",
    ]


@pytest.fixture
def invalid_checksum_id_numbers():
    return ["7106245929181", "7405095437182", "7710165556083"]
