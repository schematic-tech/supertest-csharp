#!/usr/bin/env python3
"""Publish NuGet packages, verifying existing contents before skipping an upload."""
from __future__ import annotations

import io
import os
from pathlib import Path
import subprocess
import urllib.error
import urllib.request
import zipfile

from release import ROOT, VERSION, validate, verify_assets


def verify_existing(expected: bytes, published: bytes) -> None:
    # NuGet repository signing adds this entry without changing the package files.
    with zipfile.ZipFile(io.BytesIO(expected)) as source, zipfile.ZipFile(io.BytesIO(published)) as registry:
        expected_names = set(source.namelist())
        actual_names = set(registry.namelist()) - {'.signature.p7s'}
        if expected_names != actual_names or any(source.read(name) != registry.read(name) for name in expected_names):
            raise SystemExit('NuGet already contains this version with different package contents; release a new version')


def push(path: Path, *, symbols: bool = False) -> None:
    command = ['dotnet', 'nuget', 'push', str(path), '--source', 'https://api.nuget.org/v3/index.json',
               '--api-key', os.environ['NUGET_API_KEY']]
    # A main-package 409 can mean a reserved namespace, not just a duplicate.
    command += ['--skip-duplicate'] if symbols else ['--no-symbols']
    result = subprocess.run(command, cwd=ROOT)
    if result.returncode:
        raise SystemExit(f'NuGet rejected {path.name}; see its response above (exit {result.returncode}).')


def main() -> None:
    validate()
    verify_assets()
    if not os.environ.get('NUGET_API_KEY'):
        raise SystemExit('NuGet/login must supply NUGET_API_KEY')
    package = ROOT / 'dist' / f'SchematicTech.Supertest.{VERSION}.nupkg'
    symbols = ROOT / 'dist' / f'SchematicTech.Supertest.{VERSION}.snupkg'
    url = f'https://api.nuget.org/v3-flatcontainer/schematictech.supertest/{VERSION}/schematictech.supertest.{VERSION}.nupkg'
    try:
        with urllib.request.urlopen(url, timeout=60) as response:
            published = response.read()
    except urllib.error.HTTPError as error:
        if error.code != 404:
            raise
        published = None
    if published is None:
        push(package)
    else:
        verify_existing(package.read_bytes(), published)
        print('Verified identical existing NuGet package contents.')
    push(symbols, symbols=True)


if __name__ == '__main__':
    main()
