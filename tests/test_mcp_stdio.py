from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class TestMcpStdioServer(unittest.TestCase):
    def _run_rpc(self, requests: list[dict]) -> list[dict]:
        payload = "\n".join(json.dumps(r) for r in requests) + "\n"
        proc = subprocess.run(
            [sys.executable, "-m", "eu_us_opendata_mcp.server"],
            input=payload,
            capture_output=True,
            text=True,
            env={"PYTHONPATH": str(ROOT / "src")},
            timeout=30,
            check=True,
        )
        return [json.loads(line) for line in proc.stdout.splitlines() if line.strip()]

    def test_initialize_and_tools_list(self) -> None:
        replies = self._run_rpc(
            [
                {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}},
                {"jsonrpc": "2.0", "method": "notifications/initialized"},
                {"jsonrpc": "2.0", "id": 2, "method": "tools/list"},
            ]
        )
        self.assertEqual(len(replies), 2)
        self.assertEqual(replies[0]["result"]["serverInfo"]["name"], "eu-us-opendata-mcp")
        tool_names = [t["name"] for t in replies[1]["result"]["tools"]]
        self.assertEqual(
            tool_names,
            [
                "search_french_companies",
                "search_eu_public_tenders",
                "search_clinical_trials",
                "search_us_npi_providers",
            ],
        )

    def test_live_all_four_official_registries(self) -> None:
        replies = self._run_rpc(
            [
                {"jsonrpc": "2.0", "id": 10, "method": "tools/call", "params": {"name": "search_french_companies", "arguments": {"query": "794598813", "limit": 1}}},
                {"jsonrpc": "2.0", "id": 11, "method": "tools/call", "params": {"name": "search_eu_public_tenders", "arguments": {"country": "FRA", "cpv_prefix": "72", "limit": 1}}},
                {"jsonrpc": "2.0", "id": 12, "method": "tools/call", "params": {"name": "search_clinical_trials", "arguments": {"condition": "diabetes", "limit": 1}}},
                {"jsonrpc": "2.0", "id": 13, "method": "tools/call", "params": {"name": "search_us_npi_providers", "arguments": {"npi_number": "1588410302"}}},
            ]
        )
        self.assertEqual(len(replies), 4)
        for rep in replies:
            self.assertFalse(rep["result"]["isError"], f"Tool failed: {rep}")
            data = json.loads(rep["result"]["content"][0]["text"])
            self.assertGreaterEqual(data["returned"], 1)


if __name__ == "__main__":
    unittest.main()
