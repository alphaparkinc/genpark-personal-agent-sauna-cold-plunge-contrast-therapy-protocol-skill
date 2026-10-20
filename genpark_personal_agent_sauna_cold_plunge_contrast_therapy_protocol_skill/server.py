# -*- coding: utf-8 -*-
"""MCP Server for Sauna & Cold Plunge Contrast Therapy Longevity Protocol Skill."""
import sys
import json
import logging
from typing import Dict, Any

from .core import SaunaColdPlungeContrastTherapyProtocol

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

TOOLS_SCHEMA = [
    {
        "name": "design_contrast_therapy_session",
        "description": "Calculate optimal round durations and temperature targets for Finnish sauna (80-90\u00b0C) and cold plunge (10-15\u00b0C) to maximize norepinephrine secretion without blunting hypertrophy.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "primary_goal": {
                    "type": "string",
                    "enum": [
                        "cardiovascular_longevity",
                        "acute_dopamine_norepinephrine_boost",
                        "metabolic_brown_fat_activation",
                        "post_workout_recovery"
                    ]
                },
                "hours_since_strength_training": {
                    "type": "number"
                }
            },
            "required": [
                "primary_goal"
            ]
        }
    },
    {
        "name": "audit_weekly_thermal_dosage",
        "description": "Audit cumulative weekly sauna (target 57 mins) and cold water immersion (target 11 mins) against the Soberg Longevity Thresholds.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "logged_sauna_minutes": {
                    "type": "integer"
                },
                "logged_cold_plunge_minutes": {
                    "type": "integer"
                }
            },
            "required": [
                "logged_sauna_minutes",
                "logged_cold_plunge_minutes"
            ]
        }
    }
]

def handle_rpc(line: str) -> str:
    try:
        req = json.loads(line)
        method = req.get("method")
        msg_id = req.get("id")

        if method == "initialize":
            res = {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "genpark-personal-agent-sauna-cold-plunge-contrast-therapy-protocol-skill", "version": "1.0.0"}
            }
            return json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": res})

        elif method == "tools/list":
            return json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": {"tools": TOOLS_SCHEMA}})

        elif method == "tools/call":
            params = req.get("params", {})
            tool_name = params.get("name")
            args = params.get("arguments", {})

            target_func = getattr(SaunaColdPlungeContrastTherapyProtocol, tool_name, None)
            if not target_func:
                return json.dumps({"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": f"Method not found: {tool_name}"}})

            result = target_func(**args)
            return json.dumps({
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "content": [{"type": "text", "text": json.dumps(result, indent=2)}]
                }
            })

        else:
            return json.dumps({"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": f"Method not found: {method}"}})

    except Exception as e:
        return json.dumps({"jsonrpc": "2.0", "id": req.get("id") if "req" in locals() else None, "error": {"code": -32000, "message": str(e)}})

def run_test():
    print("[TEST] Running internal RPC self-test for genpark-personal-agent-sauna-cold-plunge-contrast-therapy-protocol-skill...")
    init_req = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}})
    init_res = json.loads(handle_rpc(init_req))
    assert init_res.get("result", {}).get("serverInfo", {}).get("name") == "genpark-personal-agent-sauna-cold-plunge-contrast-therapy-protocol-skill"

    list_req = json.dumps({"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}})
    list_res = json.loads(handle_rpc(list_req))
    assert len(list_res.get("result", {}).get("tools", [])) == 2
    print(f"[TEST] SUCCESS: {len(list_res['result']['tools'])} tools verified.")
    return True

if __name__ == "__main__":
    if "--test" in sys.argv:
        if run_test():
            sys.exit(0)
        sys.exit(1)

    for line in sys.stdin:
        if not line.strip():
            continue
        out = handle_rpc(line)
        sys.stdout.write(out + "\n")
        sys.stdout.flush()
