import io
import json
import unittest

from hq_cli import mcp_server
from hq_cli.catalog import CAPABILITIES


class McpServerTests(unittest.TestCase):
    def test_every_capability_is_a_distinct_typed_tool(self):
        tools = mcp_server.list_tools()
        by_name = {tool["name"]: tool for tool in tools}
        self.assertEqual(len(CAPABILITIES) + len(mcp_server.CONTROL_TOOLS), len(tools))
        self.assertEqual(len(tools), len(by_name))
        for identifier in CAPABILITIES:
            self.assertIn(mcp_server.capability_tool_name(identifier), by_name)
        paid = by_name["hq_collect_content"]["inputSchema"]
        self.assertIn("url", paid["properties"])
        self.assertIn("confirm", paid["properties"])
        self.assertIn("quote_token", paid["properties"])
        upload = by_name["hq_image_upload"]["inputSchema"]
        self.assertEqual({"file", "confirm"}, set(upload["required"]))

    def test_paid_call_reuses_cli_quote_and_confirmation_arguments(self):
        calls = []

        def runner(arguments, stdin_text):
            calls.append((arguments, json.loads(stdin_text)))
            return 0, {"schema": "hq.run/v1", "result": {"job_id": 12}}

        result = mcp_server.call_tool("hq_collect_content", {
            "url": "https://www.bilibili.com/video/BV1xx411c7mD",
            "confirm": True,
            "quote_token": "q.test",
        }, runner=runner)
        self.assertNotIn("isError", result)
        self.assertEqual({"url": "https://www.bilibili.com/video/BV1xx411c7mD"}, calls[0][1])
        self.assertEqual([
            "run", "collect-content", "--input", "@-", "--confirm", "--quote-token", "q.test",
        ], calls[0][0])

    def test_write_and_logout_are_blocked_without_confirmation(self):
        calls = []

        def runner(arguments, stdin_text):
            calls.append(arguments)
            return 0, {"ok": True}

        write = mcp_server.call_tool("hq_inspiration_like", {"id": 1001, "favorite": True}, runner=runner)
        logout = mcp_server.call_tool("hq_cli_logout", {}, runner=runner)
        self.assertTrue(write["isError"])
        self.assertTrue(logout["isError"])
        self.assertEqual([], calls)

    def test_stdio_handshake_lists_tools_and_calls_cli(self):
        requests = [
            {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2025-06-18"}},
            {"jsonrpc": "2.0", "method": "notifications/initialized"},
            {"jsonrpc": "2.0", "id": 2, "method": "server/discover", "params": {}},
            {"jsonrpc": "2.0", "id": 3, "method": "tools/list", "params": {}},
            {"jsonrpc": "2.0", "id": 4, "method": "tools/call", "params": {"name": "hq_cli_version", "arguments": {}}},
        ]
        source = io.StringIO("".join(json.dumps(item) + "\n" for item in requests))
        output = io.StringIO()

        def runner(arguments, stdin_text):
            self.assertEqual(["version"], arguments)
            return 0, {"schema": "hq.version/v1", "cli_version": "0.11.0"}

        self.assertEqual(0, mcp_server.serve(source, output, runner=runner))
        responses = [json.loads(line) for line in output.getvalue().splitlines()]
        self.assertEqual([1, 2, 3, 4], [item["id"] for item in responses])
        self.assertEqual("huangque", responses[0]["result"]["serverInfo"]["name"])
        self.assertEqual("2025-06-18", responses[0]["result"]["protocolVersion"])
        self.assertEqual("2026-07-28", responses[1]["result"]["supportedVersions"][0])
        self.assertEqual(len(CAPABILITIES) + len(mcp_server.CONTROL_TOOLS), len(responses[2]["result"]["tools"]))
        self.assertEqual("hq.version/v1", responses[3]["result"]["structuredContent"]["schema"])


if __name__ == "__main__":
    unittest.main()
