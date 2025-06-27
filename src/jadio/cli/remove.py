import json
import shutil
from pathlib import Path
from rich.console import Console

console = Console()

def remove_package(args):
    """Remove a jadio package"""
    if not args:
        console.print("[red]Error:[/red] Package name required")
        console.print("Usage: jadio remove <package>")
        return
    
    package_name = args[0]
    
    # Check if we're in a jadio project
    if not Path("jadio.json").exists():
        console.print("[red]Error:[/red] Not in a jadio project directory")
        console.print("Run 'jadio init' first")
        return
    
    # Load current registry
    with open("jadio.json", "r") as f:
        registry = json.load(f)
    
    # Check if package is installed
    if package_name not in registry["packages"]:
        console.print(f"[yellow]Warning:[/yellow] Package '{package_name}' is not installed")
        return
    
    console.print(f"[blue]Removing[/blue] {package_name}...")
    
    # Remove module directory
    module_dir = Path(".jadio_modules") / package_name
    if module_dir.exists():
        shutil.rmtree(module_dir)
        console.print(f"  [red]Removed:[/red] .jadio_modules/{package_name}/")
    
    # Remove config file
    config_file = Path("jadio_config") / f"{package_name}.json"
    if config_file.exists():
        config_file.unlink()
        console.print(f"  [red]Removed:[/red] jadio_config/{package_name}.json")
    
    # Update registry
    del registry["packages"][package_name]
    
    with open("jadio.json", "w") as f:
        json.dump(registry, f, indent=2)
    
    console.print(f"[green]✓[/green] Successfully removed {package_name}")