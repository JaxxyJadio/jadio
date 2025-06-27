import json
import subprocess
import sys
import shutil
import tempfile
from pathlib import Path
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
import requests

console = Console()

def install_package(args):
    """Install a jadio package"""
    if not args:
        console.print("[red]Error:[/red] Package name required")
        console.print("Usage: jadio install <package>")
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
    
    # Check if already installed
    if package_name in registry["packages"]:
        console.print(f"[yellow]Warning:[/yellow] Package '{package_name}' is already installed")
        return
    
    # Convert package name to PyPI package name
    pypi_package = f"jadio-{package_name}"
    
    console.print(f"[blue]Installing[/blue] {package_name}...")
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        
        # Check if package exists on PyPI
        task = progress.add_task("Checking PyPI...", total=None)
        if not check_package_exists(pypi_package):
            progress.stop()
            console.print(f"[red]Error:[/red] Package 'jadio-{package_name}' not found on PyPI")
            return
        
        # Install package to temporary location
        progress.update(task, description="Installing package...")
        temp_dir = install_to_temp(pypi_package)
        if not temp_dir:
            progress.stop()
            console.print(f"[red]Error:[/red] Failed to install {pypi_package}")
            return
        
        # Copy package contents to .jadio_modules
        progress.update(task, description="Setting up module...")
        module_dir = Path(".jadio_modules") / package_name
        module_dir.mkdir(parents=True, exist_ok=True)
        
        # Find the installed package in temp directory
        package_source = find_package_in_temp(temp_dir, f"jadio_{package_name.replace('-', '_')}")
        if package_source and package_source.exists():
            copy_package_contents(package_source, module_dir)
        else:
            # Fallback: create basic structure
            (module_dir / "__init__.py").touch()
        
        # Create config directory
        config_dir = Path("jadio_config")
        config_file = config_dir / f"{package_name}.json"
        if not config_file.exists():
            default_config = {"enabled": True, "version": "latest"}
            with open(config_file, "w") as f:
                json.dump(default_config, f, indent=2)
        
        # Update registry
        progress.update(task, description="Updating registry...")
        registry["packages"][package_name] = {
            "version": "latest", 
            "source": pypi_package
        }
        
        with open("jadio.json", "w") as f:
            json.dump(registry, f, indent=2)
        
        # Cleanup
        shutil.rmtree(temp_dir, ignore_errors=True)
        
        progress.stop()
    
    console.print(f"[green]✓[/green] Successfully installed {package_name}")
    console.print(f"  Module: [blue].jadio_modules/{package_name}/[/blue]")
    console.print(f"  Config: [blue]jadio_config/{package_name}.json[/blue]")

def check_package_exists(package_name):
    """Check if package exists on PyPI"""
    try:
        response = requests.get(f"https://pypi.org/pypi/{package_name}/json", timeout=10)
        return response.status_code == 200
    except:
        return False

def install_to_temp(package_name):
    """Install package to temporary directory"""
    try:
        temp_dir = tempfile.mkdtemp()
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", 
            "--target", temp_dir, 
            package_name
        ], capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            return temp_dir
        else:
            console.print(f"[red]Pip error:[/red] {result.stderr}")
            return None
    except Exception as e:
        console.print(f"[red]Install error:[/red] {e}")
        return None

def find_package_in_temp(temp_dir, package_dir_name):
    """Find the installed package directory"""
    temp_path = Path(temp_dir)
    
    # Look for the package directory
    possible_paths = [
        temp_path / package_dir_name,
        temp_path / package_dir_name.replace("_", "-"),
    ]
    
    for path in possible_paths:
        if path.exists() and path.is_dir():
            return path
    
    return None

def copy_package_contents(source_dir, target_dir):
    """Copy package contents to jadio modules"""
    for item in source_dir.iterdir():
        if item.is_file() and item.suffix == ".py":
            shutil.copy2(item, target_dir)
        elif item.is_dir() and not item.name.startswith("__pycache__"):
            target_subdir = target_dir / item.name
            target_subdir.mkdir(exist_ok=True)
            shutil.copytree(item, target_subdir, dirs_exist_ok=True)

def list_packages(args):
    """List installed packages"""
    if not Path("jadio.json").exists():
        console.print("[red]Error:[/red] Not in a jadio project directory")
        return
    
    with open("jadio.json", "r") as f:
        registry = json.load(f)
    
    packages = registry.get("packages", {})
    
    if not packages:
        console.print("[yellow]No packages installed[/yellow]")
        return
    
    console.print("[bold]Installed packages:[/bold]")
    for name, info in packages.items():
        version = info.get("version", "unknown")
        source = info.get("source", "unknown")
        console.print(f"  [green]{name}[/green] @ {version} ([dim]{source}[/dim])")