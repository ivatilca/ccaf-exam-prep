#!/usr/bin/env python3
"""
Audit logger: hook PostToolUse que registra cada accion del agente.
"""
import sys, json, datetime
from pathlib import Path

AUDIT_FILE = '.claude/audit.log'

def log_action(event: dict):
    ts            = datetime.datetime.utcnow().isoformat() + 'Z'
    tool_name     = event.get('tool_name', 'unknown')
    tool_input    = event.get('tool_input', {})
    input_summary = str(tool_input)[:120]

    log_line = f'{ts} | {tool_name} | {input_summary}\n'

    Path(AUDIT_FILE).parent.mkdir(exist_ok=True)
    with open(AUDIT_FILE, 'a') as f:
        f.write(log_line)

    print(f'[AUDIT] {tool_name} registrado', file=sys.stderr)

if __name__ == '__main__':
    event = json.loads(sys.stdin.read())
    log_action(event)
    # PostToolUse no toma decisiones — solo observa
    # No hace falta devolver nada
