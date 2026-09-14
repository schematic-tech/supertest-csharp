#!/usr/bin/env python3
"""Build, test, pack, and consume the NuGet package from a local feed."""
import os
from pathlib import Path
import subprocess
import tempfile
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]
DOTNET = os.environ.get("DOTNET", "dotnet")


def run(*args, cwd=ROOT):
    subprocess.run(args, cwd=cwd, check=True)


run(sys.executable, "scripts/release.py", "check")
run(DOTNET, "run", "--project", "tests/Authoring/Authoring.csproj", "-c", "Release")
run(DOTNET, "pack", "src/Schematic.Supertest/Schematic.Supertest.csproj", "-c", "Release",
    "-o", "dist", "-p:ContinuousIntegrationBuild=true")
version = (ROOT / "VERSION").read_text().strip()
package = ROOT / "dist" / f"SchematicTech.Supertest.{version}.nupkg"
with zipfile.ZipFile(package) as archive:
    for name in ("lib/netstandard2.0/Schematic.Supertest.dll", "lib/netstandard2.0/Schematic.Supertest.xml",
                 "README.md", "LICENSE-MIT", "LICENSE-APACHE"):
        assert name in archive.namelist(), name
    assert archive.read("README.md") == (ROOT / "README.md").read_bytes()
assert (ROOT / "dist" / f"SchematicTech.Supertest.{version}.snupkg").is_file()
with tempfile.TemporaryDirectory(prefix="supertest-nuget-") as temporary:
    consumer = Path(temporary)
    (consumer / "Consumer.csproj").write_text(f'''<Project Sdk="Microsoft.NET.Sdk">
<PropertyGroup><OutputType>Exe</OutputType><TargetFramework>net8.0</TargetFramework></PropertyGroup>
<ItemGroup><PackageReference Include="SchematicTech.Supertest" Version="{version}" /></ItemGroup>
</Project>''')
    (consumer / "NuGet.Config").write_text(f'''<configuration><packageSources><clear />
<add key="local" value="{ROOT / 'dist'}" />
</packageSources><config><add key="globalPackagesFolder" value="{consumer / 'packages'}" /></config></configuration>''')
    (consumer / "Program.cs").write_text('''using Schematic;
using static Schematic.Assumptions;
class Program {
    [Supertest] static void Claim() { Assume(true); }
    static void Main() { Claim(); }
}''')
    run(DOTNET, "run", "--project", str(consumer / "Consumer.csproj"), "-c", "Release", cwd=consumer)
