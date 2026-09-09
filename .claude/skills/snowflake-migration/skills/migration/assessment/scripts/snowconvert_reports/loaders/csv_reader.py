# Copyright 2026 Snowflake Inc.
# SPDX-License-Identifier: Apache-2.0
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import csv
from pathlib import Path
from typing import Callable, Iterator, TypeVar

T = TypeVar("T")

DEFAULT_ENCODINGS = ("utf-8-sig", "utf-8", "latin-1")


def read_csv_rows(
    csv_path: str | Path,
    *,
    encodings: tuple[str, ...] = DEFAULT_ENCODINGS,
) -> Iterator[dict[str, str]]:
    """Yield stripped dict rows from a CSV file, trying multiple encodings."""
    csv_path = Path(csv_path)
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    last_error = None
    for encoding in encodings:
        try:
            with open(csv_path, "r", encoding=encoding, newline="") as f:
                reader = csv.DictReader(f)
                rows = []
                for row in reader:
                    rows.append(
                        {k: (v.strip() if v else "") for k, v in row.items()}
                    )
            yield from rows
            return
        except UnicodeDecodeError as e:
            last_error = e
            continue

    raise last_error or ValueError(
        f"Could not decode {csv_path} with any of {encodings}"
    )


def load_csv_as(
    csv_path: str | Path,
    factory: Callable[[dict[str, str]], T | None],
    *,
    encodings: tuple[str, ...] = DEFAULT_ENCODINGS,
) -> list[T]:
    """Load a CSV, map each row through factory, skip None results."""
    return [
        obj
        for row in read_csv_rows(csv_path, encodings=encodings)
        if (obj := factory(row)) is not None
    ]
