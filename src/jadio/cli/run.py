import json
import subprocess
import shlex
from pathlib import Path
from rich.console import Console

console = Console()

def run_script(args):
    """Run a script defined in jadio.json"""
    if not args:
        console.print("[red]Error:[/red] Script name required")
        console.print("Usage: jadio run <script>")
        return
    
    script_name = args[0]
    script_args = args[1:]  # Additional arguments to pass to the script
    
    # Check if we're in a jadio project
    if not Path("jadio.json").exists():
        console.print("[red]Error:[/red] Not in a jadio project directory")
        console.print("Run 'jadio init' first")
        return
    
    # Load registry
    with open("jadio.json", "r") as f:
        registry = json.load(f)
    
    scripts = registry.get("scripts", {})
    
    if script_name not in scripts:
        console.print(f"[red]Error:[/red] Script '{script_name}' not found")
        if scripts:
            console.print("\nAvailable scripts:")
            for name, command in scripts.items():
                console.print(f"  [green]{name}[/green]: {command}")
        else:
            console.print("\nNo scripts defined in jadio.json")
            console.print("Add scripts to the 'scripts' section:")
            console.print('  "scripts": {')
            console.print('    "dev": "python app.py --dev",')
            console.print('    "start": "python app.py"')
            console.print('  }')
        return
    
    command = scripts[script_name]
    
    # Append additional arguments
    if script_args:
        command += " " + " ".join(shlex.quote(arg) for arg in script_args)
    
    console.print(f"[blue]Running:[/blue] {command}")
    console.print()
    
    try:
        # Run the command in the current directory
        result = subprocess.run(command, shell=True, cwd=Path.cwd())
        
        if result.returncode != 0:
            console.print(f"\n[red]Script exited with code {result.returncode}[/red]")
        else:
            console.print(f"\n[green]✓[/green] Script completed successfully")
            
    except KeyboardInterrupt:
        console.print(f"\n[yellow]Script interrupted[/yellow]")
    except Exception as e:
        console.print(f"\n[red]Error running script:[/red] {e}")