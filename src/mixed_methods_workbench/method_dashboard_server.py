"""Local HTTP and JSON surface for the METHOD-DASH-C1 review prototype."""

from __future__ import annotations

import argparse
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
from typing import ClassVar

from pydantic import ValidationError

from .method_dashboard import StudyBrief, dashboard_catalog, route_study


STATIC_PATH = Path(__file__).with_name("static") / "method_dashboard.html"
MAX_REQUEST_BYTES = 100_000


def catalog_payload() -> dict[str, object]:
    """Return JSON-compatible catalog data for agents and the browser."""
    return dashboard_catalog().model_dump(mode="json")


def route_payload(payload: object) -> tuple[HTTPStatus, dict[str, object]]:
    """Validate one study brief and return an explainable route or typed errors."""
    try:
        brief = StudyBrief.model_validate(payload)
    except ValidationError as exc:
        return HTTPStatus.UNPROCESSABLE_ENTITY, {
            "error": "The study brief needs correction.",
            "details": exc.errors(include_url=False, include_input=False),
        }
    return HTTPStatus.OK, route_study(brief).model_dump(mode="json")


class MethodDashboardHandler(BaseHTTPRequestHandler):
    """Serve one static work surface and the two matching typed JSON operations."""

    server_version = "MethodDashboard/0.1"
    html_path: ClassVar[Path] = STATIC_PATH

    def _write_json(self, status: HTTPStatus, payload: object) -> None:
        body = json.dumps(payload, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _write_html(self) -> None:
        body = self.html_path.read_bytes()
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:  # noqa: N802 - BaseHTTPRequestHandler contract
        """Serve the dashboard or its exact catalog."""
        if self.path in {"/", "/index.html"}:
            self._write_html()
            return
        if self.path == "/api/catalog":
            self._write_json(HTTPStatus.OK, catalog_payload())
            return
        self._write_json(HTTPStatus.NOT_FOUND, {"error": "Route not found."})

    def do_POST(self) -> None:  # noqa: N802 - BaseHTTPRequestHandler contract
        """Run the question-first router through a typed JSON boundary."""
        if self.path != "/api/route":
            self._write_json(HTTPStatus.NOT_FOUND, {"error": "Route not found."})
            return
        raw_length = self.headers.get("Content-Length")
        try:
            length = int(raw_length or "0")
        except ValueError:
            self._write_json(HTTPStatus.BAD_REQUEST, {"error": "Invalid Content-Length."})
            return
        if length <= 0 or length > MAX_REQUEST_BYTES:
            self._write_json(
                HTTPStatus.REQUEST_ENTITY_TOO_LARGE if length > MAX_REQUEST_BYTES else HTTPStatus.BAD_REQUEST,
                {"error": "Request body is missing or too large."},
            )
            return
        try:
            payload = json.loads(self.rfile.read(length))
        except (json.JSONDecodeError, UnicodeDecodeError):
            self._write_json(HTTPStatus.BAD_REQUEST, {"error": "Request body must be valid JSON."})
            return
        status, result = route_payload(payload)
        self._write_json(status, result)

    def log_message(self, format_string: str, *args: object) -> None:
        """Retain concise standard request logging for local diagnosis."""
        super().log_message(format_string, *args)


def main() -> None:
    """Launch the local dashboard without adding a production service framework."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()
    server = ThreadingHTTPServer((args.host, args.port), MethodDashboardHandler)
    print(f"Methodology dashboard: http://{args.host}:{args.port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
