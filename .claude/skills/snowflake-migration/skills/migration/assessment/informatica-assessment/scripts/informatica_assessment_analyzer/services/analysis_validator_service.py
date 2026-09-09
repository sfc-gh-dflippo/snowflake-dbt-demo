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

"""AnalysisValidatorService — validates AI analysis text structure and quality."""

from typing import Tuple


class AnalysisValidatorService:
    """Validates that AI analysis meets quality requirements.

    Required sections (paragraph-separated):
    1. Classification: — min 200 chars, 50 words
    2. Sources & Destinations: — min 100 chars, 30 words
    3. Purpose: — min 100 chars, 30 words
    4. Conversion: — min 100 chars, 30 words
    """

    VALID_CLASSIFICATIONS = [
        "Data Transformation",
        "Ingestion",
        "Configuration & Control",
        "Mixed: Ingestion + Transformation",
    ]

    REQUIRED_SECTIONS = [
        ("Classification:", 200, 50),
        ("Sources & Destinations:", 100, 30),
        ("Purpose:", 100, 30),
        ("Conversion:", 100, 30),
    ]

    @classmethod
    def validate(cls, analysis_text: str) -> Tuple[bool, str]:
        """Validate analysis text structure.

        Returns:
            Tuple of (is_valid, error_message)
        """
        if not analysis_text or not analysis_text.strip():
            return False, "Analysis text is empty"

        for section_name, min_chars, min_words in cls.REQUIRED_SECTIONS:
            if section_name not in analysis_text:
                return False, f"Missing required section: {section_name}"

            # Extract section content
            section_start = analysis_text.index(section_name) + len(section_name)
            # Find the next section or end
            section_end = len(analysis_text)
            for other_name, _, _ in cls.REQUIRED_SECTIONS:
                if other_name != section_name and other_name in analysis_text:
                    other_pos = analysis_text.index(other_name)
                    if other_pos > section_start and other_pos < section_end:
                        section_end = other_pos

            content = analysis_text[section_start:section_end].strip()

            if len(content) < min_chars:
                return (
                    False,
                    f"Section '{section_name}' too short: "
                    f"{len(content)} chars (minimum {min_chars})",
                )

            word_count = len(content.split())
            if word_count < min_words:
                return (
                    False,
                    f"Section '{section_name}' too few words: "
                    f"{word_count} words (minimum {min_words})",
                )

        return True, ""

    @classmethod
    def validate_classification(cls, classification: str) -> Tuple[bool, str]:
        """Validate that a classification value is one of the allowed categories.

        Returns:
            Tuple of (is_valid, error_message)
        """
        if not classification or not classification.strip():
            return False, "Classification is empty"

        if classification not in cls.VALID_CLASSIFICATIONS:
            allowed = ", ".join(f'"{c}"' for c in cls.VALID_CLASSIFICATIONS)
            return (
                False,
                f"Invalid classification '{classification}'. "
                f"Must be one of: {allowed}",
            )

        return True, ""

    @classmethod
    def validate_and_report(
        cls, analysis_text: str, workflow_path: str
    ) -> Tuple[bool, str]:
        """Validate and format a user-facing error message if invalid."""
        is_valid, error = cls.validate(analysis_text)
        if not is_valid:
            return False, (
                f"Validation failed for {workflow_path}:\n"
                f"  {error}\n\n"
                f"Required sections:\n"
                f"  - Classification: (min 200 chars, 50 words)\n"
                f"  - Sources & Destinations: (min 100 chars, 30 words)\n"
                f"  - Purpose: (min 100 chars, 30 words)\n"
                f"  - Conversion: (min 100 chars, 30 words)"
            )
        return True, ""
