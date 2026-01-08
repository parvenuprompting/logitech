import os
import re
import json

# Configuration
REPO_ROOT = "../.."
OUTPUT_FILE = "../../docs/governance/dependency_graph.json"

# Regex patterns to find table usages
# Matches: spark.read.table("bronze.telemetry") or spark.table("...")
READ_PATTERN = r'(?:spark\.read\.table|spark\.table)\(["\']([a-zA-Z0-9_]+\.[a-zA-Z0-9_]+)["\']\)'
# Matches: .saveAsTable("silver.trips")
WRITE_PATTERN = r'\.saveAsTable\(["\']([a-zA-Z0-9_]+\.[a-zA-Z0-9_]+)["\']\)'

def scan_files(root_dir):
    dependencies = []
    
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Skip hidden dirs and infrastructure
        if ".git" in dirpath or "infrastructure" in dirpath:
            continue
            
        for filename in filenames:
            if filename.endswith(".py") or filename.endswith(".sql"):
                full_path = os.path.join(dirpath, filename)
                rel_path = os.path.relpath(full_path, root_dir)
                
                with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    
                    reads = re.findall(READ_PATTERN, content)
                    writes = re.findall(WRITE_PATTERN, content)
                    
                    if reads or writes:
                        dependencies.append({
                            "file": rel_path,
                            "reads_from": list(set(reads)),
                            "writes_to": list(set(writes))
                        })
    return dependencies

def generate_markdown_graph(deps):
    md = "# Data Lineage Dependency Graph\n\n"
    md += "Genereerd door `tools/impact_analysis/generate_graph.py`\n\n"
    md += "```mermaid\nflowchart TD\n"
    
    for item in deps:
        script_node = item['file'].replace("/", "_").replace(".", "_")
        md += f"    subgraph {script_node} [{item['file']}]\n    end\n"
        
        for read in item['reads_from']:
            table_node = read.replace(".", "_")
            md += f"    {table_node}([{read}]) --> {script_node}\n"
            
        for write in item['writes_to']:
            table_node = write.replace(".", "_")
            md += f"    {script_node} --> {table_node}([{write}])\n"
            
    md += "```\n"
    return md

if __name__ == "__main__":
    print(f"Scanning {REPO_ROOT} for dependencies...")
    deps = scan_files(REPO_ROOT)
    
    # Generate JSON
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(deps, f, indent=2)
    print(f"Graph JSON written to {OUTPUT_FILE}")
    
    # Generate Markdown Visualization
    md_output = OUTPUT_FILE.replace(".json", ".md")
    with open(md_output, 'w') as f:
        f.write(generate_markdown_graph(deps))
    print(f"Graph Markdown written to {md_output}")
