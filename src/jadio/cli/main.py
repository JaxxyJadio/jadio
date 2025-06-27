#!/usr/bin/env python3
import sys
import json
import importlib
from pathlib import Path
from rich.console import Console

console = Console()

def main():
    """Main entry point for jadio CLI"""
    if len(sys.argv) < 2:
        show_help([])
        return
    
    command = sys.argv[1]
    args = sys.argv[2:]
    
    # Load command mappings
    commands_file = Path(__file__).parent / "clicommands.json"
    
    try:
        with open(commands_file, 'r') as f:
            commands = json.load(f)
    except FileNotFoundError:
        console.print("[red]Error:[/red] Command configuration not found")
        return
    
    if command not in commands:
        console.print(f"[red]Unknown command:[/red] {command}")
        console.print(f"Available: {', '.join(commands.keys())}")
        return
    
    # Import and run the command
    try:
        module_name = commands[command]["module"]
        function_name = commands[command]["function"]
        
        module = importlib.import_module(f"jadio.cli.{module_name}")
        func = getattr(module, function_name)
        func(args)
        
    except Exception as e:
        console.print(f"[red]Error running command {command}:[/red] {e}")

def show_help(args):
    """Show help information"""
    console.print("[bold blue]Jadio[/bold blue] - Modular CLI framework")
    console.print("\n[bold]Usage:[/bold] jadio <command> [args...]")
    console.print("\n[bold]Available commands:[/bold]")
    console.print("  [green]init[/green]     Initialize a new jadio project")
    console.print("  [green]install[/green]  Install a jadio package")
    console.print("  [green]remove[/green]   Remove a jadio package")
    console.print("  [green]run[/green]      Run a jadio script")
    console.print("  [green]list[/green]     List installed packages")
    console.print("  [green]help[/green]     Show this help message")

if __name__ == "__main__":
    main()