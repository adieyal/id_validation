from __future__ import annotations

import datetime as _dt
import re
from typing import Any

from ..registry import register
from ..validate import ValidationError
from .base import BaseValidator, ParsedID


_RC_RE = re.compile(r"^(\d{9,10})$")


def _decode_rc_date(mm_raw: int, *, year: int, dd: int) -> tuple[_dt.date, str | None, dict[str, Any]]:
    gender: str | None = None
    mm = mm_raw
    special_series = False

    if mm >= 70:
        mm -= 70
        gender = "F"
        special_series = True
    elif mm >= 50:
        mm -= 50
        gender = "F"
    elif mm >= 20:
        mm -= 20
        special_series = True

    try:
        dob = _dt.date(year, mm, dd)
    except ValueError as e:
        raise ValidationError("Invalid date of birth") from e

    extra: dict[str, Any] = {"month_raw": mm_raw}
    if special_series:
        extra["special_series"] = True
    return dob, gender, extra


def _infer_century(yy: int) -> int:
    today = _dt.date.today()
    pivot = today.year % 100
    return 2000 if yy <= pivot else 1900


def _checksum_ok_10digits(rc10: str) -> bool:
    base9 = int(rc10[:9])
    mod = base9 % 11
    check = mod
    if check == 10:
        check = 0
    return int(rc10[9]) == check


@register("SK")
class SlovakiaRodneCisloValidator(BaseValidator):
    """Slovakia rodné číslo (birth number).

    Very similar to Czech rodné číslo; normalization removes optional slash.

    Accepts 9-digit legacy numbers (no checksum) and 10-digit numbers with mod-11.
    """

    country_code = "SK"

    def normalize(self, id_number: str) -> str:
        return id_number.strip().replace(" ", "").replace("/", "")

    def parse(self, id_number: str) -> ParsedID:
        v = self.normalize(id_number)
        if not _RC_RE.match(v):
            raise ValidationError("Invalid rodné číslo format")

        yy = int(v[0:2])
        mm_raw = int(v[2:4])
        dd = int(v[4:6])

        if len(v) == 9:
            century = 1900
            year = century + yy
            dob, gender, extra = _decode_rc_date(mm_raw, year=year, dd=dd)
            extra.update({"century": century, "checksum": None})
            return ParsedID(country_code="SK", id_number=v, id_type="RODNE_CISLO", dob=dob, gender=gender, extra=extra)

        if len(v) != 10:
            raise ValidationError("Invalid rodné číslo length")

        if not _checksum_ok_10digits(v):
            raise ValidationError("Invalid checksum")

        century = _infer_century(yy)
        year = century + yy
        dob, gender, extra = _decode_rc_date(mm_raw, year=year, dd=dd)

        extra.update({"century": century, "extension": int(v[6:9]), "checksum": int(v[9])})
        return ParsedID(country_code="SK", id_number=v, id_type="RODNE_CISLO", dob=dob, gender=gender, extra=extra)
