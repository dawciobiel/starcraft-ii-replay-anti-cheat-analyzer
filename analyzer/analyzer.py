# analyzer/analyzer.py

import os
import importlib.util
import sqlite3
import json
from datetime import datetime
import inspect

RULES_DIR = os.path.join(os.path.dirname(__file__), 'rules')

class BaseRule:
    """Base class for all analyzer rules."""
    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = None
        self.cursor = None

    def connect_db(self):
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

    def close_db(self):
        if self.conn:
            self.conn.close()

    def run(self):
        """
        Executes the rule's analysis logic.
        This method must be implemented by all concrete rule classes.
        """
        raise NotImplementedError

    def _insert_alert(self, player_id, tick, type, description):
        """Helper to insert an alert into the database."""
        if not self.cursor:
            raise ConnectionError("Database connection not established for alert insertion.")
        self.cursor.execute("""
            INSERT INTO alerts (player_id, tick, type, description)
            VALUES (?, ?, ?, ?)
        """, (player_id, tick, type, description))
        self.conn.commit()

def find_rules():
    """Finds all rule modules/classes in the rules directory."""
    found_rules = []
    for rule_name in os.listdir(RULES_DIR):
        rule_dir = os.path.join(RULES_DIR, rule_name)
        if os.path.isdir(rule_dir):
            for file_name in os.listdir(rule_dir):
                if file_name.endswith('.py') and not file_name.startswith('__'):
                    module_full_name = f"analyzer.rules.{rule_name}.{file_name[:-3]}"
                    module_path = os.path.join(rule_dir, file_name)
                    spec = importlib.util.spec_from_file_location(module_full_name, module_path)
                    if spec and spec.loader:
                        module = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(module)

                        # Check for new-style BaseRule classes
                        for name, obj in inspect.getmembers(module):
                            if inspect.isclass(obj) and issubclass(obj, BaseRule) and obj is not BaseRule:
                                found_rules.append(("class", obj))
                        
                        # Check for old-style modules with an 'analyze' function
                        # Ensure we don't add the same module twice if it contains a BaseRule class
                        if hasattr(module, 'analyze') and not any(item[1] == module for item in found_rules if item[0] == "module"):
                            found_rules.append(("module", module))
    return found_rules

def analyze_replay(db_path, output_dir):
    """
    Analyzes a replay using all available rule plugins.

    Args:
        db_path: Path to the parsed replay database.
        output_dir: Directory to save the analysis results.
    """
    found_rules = find_rules()
    all_alerts = [] # This will now be collected from the DB after all rules run

    print(f"Found {len(found_rules)} rule(s) to run...")

    for rule_type, rule_obj in found_rules:
        if rule_type == "class":
            rule_instance = None
            try:
                rule_instance = rule_obj(db_path)
                rule_instance.connect_db()
                print(f"Running rule (class): {rule_obj.__name__}...")
                rule_instance.run()
            except Exception as e:
                print(f"Error running rule class {rule_obj.__name__}: {e}")
            finally:
                if rule_instance:
                    rule_instance.close_db()
        elif rule_type == "module":
            conn = None
            try:
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                print(f"Running rule (module): {rule_obj.__name__}...")
                alerts = rule_obj.analyze(cursor)
                for alert in alerts:
                    # For old-style modules, we still collect alerts and insert them
                    # This assumes old-style alerts are dicts with player_id, tick, type, description
                    cursor.execute("""
                        INSERT INTO alerts (player_id, tick, type, description)
                        VALUES (?, ?, ?, ?)
                    """, (alert["player_id"], alert["tick"], alert["type"], alert["description"])) # Assuming alert is a dict
                conn.commit()
            except Exception as e:
                print(f"Error running rule module {rule_obj.__name__}: {e}")
            finally:
                if conn:
                    conn.close()

    # After all rules have run, retrieve alerts from the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT player_id, tick, type, description FROM alerts")
    alerts_from_db = cursor.fetchall()
    conn.close()

    if alerts_from_db:
        # Convert to a list of dicts for JSON output, if still desired
        for alert in alerts_from_db:
            all_alerts.append({
                "player_id": alert[0],
                "tick": alert[1],
                "type": alert[2],
                "description": alert[3]
            })

        alerts_file_path = os.path.join(output_dir, 'alerts.json')
        with open(alerts_file_path, 'w') as f:
            json.dump(all_alerts, f, indent=4)
        print(f"Analysis complete. {len(all_alerts)} alert(s) saved to {alerts_file_path}")
    else:
        print("Analysis complete. No alerts were generated.")

# This script is intended to be used as a module.