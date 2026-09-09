import re
from typing import List, Dict, Set, Tuple
from .parser import SASScript, SASBlock, BlockType


class DependencyTracker:

    EXTERNAL_LIBRARIES = {
        'oracle', 'teradata', 'db2', 'sqlsvr', 'odbc', 'oledb',
        'hadoop', 'spark', 'redshift', 'snowflake', 'postgres', 'mysql', 'mssql',
    }

    # Librefs that are local scratch or SAS-supplied metadata, never a data source.
    LOCAL_LIBREFS = {'WORK', 'SWORK'}
    SYSTEM_LIBREFS = {'DICTIONARY', 'SASHELP', 'SASUSER', 'MAPS', 'MAPSGFK', 'MAPSSAS'}
    _LIBREF_RE = re.compile(r'^[A-Za-z_][A-Za-z0-9_]*$')

    def analyze_file(self, script: SASScript) -> Dict:
        creates: Set[str] = set()
        reads: Set[str] = set()
        external_sources: List[Dict] = []

        for block in script.blocks:
            md = block.metadata
            for ds in md.get('output_datasets', []):
                creates.add(self._normalize_dataset(ds))
            for ds in md.get('input_datasets', []):
                reads.add(self._normalize_dataset(ds))

        for lib_name, lib_path in script.libraries.items():
            path_lower = lib_path.lower()
            for engine in self.EXTERNAL_LIBRARIES:
                if engine in path_lower or engine in lib_name.lower():
                    external_sources.append({
                        'libname': lib_name,
                        'engine': engine,
                        'path': lib_path,
                    })
                    break

        full_content = '\n'.join(b.content for b in script.blocks).lower()
        connect_pattern = r'connect\s+to\s+(\w+)'
        for match in re.finditer(connect_pattern, full_content):
            engine = match.group(1)
            if engine in self.EXTERNAL_LIBRARIES:
                external_sources.append({
                    'libname': 'PASSTHROUGH',
                    'engine': engine,
                    'path': f'CONNECT TO {engine}',
                })

        return {
            'creates': sorted(creates),
            'reads': sorted(reads),
            'external_sources': external_sources,
        }

    def build_cross_file_graph(self, file_analyses: Dict[str, Dict]) -> Dict:
        nodes = list(file_analyses.keys())
        edges: List[Dict] = []
        all_creates: Dict[str, str] = {}

        for filename, analysis in file_analyses.items():
            for dataset in analysis['creates']:
                all_creates[dataset] = filename

        for filename, analysis in file_analyses.items():
            for dataset in analysis['reads']:
                if dataset in all_creates and all_creates[dataset] != filename:
                    edges.append({
                        'from': all_creates[dataset],
                        'to': filename,
                        'via': dataset,
                    })

        external_inputs = set()
        for filename, analysis in file_analyses.items():
            for dataset in analysis['reads']:
                if dataset not in all_creates:
                    external_inputs.add(dataset)

        return {
            'nodes': nodes,
            'edges': edges,
            'external_inputs': sorted(external_inputs),
        }

    def build_source_inventory(self, file_analyses: Dict[str, Dict]) -> List[Dict]:
        """Aggregate qualified external libraries into a source inventory.

        One row per non-local libref (e.g. OWDATA, SFNGGRE) with its table count
        and read/write direction. Local WORK, unqualified, and SAS metadata
        librefs are dropped — they are scratch, not data sources.
        """
        engine_by_lib: Dict[str, str] = {}
        for analysis in file_analyses.values():
            for src in analysis.get('external_sources', []):
                engine_by_lib[src['libname'].upper()] = src['engine']

        reads_by_lib: Dict[str, Set[str]] = {}
        writes_by_lib: Dict[str, Set[str]] = {}
        for analysis in file_analyses.values():
            for ds in analysis.get('reads', []):
                lib, table = self._split_libref(ds)
                if lib:
                    reads_by_lib.setdefault(lib, set()).add(table)
            for ds in analysis.get('creates', []):
                lib, table = self._split_libref(ds)
                if lib:
                    writes_by_lib.setdefault(lib, set()).add(table)

        inventory: List[Dict] = []
        for lib in set(reads_by_lib) | set(writes_by_lib):
            if lib in self.LOCAL_LIBREFS or lib in self.SYSTEM_LIBREFS:
                continue
            if not self._LIBREF_RE.match(lib):
                continue
            rd = reads_by_lib.get(lib, set())
            wr = writes_by_lib.get(lib, set())
            direction = 'Read + Write' if rd and wr else ('Read' if rd else 'Write')
            inventory.append({
                'source': lib,
                'engine': engine_by_lib.get(lib, 'External SAS library'),
                'tables': len(rd | wr),
                'direction': direction,
                'table_names': sorted(rd | wr),
            })

        inventory.sort(key=lambda r: (-r['tables'], r['source']))
        return inventory

    def _split_libref(self, name: str):
        if '.' not in name:
            return None, name
        lib, _, table = name.partition('.')
        return lib.upper().strip(), table.strip()

    def generate_mermaid(self, graph: Dict) -> str:
        lines = ['graph LR']

        node_ids = {}
        for i, node in enumerate(graph['nodes']):
            node_id = f'F{i}'
            node_ids[node] = node_id
            safe_label = node.replace('.sas', '').replace(' ', '_')
            lines.append(f'    {node_id}["{safe_label}"]')

        for ext in graph.get('external_inputs', [])[:20]:
            ext_id = f'EXT_{ext.replace(".", "_").replace(" ", "")}'
            lines.append(f'    {ext_id}[("{ext}")]')

        for edge in graph['edges']:
            from_id = node_ids.get(edge['from'], '')
            to_id = node_ids.get(edge['to'], '')
            if from_id and to_id:
                lines.append(f'    {from_id} -->|"{edge["via"]}"| {to_id}')

        for ext in graph.get('external_inputs', [])[:20]:
            ext_id = f'EXT_{ext.replace(".", "_").replace(" ", "")}'
            for filename, analysis in []:
                pass

        return '\n'.join(lines)

    def generate_mermaid_with_externals(self, graph: Dict, file_analyses: Dict[str, Dict]) -> str:
        lines = ['graph LR']

        node_ids = {}
        for i, node in enumerate(graph['nodes']):
            node_id = f'F{i}'
            node_ids[node] = node_id
            safe_label = node.replace('.sas', '').replace(' ', '_')
            lines.append(f'    {node_id}["{safe_label}"]')

        ext_node_ids = {}
        for i, ext in enumerate(graph.get('external_inputs', [])[:20]):
            ext_id = f'EXT{i}'
            ext_node_ids[ext] = ext_id
            lines.append(f'    {ext_id}[("{ext}")]')

        for edge in graph['edges']:
            from_id = node_ids.get(edge['from'], '')
            to_id = node_ids.get(edge['to'], '')
            if from_id and to_id:
                lines.append(f'    {from_id} -->|"{edge["via"]}"| {to_id}')

        for filename, analysis in file_analyses.items():
            file_id = node_ids.get(filename, '')
            if not file_id:
                continue
            for dataset in analysis['reads']:
                if dataset in ext_node_ids:
                    lines.append(f'    {ext_node_ids[dataset]} --> {file_id}')

        return '\n'.join(lines)

    def _normalize_dataset(self, name: str) -> str:
        clean = re.sub(r'\([^)]*\)', '', name).strip()
        clean = clean.strip("'\"")
        return clean.upper()
