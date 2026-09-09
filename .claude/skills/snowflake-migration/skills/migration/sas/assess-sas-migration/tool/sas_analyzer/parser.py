import re
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum


class BlockType(Enum):
    PROC_SQL = "PROC_SQL"
    DATA_STEP = "DATA_STEP"
    PROC_SORT = "PROC_SORT"
    PROC_DATASETS = "PROC_DATASETS"
    PROC_APPEND = "PROC_APPEND"
    PROC_MEANS = "PROC_MEANS"
    PROC_SUMMARY = "PROC_SUMMARY"
    PROC_FREQ = "PROC_FREQ"
    PROC_TRANSPOSE = "PROC_TRANSPOSE"
    PROC_FORMAT = "PROC_FORMAT"
    PROC_PRINT = "PROC_PRINT"
    PROC_IMPORT = "PROC_IMPORT"
    PROC_EXPORT = "PROC_EXPORT"
    PROC_CONTENTS = "PROC_CONTENTS"
    PROC_OTHER = "PROC_OTHER"
    MACRO_DEF = "MACRO_DEF"
    MACRO_CALL = "MACRO_CALL"
    LET_STATEMENT = "LET_STATEMENT"
    LIBNAME = "LIBNAME"
    COMMENT = "COMMENT"
    UNKNOWN = "UNKNOWN"


@dataclass
class SASBlock:
    block_type: BlockType
    content: str
    start_line: int
    end_line: int
    raw_text: str
    complexity_score: int = 0
    sub_blocks: List['SASBlock'] = field(default_factory=list)
    metadata: Dict = field(default_factory=dict)


@dataclass
class SASScript:
    filename: str
    total_lines: int
    blocks: List[SASBlock]
    macros: Dict[str, SASBlock]
    macro_variables: Dict[str, str]
    libraries: Dict[str, str]
    complexity_score: int = 0


class SASParser:

    PROC_PATTERNS = {
        BlockType.PROC_SQL: r'(?i)^\s*PROC\s+SQL\b',
        BlockType.PROC_SORT: r'(?i)^\s*PROC\s+SORT\b',
        BlockType.PROC_DATASETS: r'(?i)^\s*PROC\s+DATASETS\b',
        BlockType.PROC_APPEND: r'(?i)^\s*PROC\s+APPEND\b',
        BlockType.PROC_MEANS: r'(?i)^\s*PROC\s+MEANS\b',
        BlockType.PROC_SUMMARY: r'(?i)^\s*PROC\s+SUMMARY\b',
        BlockType.PROC_FREQ: r'(?i)^\s*PROC\s+FREQ\b',
        BlockType.PROC_TRANSPOSE: r'(?i)^\s*PROC\s+TRANSPOSE\b',
        BlockType.PROC_FORMAT: r'(?i)^\s*PROC\s+FORMAT\b',
        BlockType.PROC_PRINT: r'(?i)^\s*PROC\s+PRINT\b',
        BlockType.PROC_IMPORT: r'(?i)^\s*PROC\s+IMPORT\b',
        BlockType.PROC_EXPORT: r'(?i)^\s*PROC\s+EXPORT\b',
        BlockType.PROC_CONTENTS: r'(?i)^\s*PROC\s+CONTENTS\b',
    }

    def __init__(self):
        self.macro_vars: Dict[str, str] = {}
        self.libraries: Dict[str, str] = {}

    def parse(self, content: str, filename: str = "unknown.sas") -> SASScript:
        lines = content.split('\n')
        total_lines = len(lines)

        content = self._remove_comments_preserve_structure(content)
        blocks = self._extract_blocks(content)

        macros = {b.metadata.get('name', ''): b for b in blocks if b.block_type == BlockType.MACRO_DEF}

        for block in blocks:
            block.complexity_score = self._calculate_block_complexity(block)

        total_complexity = sum(b.complexity_score for b in blocks)

        return SASScript(
            filename=filename,
            total_lines=total_lines,
            blocks=blocks,
            macros=macros,
            macro_variables=self.macro_vars.copy(),
            libraries=self.libraries.copy(),
            complexity_score=total_complexity
        )

    def _remove_comments_preserve_structure(self, content: str) -> str:
        content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
        content = re.sub(r'^\s*\*[^;]*;', '', content, flags=re.MULTILINE)
        return content

    def _extract_blocks(self, content: str) -> List[SASBlock]:
        blocks = []

        libname_pattern = r"(?i)LIBNAME\s+(\w+)\s+['\"]?([^;'\"]+)['\"]?\s*;"
        for match in re.finditer(libname_pattern, content):
            lib_name = match.group(1)
            lib_path = match.group(2).strip()
            self.libraries[lib_name.upper()] = lib_path
            blocks.append(SASBlock(
                block_type=BlockType.LIBNAME,
                content=match.group(0),
                start_line=content[:match.start()].count('\n') + 1,
                end_line=content[:match.end()].count('\n') + 1,
                raw_text=match.group(0),
                metadata={'name': lib_name, 'path': lib_path}
            ))

        let_pattern = r"(?i)%LET\s+(\w+)\s*=\s*([^;]+);"
        for match in re.finditer(let_pattern, content):
            var_name = match.group(1)
            var_value = match.group(2).strip()
            self.macro_vars[var_name.upper()] = var_value
            blocks.append(SASBlock(
                block_type=BlockType.LET_STATEMENT,
                content=match.group(0),
                start_line=content[:match.start()].count('\n') + 1,
                end_line=content[:match.end()].count('\n') + 1,
                raw_text=match.group(0),
                metadata={'name': var_name, 'value': var_value}
            ))

        macro_blocks = self._extract_macro_definitions(content)
        blocks.extend(macro_blocks)

        proc_sql_blocks = self._extract_proc_sql_blocks(content)
        blocks.extend(proc_sql_blocks)

        data_step_blocks = self._extract_data_step_blocks(content)
        blocks.extend(data_step_blocks)

        other_proc_blocks = self._extract_other_proc_blocks(content)
        blocks.extend(other_proc_blocks)

        blocks.sort(key=lambda b: b.start_line)
        return blocks

    def _extract_macro_definitions(self, content: str) -> List[SASBlock]:
        blocks = []
        macro_pattern = r"(?i)%MACRO\s+(\w+)(?:\s*\([^)]*\))?\s*;(.*?)%MEND\s*(?:\1)?\s*;"

        for match in re.finditer(macro_pattern, content, re.DOTALL):
            macro_name = match.group(1)
            macro_body = match.group(2)
            inner_blocks = self._extract_blocks(macro_body)

            blocks.append(SASBlock(
                block_type=BlockType.MACRO_DEF,
                content=match.group(0),
                start_line=content[:match.start()].count('\n') + 1,
                end_line=content[:match.end()].count('\n') + 1,
                raw_text=match.group(0),
                sub_blocks=inner_blocks,
                metadata={'name': macro_name}
            ))
        return blocks

    def _extract_proc_sql_blocks(self, content: str) -> List[SASBlock]:
        blocks = []
        proc_sql_pattern = r"(?i)(PROC\s+SQL\b[^;]*;)(.*?)(QUIT\s*;|(?=PROC\s+|DATA\s+|%MACRO\s+|$))"

        for match in re.finditer(proc_sql_pattern, content, re.DOTALL):
            proc_header = match.group(1)
            sql_body = match.group(2)
            terminator = match.group(3) or ''
            full_content = proc_header + sql_body + terminator

            metadata = self._parse_sql_metadata(sql_body, proc_header)

            blocks.append(SASBlock(
                block_type=BlockType.PROC_SQL,
                content=full_content,
                start_line=content[:match.start()].count('\n') + 1,
                end_line=content[:match.end()].count('\n') + 1,
                raw_text=full_content,
                metadata=metadata
            ))
        return blocks

    def _parse_sql_metadata(self, sql_body: str, proc_header: str) -> Dict:
        metadata = {
            'output_datasets': [],
            'input_datasets': [],
            'noprint': 'noprint' in proc_header.lower()
        }

        create_pattern = r"(?i)CREATE\s+TABLE\s+(\S+)"
        for match in re.finditer(create_pattern, sql_body):
            metadata['output_datasets'].append(match.group(1).rstrip('('))

        from_pattern = r"(?i)\bFROM\s+(\w+\.?\w*)"
        join_pattern = r"(?i)\bJOIN\s+(\w+\.?\w*)"
        for match in re.finditer(from_pattern, sql_body):
            tbl = match.group(1)
            if tbl.upper() not in ('DUAL', 'DICTIONARY'):
                metadata['input_datasets'].append(tbl)
        for match in re.finditer(join_pattern, sql_body):
            metadata['input_datasets'].append(match.group(1))

        return metadata

    def _extract_data_step_blocks(self, content: str) -> List[SASBlock]:
        blocks = []
        data_step_pattern = r"(?i)(DATA\s+([^;]+)\s*;)(.*?)(RUN\s*;)"

        for match in re.finditer(data_step_pattern, content, re.DOTALL):
            data_header = match.group(1)
            output_datasets = match.group(2)
            data_body = match.group(3)
            run_stmt = match.group(4)
            full_content = data_header + data_body + run_stmt

            data_metadata = self._parse_data_step_body(data_body, output_datasets)

            blocks.append(SASBlock(
                block_type=BlockType.DATA_STEP,
                content=full_content,
                start_line=content[:match.start()].count('\n') + 1,
                end_line=content[:match.end()].count('\n') + 1,
                raw_text=full_content,
                metadata=data_metadata
            ))
        return blocks

    def _parse_data_step_body(self, body: str, output_datasets: str) -> Dict:
        out_datasets = []
        for ds in output_datasets.split():
            clean = re.sub(r'\([^)]*\)', '', ds).strip()
            if clean and clean.upper() != '_NULL_':
                out_datasets.append(clean)

        metadata = {
            'output_datasets': out_datasets,
            'input_datasets': [],
            'has_retain': bool(re.search(r'(?i)\bRETAIN\b', body)),
            'has_array': bool(re.search(r'(?i)\bARRAY\b', body)),
            'has_merge': False,
            'has_first_last': bool(re.search(r'(?i)\b(FIRST\.|LAST\.)', body)),
            'by_vars': [],
        }

        set_match = re.search(r'(?i)SET\s+([^;]+)\s*;', body)
        if set_match:
            datasets = set_match.group(1)
            for ds in re.split(r'\s+', datasets):
                clean = re.sub(r'\([^)]*\)', '', ds).strip()
                if clean and not clean.upper().startswith('END=') and not clean.upper().startswith('NOBS='):
                    metadata['input_datasets'].append(clean)

        merge_match = re.search(r'(?i)MERGE\s+([^;]+)\s*;', body)
        if merge_match:
            metadata['has_merge'] = True
            datasets = merge_match.group(1)
            for ds in re.split(r'\s+', datasets):
                clean = re.sub(r'\([^)]*\)', '', ds).strip()
                if clean:
                    metadata['input_datasets'].append(clean)

        by_match = re.search(r'(?i)BY\s+([^;]+)\s*;', body)
        if by_match:
            metadata['by_vars'] = [v.strip() for v in by_match.group(1).split()
                                   if v.strip() and v.upper() not in ('DESCENDING', 'ASCENDING')]

        return metadata

    def _extract_other_proc_blocks(self, content: str) -> List[SASBlock]:
        blocks = []

        for block_type, pattern in self.PROC_PATTERNS.items():
            if block_type == BlockType.PROC_SQL:
                continue

            # Strip the leading ^\s* anchor: these patterns are matched WITHOUT
            # re.MULTILINE, so ^ would only match the very start of the file and
            # silently drop every PROC after the first statement. Use a word
            # boundary so we still match PROC anywhere in the content.
            clean_pattern = pattern.replace('(?i)', '').replace(r'^\s*', r'\b')
            proc_pattern = rf"({clean_pattern}[^;]*;)(.*?)((?:QUIT|RUN)\s*;)"

            for match in re.finditer(proc_pattern, content, re.DOTALL | re.IGNORECASE):
                proc_header = match.group(1)
                proc_body = match.group(2)
                terminator = match.group(3)
                full_content = proc_header + proc_body + terminator

                metadata = self._parse_proc_metadata(proc_header, proc_body, block_type)

                blocks.append(SASBlock(
                    block_type=block_type,
                    content=full_content,
                    start_line=content[:match.start()].count('\n') + 1,
                    end_line=content[:match.end()].count('\n') + 1,
                    raw_text=full_content,
                    metadata=metadata
                ))

        # Catch-all for any PROC not covered by a specific pattern above (e.g.
        # PROC REG / GLM / LOGISTIC / TABULATE / REPORT / SGPLOT ...). Without
        # this, statistical and other PROCs are invisible to counting and
        # tiering, diverging from how the conversion skill enumerates blocks.
        known = 'SQL|SORT|DATASETS|APPEND|MEANS|SUMMARY|FREQ|TRANSPOSE|FORMAT|PRINT|IMPORT|EXPORT|CONTENTS'
        generic_pattern = rf"(\bPROC\s+(?!(?:{known})\b)\w+\b[^;]*;)(.*?)((?:QUIT|RUN)\s*;)"
        for match in re.finditer(generic_pattern, content, re.DOTALL | re.IGNORECASE):
            proc_header = match.group(1)
            proc_body = match.group(2)
            terminator = match.group(3)
            full_content = proc_header + proc_body + terminator

            metadata = self._parse_proc_metadata(proc_header, proc_body, BlockType.PROC_OTHER)

            blocks.append(SASBlock(
                block_type=BlockType.PROC_OTHER,
                content=full_content,
                start_line=content[:match.start()].count('\n') + 1,
                end_line=content[:match.end()].count('\n') + 1,
                raw_text=full_content,
                metadata=metadata
            ))
        return blocks

    def _parse_proc_metadata(self, header: str, body: str, block_type: BlockType) -> Dict:
        metadata: Dict = {'input_datasets': [], 'output_datasets': []}

        data_match = re.search(r'(?i)DATA\s*=\s*(\S+)', header)
        out_match = re.search(r'(?i)OUT\s*=\s*(\S+)', header)

        if data_match:
            metadata['input_datasets'].append(re.sub(r'\([^)]*\)', '', data_match.group(1)))
        if out_match:
            metadata['output_datasets'].append(re.sub(r'\([^)]*\)', '', out_match.group(1)))

        if block_type == BlockType.PROC_SORT:
            metadata['nodupkey'] = 'nodupkey' in header.lower()
        elif block_type == BlockType.PROC_APPEND:
            base_match = re.search(r'(?i)BASE\s*=\s*(\S+)', header + body)
            if base_match:
                metadata['output_datasets'].append(re.sub(r'\([^)]*\)', '', base_match.group(1)))

        output_match = re.search(r'(?i)OUTPUT\s+OUT\s*=\s*(\S+)', body)
        if output_match:
            metadata['output_datasets'].append(re.sub(r'\([^)]*\)', '', output_match.group(1)))

        return metadata

    def _calculate_block_complexity(self, block: SASBlock) -> int:
        type_scores = {
            BlockType.PROC_SQL: 3,
            BlockType.DATA_STEP: 3,
            BlockType.PROC_SORT: 1,
            BlockType.MACRO_DEF: 4,
            BlockType.PROC_TRANSPOSE: 2,
            BlockType.PROC_MEANS: 2,
            BlockType.PROC_SUMMARY: 2,
            BlockType.PROC_FREQ: 2,
        }
        score = type_scores.get(block.block_type, 1)

        content_lower = block.content.lower()
        score += content_lower.count('join') * 2
        score += content_lower.count('case when') * 1
        score += content_lower.count('group by') * 1
        score += content_lower.count('having') * 1
        score += len(re.findall(r'(?i)\bif\b', content_lower))
        score += content_lower.count('%do') * 2
        score += content_lower.count('array') * 2
        score += content_lower.count('retain') * 1

        if block.metadata.get('has_merge'):
            score += 3
        if block.metadata.get('has_first_last'):
            score += 2

        score += len(block.sub_blocks) * 2
        return score
