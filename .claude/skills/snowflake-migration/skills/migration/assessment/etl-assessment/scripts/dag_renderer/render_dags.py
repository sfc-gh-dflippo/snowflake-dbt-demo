"""Inject a dag_model.json into the static DAG template, one HTML file per graph."""

import argparse
import json
from pathlib import Path

_TEMPLATE_PATH = Path(__file__).resolve().parent / "dag_template.html"
_SENTINEL = "/*__DAG_DATA__*/"


def render_dags(dag_model_path: str, output_root: str) -> None:
    """Render each graph in the model to output_root/<graph.output_file>."""
    model_path = Path(dag_model_path)
    if not model_path.is_file():
        print(f"dag_model not found, skipping DAG render: {model_path}")
        return

    template = _TEMPLATE_PATH.read_text(encoding="utf-8")
    model = json.loads(model_path.read_text(encoding="utf-8"))
    root = Path(output_root)

    count = 0
    for graph in model.get("graphs", []):
        payload = json.dumps(graph).replace("</", "<\\/")
        html = template.replace(_SENTINEL, payload)
        out_path = root / graph["output_file"]
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(html, encoding="utf-8")
        count += 1

    print(f"Rendered {count} DAG HTML file(s) to {root}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Render ETL DAG HTML from a dag_model.json.")
    parser.add_argument("dag_model_path")
    parser.add_argument("--output-root", default=None)
    args = parser.parse_args()
    output_root = args.output_root or str(Path(args.dag_model_path).resolve().parent)
    render_dags(args.dag_model_path, output_root)


if __name__ == "__main__":
    main()
