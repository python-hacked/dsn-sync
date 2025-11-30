# 📦 PyPI Publishing Guide

## Prerequisites

1. ✅ PyPI account created
2. ✅ PyPI API token generated
3. ✅ Token configured in `.pypirc` file
4. Install required tools:
   ```bash
   pip install twine build
   ```

## Configuration

### PyPI Token Setup

The `.pypirc` file is already configured with your PyPI token. This file is in `.gitignore` to keep your token secure.

**Location:** `~/.pypirc` or project root `.pypirc`

**Format:**
```ini
[pypi]
username = __token__
password = YOUR_PYPI_API_TOKEN_HERE
```

## Steps to Publish

### 1. Build the Package

```bash
# Clean previous builds
rm -rf build/ dist/ *.egg-info

# Build the package
python -m build
```

This will create:
- `dist/dsn_sync-0.1.0-py3-none-any.whl` (wheel)
- `dist/dsn-sync-0.1.0.tar.gz` (source distribution)

### 2. Test on TestPyPI First (Recommended)

```bash
# Upload to TestPyPI
twine upload --repository testpypi dist/*

# Test installation
pip install --index-url https://test.pypi.org/simple/ dsn-sync
```

### 3. Publish to PyPI

```bash
# Upload to PyPI (token will be read from .pypirc automatically)
twine upload dist/*
```

**Note:** With `.pypirc` configured, you won't be prompted for username/password. The token will be used automatically.

### Alternative: Manual Token Entry

If you prefer not to use `.pypirc`, you can use environment variable:

```bash
# Set token as environment variable
export TWINE_PASSWORD="YOUR_PYPI_API_TOKEN_HERE"

# Upload
twine upload dist/*
```

Or use command line:

```bash
twine upload dist/* --username __token__ --password YOUR_PYPI_API_TOKEN_HERE
```

## After Publishing

1. Verify on PyPI: https://pypi.org/project/dsn-sync/
2. Test installation: `pip install dsn-sync`
3. Update version in `setup.py` and `pyproject.toml` for next release

## Version Update

When updating version:
1. Update `version` in `setup.py`
2. Update `version` in `pyproject.toml`
3. Update `__version__` in `dsn_sync/__init__.py`
4. Update version badge in `README.md`

## Quick Publish Script

Create a script for easy publishing:

```bash
#!/bin/bash
# publish.sh

echo "Cleaning previous builds..."
rm -rf build/ dist/ *.egg-info

echo "Building package..."
python -m build

echo "Uploading to PyPI..."
twine upload dist/*

echo "Done! Check https://pypi.org/project/dsn-sync/"
```

Make it executable:
```bash
chmod +x publish.sh
./publish.sh
```

## Notes

- ✅ Package name on PyPI: `dsn-sync` (with hyphen)
- ✅ Import name: `dsn_sync` (with underscore)
- ✅ `.pypirc` is in `.gitignore` (token is secure)
- ✅ Make sure all files are included in MANIFEST.in

## Security

⚠️ **Important:**
- Never commit `.pypirc` to git (already in `.gitignore`)
- Never share your PyPI token publicly
- If token is compromised, revoke it immediately at https://pypi.org/manage/account/token/

## Troubleshooting

### Error: "Invalid credentials"
- Check if token is correct in `.pypirc`
- Verify token hasn't expired
- Regenerate token if needed

### Error: "Package already exists"
- Update version number
- Or delete old version from PyPI (if you have permissions)

### Error: "File already exists"
- Clean dist/ folder: `rm -rf dist/`
- Rebuild: `python -m build`
