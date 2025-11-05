# analyzer/analyzer.py

import os
import importlib.util
import sqlite3
import json
from datetime import datetime

RULES_DIR = os.path.join(os.path.dirname(__file__), 'rules')

def find_rules():
    """Finds all rule modules in the rules directory."""
    rule_modules = []
    for rule_name in os.listdir(RULES_DIR):
        rule_dir = os.path.join(RULES_DIR, rule_name)
        if os.path.isdir(rule_dir):
            for file_name in os.listdir(rule_dir):
                if file_name.endswith('.py') and not file_name.startswith('__'):
                    module_name = f"analyzer.rules.{rule_name}.{file_name[:-3]}"
                    module_path = os.path.join(rule_dir, file_name)
                    spec = importlib.util.spec_from_file_location(module_name, module_path)
                    if spec and spec.loader:
                        module = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(module)
                        if hasattr(module, 'analyze'):
                            rule_modules.append(module)
    return rule_modules

def analyze_replay(db_path, output_dir):
    """
    Analyzes a replay using all available rule plugins.

    Args:
        db_path: Path to the parsed replay database.
        output_dir: Directory to save the analysis results.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    all_alerts = []
    rule_modules = find_rules()

    print(f"Found {len(rule_modules)} rule(s) to run...")

    for module in rule_modules:
        try:
            print(f"Running rule: {module.__name__}...")
            alerts = module.analyze(cursor)
            for alert in alerts:
                all_alerts.append(alert)
        except Exception as e:
            print(f"Error running rule {module.__name__}: {e}")

    conn.close()

    # Save alerts to a JSON file
    if all_alerts:
        alerts_file_path = os.path.join(output_dir, 'alerts.json')
        with open(alerts_file_path, 'w') as f:
            json.dump(all_alerts, f, indent=4)
        print(f"Analysis complete. {len(all_alerts)} alert(s) saved to {alerts_file_path}")
    else:
        print("Analysis complete. No alerts were generated.")

# This script is intended to be used as a module.