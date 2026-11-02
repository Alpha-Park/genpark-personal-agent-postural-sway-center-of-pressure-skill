"""
MCP Server for Postural Sway & Center of Pressure (COP) Statokinesigram.
Exposes JSON-RPC endpoints for 95% confidence ellipse area, sway velocity, and Romberg Quotient.
"""

import json
import sys
from client import PosturalSwayClient

client = PosturalSwayClient()


def handle_request(request: dict) -> dict:
    req_id = request.get("id")
    method = request.get("method")
    params = request.get("params", {})

    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "analyze_cop_sway",
                        "description": "Analyzes 2D center of pressure timeseries to compute 95% confidence ellipse area, path length, mean velocity, and postural stability index.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "x_coords_mm": {
                                    "type": "array",
                                    "items": {"type": "number"},
                                    "description": "Mediolateral (ML) displacement series in mm"
                                },
                                "y_coords_mm": {
                                    "type": "array",
                                    "items": {"type": "number"},
                                    "description": "Anterior-posterior (AP) displacement series in mm"
                                },
                                "sample_rate_hz": {
                                    "type": "number",
                                    "default": 50.0,
                                    "description": "Sampling frequency in Hz"
                                }
                            },
                            "required": ["x_coords_mm", "y_coords_mm"]
                        }
                    },
                    {
                        "name": "compute_romberg_quotient",
                        "description": "Calculates Romberg Quotient (Eyes Closed / Eyes Open sway area) to quantify visual dependence and proprioceptive integrity.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "eyes_open_sway_area_mm2": {"type": "number", "description": "95% confidence ellipse area with eyes open in mm^2"},
                                "eyes_closed_sway_area_mm2": {"type": "number", "description": "95% confidence ellipse area with eyes closed in mm^2"}
                            },
                            "required": ["eyes_open_sway_area_mm2", "eyes_closed_sway_area_mm2"]
                        }
                    }
                ]
            }
        }

    elif method == "tools/call":
        tool_name = params.get("name")
        args = params.get("arguments", {})

        if tool_name == "analyze_cop_sway":
            res = client.analyze_cop_sway(
                x_coords_mm=args.get("x_coords_mm", []),
                y_coords_mm=args.get("y_coords_mm", []),
                sample_rate_hz=args.get("sample_rate_hz", 50.0)
            )
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
            }

        elif tool_name == "compute_romberg_quotient":
            res = client.compute_romberg_quotient(
                eyes_open_sway_area_mm2=args.get("eyes_open_sway_area_mm2", 80.0),
                eyes_closed_sway_area_mm2=args.get("eyes_closed_sway_area_mm2", 130.0)
            )
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
            }

        else:
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32601, "message": f"Method {tool_name} not found"}
            }

    return {
        "jsonrpc": "2.0",
        "id": req_id,
        "error": {"code": -32600, "message": "Invalid Request"}
    }


def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            resp = handle_request(req)
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            err = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": str(e)}}
            sys.stdout.write(json.dumps(err) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
