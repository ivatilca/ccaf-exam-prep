#!/usr/bin/env python3
# pyrefly: ignore [missing-import]
from mcp.server.fastmcp import FastMCP
import sqlite3, os, json

app = FastMCP('rebel-db')
DB_PATH = os.getenv('REBEL_DB_PATH', '/Users/ivanatilca/Documents/Ivana Tilca/Demos/rebel_ops.db')

@app.tool()
def list_tables() -> str:
    """Lista todas las tablas disponibles en la base de datos."""
    conn = sqlite3.connect(DB_PATH)
    try:
        rows = conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
        return json.dumps([r[0] for r in rows])
    finally:
        conn.close()

@app.tool()
def query_database(sql: str) -> str:
    """Ejecuta una query SQL de solo lectura. NO usar para INSERT/UPDATE/DELETE."""
    if any(w in sql.upper() for w in ['INSERT', 'UPDATE', 'DELETE', 'DROP']):
        return json.dumps({'error': 'solo lectura. Usar execute_transaction.'})
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        rows = conn.execute(sql).fetchall()
        return json.dumps([dict(r) for r in rows])
    except Exception as e:
        return json.dumps({'error': str(e)})
    finally:
        conn.close()

@app.tool()
def execute_transaction(sql: str) -> str:
    """Ejecuta INSERT, UPDATE o DELETE. Requiere confirmacion."""
    conn = sqlite3.connect(DB_PATH)
    try:
        conn.execute(sql)
        conn.commit()
        return json.dumps({'ok': True})
    except Exception as e:
        return json.dumps({'error': str(e)})
    finally:
        conn.close()

if __name__ == '__main__':
    app.run(transport='stdio')
