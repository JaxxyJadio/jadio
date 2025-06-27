# Jadio Framework 

## 🎯 Framework Overview

Jadio is a modular CLI framework that brings npm-style package management to Python. It creates a clean, organized structure for managing modular Python packages with familiar commands.

### Core Concept
- **Main Framework**: `jadio` (published to PyPI)
- **Extension Packages**: `jadio-{name}` (e.g., `jadio-ai-server`, `jadio-database`)
- **Local Structure**: `.jadio_modules/` and `jadio_config/` in user projects
- **Registry**: `jadio.json` tracks installed packages and scripts

## 📁 Jadio Framework Structure

The main `jadio` framework follows this exact structure:

```
JADIO/
├── src/
│   └── jadio/
│       ├── __init__.py                 # Version: __version__ = "0.1.0"
│       └── cli/
│           ├── __init__.py             # Empty module file
│           ├── main.py                 # Main CLI entry point
│           ├── clicommands.json        # Command routing configuration
│           ├── init.py                 # jadio init command
│           ├── install.py              # jadio install command  
│           ├── remove.py               # jadio remove command
│           └── run.py                  # jadio run command
├── pyproject.toml                      # Modern Python packaging
├── README.md                           # User documentation
├── LICENSE                             # MIT License
└── .gitignore                          # Python gitignore
```

## ⚙️ How Jadio Works

### 1. Command Routing System

**`clicommands.json`** maps commands to Python functions:
```json
{
    "init": {"module": "init", "function": "init_project"},
    "install": {"module": "install", "function": "install_package"},
    "remove": {"module": "remove", "function": "remove_package"},
    "run": {"module": "run", "function": "run_script"},
    "list": {"module": "install", "function": "list_packages"},
    "help": {"module": "main", "function": "show_help"}
}
```

**`main.py`** dynamically imports and executes commands:
```python
# Load command mapping
module_name = commands[command]["module"]
function_name = commands[command]["function"]

# Import and execute
module = importlib.import_module(f"jadio.cli.{module_name}")
func = getattr(module, function_name)
func(args)
```

### 2. Project Structure Created by `jadio init`

When users run `jadio init`, it creates:
```
user-project/
├── .jadio_modules/          # Installed package modules
├── jadio_config/            # Package configuration files
└── jadio.json               # Project registry
```

**`jadio.json` format:**
```json
{
  "name": "project-name",
  "version": "1.0.0",
  "packages": {
    "server": {
      "version": "1.0.0",
      "source": "jadio-ai-server"
    }
  },
  "scripts": {
    "dev": "python server.py --dev",
    "start": "python server.py"
  }
}
```

### 3. Package Installation Process

When users run `jadio install server`:

1. **Package Discovery**: Converts `server` → `jadio-ai-server`
2. **PyPI Check**: Verifies package exists on PyPI
3. **Installation**: Downloads package to temporary directory
4. **Module Setup**: Copies files to `.jadio_modules/server/`
5. **Configuration**: Creates `jadio_config/server.json`
6. **Registry Update**: Adds entry to `jadio.json`

## 🏗️ Creating Jadio-Compatible Packages

### Package Naming Convention
- **PyPI Name**: `jadio-{component}` (e.g., `jadio-ai-server`)
- **Import Name**: `jadio_{component}` (e.g., `jadio_ai_server`)
- **Install Command**: `jadio install {component}` (e.g., `jadio install server`)

### Complete Package Template

Here's the exact structure for creating a new Jadio package:

```
jadio-ai-server/
├── src/
│   └── jadio_ai_server/
│       ├── __init__.py
│       ├── server.py               # Main functionality
│       ├── config/
│       │   ├── __init__.py
│       │   └── default.json        # Default configuration
│       └── templates/
│           ├── __init__.py
│           ├── app.py             # Template files to copy
│           └── requirements.txt
├── pyproject.toml
├── README.md
├── LICENSE
└── .gitignore
```

### pyproject.toml Template for Jadio Packages

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "jadio-ai-server"
dynamic = ["version"]
description = "AI Server module for Jadio framework"
readme = "README.md"
license = "MIT"
requires-python = ">=3.8"
authors = [
    {name = "Your Name", email = "your@email.com"},
]
classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.8+",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Framework :: Jadio",
]
dependencies = [
    "jadio>=0.1.0",
    "fastapi",
    "uvicorn",
]
keywords = ["jadio", "ai", "server", "framework"]

[tool.hatch.version]
path = "src/jadio_ai_server/__init__.py"

[tool.hatch.build.targets.wheel]
packages = ["src/jadio_ai_server"]
```

### Package Structure Requirements

**1. `src/jadio_ai_server/__init__.py`:**
```python
"""Jadio AI Server module"""
__version__ = "1.0.0"

# Optional: Installation hooks
def install_hook(project_path):
    """Called when package is installed via jadio install"""
    import shutil
    from pathlib import Path
    
    # Copy templates to project
    templates_dir = Path(__file__).parent / "templates"
    project_path = Path(project_path)
    
    for template in templates_dir.glob("*.py"):
        shutil.copy2(template, project_path)

def uninstall_hook(project_path):
    """Called when package is removed via jadio remove"""
    # Cleanup logic here
    pass
```

**2. `src/jadio_ai_server/config/default.json`:**
```json
{
    "server": {
        "host": "localhost",
        "port": 8000,
        "debug": false
    },
    "ai": {
        "model": "gpt-3.5-turbo",
        "max_tokens": 1000
    }
}
```

**3. `src/jadio_ai_server/server.py`:**
```python
"""Main AI Server implementation"""
import json
from pathlib import Path
from fastapi import FastAPI

def create_server():
    """Create FastAPI server instance"""
    app = FastAPI(title="Jadio AI Server")
    
    @app.get("/")
    def read_root():
        return {"message": "Jadio AI Server is running!"}
    
    return app

def load_config():
    """Load configuration from jadio_config"""
    config_path = Path("jadio_config/server.json")
    if config_path.exists():
        with open(config_path) as f:
            return json.load(f)
    return {}

if __name__ == "__main__":
    import uvicorn
    app = create_server()
    config = load_config()
    
    host = config.get("server", {}).get("host", "localhost")
    port = config.get("server", {}).get("port", 8000)
    
    uvicorn.run(app, host=host, port=port)
```

**4. `src/jadio_ai_server/templates/app.py`:**
```python
"""Template application file"""
from jadio_ai_server import create_server, load_config

# This file gets copied to the user's project root
app = create_server()
config = load_config()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
```

## 📋 Package Development Workflow

### 1. Create Package Structure
```bash
# Create new package
mkdir jadio-ai-server
cd jadio-ai-server

# Create source structure
mkdir -p src/jadio_ai_server/{config,templates}
touch src/jadio_ai_server/__init__.py
touch src/jadio_ai_server/config/__init__.py
touch src/jadio_ai_server/templates/__init__.py

# Add version
echo '__version__ = "1.0.0"' > src/jadio_ai_server/__init__.py
```

### 2. Implement Core Functionality
- Add main module files (server.py, client.py, etc.)
- Create default configuration files
- Add template files for user projects
- Implement optional install/uninstall hooks

### 3. Test Integration
```bash
# Test with local jadio
pip install -e ../jadio  # Install main framework
pip install -e .         # Install your package

# Test in new project
mkdir test-project
cd test-project
jadio init
jadio install ai-server  # Should find jadio-ai-server
jadio list
```

### 4. Publish to PyPI
```bash
# Build package
python -m build

# Upload to PyPI
python -m twine upload dist/*
```

## 🔧 Advanced Package Features

### Custom Installation Logic

Override the default installation by implementing hooks:

```python
# In your package's __init__.py
def install_hook(project_path):
    """Custom installation logic"""
    from pathlib import Path
    import json
    
    project_path = Path(project_path)
    
    # Create custom directory structure
    (project_path / "ai_models").mkdir(exist_ok=True)
    
    # Copy specific files
    templates_dir = Path(__file__).parent / "templates"
    for template in templates_dir.glob("**/*.py"):
        target = project_path / template.name
        shutil.copy2(template, target)
    
    # Create custom config
    config = {
        "ai_server": {
            "enabled": True,
            "models_path": "./ai_models",
            "default_model": "gpt-3.5-turbo"
        }
    }
    
    config_file = project_path / "jadio_config" / "server.json"
    with open(config_file, "w") as f:
        json.dump(config, f, indent=2)
```

### Script Integration

Packages can add scripts to the user's `jadio.json`:

```python
def install_hook(project_path):
    """Add scripts to jadio.json"""
    import json
    from pathlib import Path
    
    jadio_json = Path(project_path) / "jadio.json"
    
    with open(jadio_json, "r") as f:
        registry = json.load(f)
    
    # Add package-specific scripts
    registry["scripts"].update({
        "server:start": "python app.py",
        "server:dev": "python app.py --reload",
        "server:test": "python -m pytest tests/"
    })
    
    with open(jadio_json, "w") as f:
        json.dump(registry, f, indent=2)
```

## 🚀 Quick Start Template

### For AI Assistants: Creating a New Jadio Package

When asked to create a Jadio package, use this template:

1. **Ask for package name** (e.g., "database", "auth", "ui")
2. **Create structure** using the template above
3. **Set package name** as `jadio-{name}`
4. **Set import name** as `jadio_{name}`
5. **Implement core functionality** in the main module
6. **Add configuration** with sensible defaults
7. **Create templates** for user projects
8. **Test installation** with `jadio install {name}`

### Example Commands for AI to Use:

```bash
# When helping create a new package:
mkdir jadio-{name}
cd jadio-{name}

# Create the exact structure needed
mkdir -p src/jadio_{name}/{config,templates}
touch src/jadio_{name}/__init__.py
echo '__version__ = "1.0.0"' > src/jadio_{name}/__init__.py

# Create pyproject.toml with the template above
# Implement the main functionality
# Test with jadio framework
```

## 📝 Package Documentation Template

Every Jadio package should include this in its README:

```markdown
# jadio-{name}

{Description} module for the Jadio framework.

## Installation

```bash
# Install main framework first
pip install jadio

# Install this package
jadio install {name}
```

## Usage

```bash
# In your project directory
jadio init
jadio install {name}
jadio run {name}:start
```

## Configuration

The package creates `jadio_config/{name}.json` with these options:
- `option1`: Description
- `option2`: Description

## Scripts Added

- `{name}:start` - Start the {name} service
- `{name}:dev` - Run in development mode
- `{name}:test` - Run tests
```

This guide provides everything needed to understand and extend the Jadio framework!