import json
import os
from pathlib import Path
from rich.console import Console

console = Console()

def init_project(args):
    """Initialize a new jadio project"""
    cwd = Path.cwd()
    
    # Create directories
    jadio_modules = cwd / ".jadio_modules"
    jadio_config = cwd / "jadio_config"
    
    jadio_modules.mkdir(exist_ok=True)
    jadio_config.mkdir(exist_ok=True)
    
    # Create jadio.json registry
    jadio_json = cwd / "jadio.json"
    if not jadio_json.exists():
        registry = {
            "name": cwd.name,
            "version": "0.0.2",
            "packages": {},
            "scripts": {}
        }
        
        with open(jadio_json, 'w') as f:
            json.dump(registry, f, indent=2)
    
    console.print("[green]✓[/green] Jadio project initialized!")
    console.print(f"Created: [blue]{jadio_modules.relative_to(cwd)}/[/blue]")
    console.print(f"Created: [blue]{jadio_config.relative_to(cwd)}/[/blue]")
    console.print(f"Created: [blue]{jadio_json.name}[/blue]")