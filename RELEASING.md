# Releasing

The interop library is dual licensed under **MIT OR Apache-2.0**, at the recipient's
option. Both license texts ship with the package. `VERSION` is the stable release
version and must agree with all package metadata.

Development happens in `schematic-internal`. A release is a squash snapshot copied
to the repository of the same name under `schematic-tech`. These workflows do not
copy history, create public repositories, or push release tags.

## Trigger and behavior

After copying the reviewed snapshot to the public repository, commit it, then push
a matching version tag such as `v0.1.0`. `.github/workflows/release.yml` runs CI,
builds and tests the installable artifacts, and publishes the same verified artifacts.
It only publishes from this repository's exact `schematic-tech` name. A private-repo
tag does not publish. A normal branch push only runs CI.

The publish job uses a GitHub environment named **release**. Create that environment
in the public repository before the first release. Set its deployment rules to
allow the release tags. Required reviewers are optional; omit them if tag pushes
should publish without a second manual step. Keep Actions enabled and allow the
pinned actions used in these workflows. GitHub release uploads use the automatically
provided `GITHUB_TOKEN`; no GitHub personal access token is needed.

All public GitHub releases include source `.tar.gz` and `.zip` archives, both
licenses, and `SHA256SUMS`, alongside the language-specific artifacts. Assets are
uploaded to a draft first and the draft is then published. Already published
GitHub release assets are not overwritten on retries.

## Versions and retries

Update `VERSION` and the language's package metadata together. The first prepared
version is `0.1.0`. The release validator rejects tags that do not match the package
version. Run CI on the final public squash commit before tagging it.

If publication fails partway through, correct the external configuration and rerun
the failed GitHub Actions run for the same tag. Registry uploads skip versions
already uploaded during an earlier attempt. Do not change the contents of an
already published version or move a published tag; use a new version for code fixes.

Registry publication is separate from checker support. These packages provide
markers and runtime assumptions; they do not expand Pup/backend language discovery.

## NuGet.org setup

Create or use the **`schematic-tech` NuGet organization**, using an individual
NuGet account that is a member. Add a trusted publishing policy with
**Package Owner `schematic-tech`**, a package scope permitting creation of
`SchematicTech.Supertest`, and:

| Field | Value |
| --- | --- |
| GitHub owner | `schematic-tech` |
| GitHub repository | `supertest-csharp` |
| Workflow filename | `release.yml` |
| Environment | `release` |

Set the GitHub repository or `release` environment **variable `NUGET_USER`** to the
individual NuGet.org username that created the policy. This is the login/profile
name, not the organization name, an email address or a GitHub username unless
they happen to match. Selecting the organization as Package Owner gives it package
ownership while the individual account authenticates the policy. The variable is not
a secret. No long-lived NuGet API key is needed.

The workflow exchanges OIDC identity for a temporary NuGet key and publishes
`SchematicTech.Supertest.<version>.nupkg` plus its `.snupkg` symbols. The package contains
the .NET Standard 2.0 assembly, XML documentation, README, both licenses, and source
control metadata. Public source debugging resolves to the public squash commit.

Run `python scripts/package.py` with .NET SDK 8 installed. It tests on the current
platform, packs the library, and builds a separate consumer from a local NuGet feed.
CI also tests Windows. `DOTNET` can select an alternate dotnet executable locally.

Reference: [NuGet trusted publishing](https://learn.microsoft.com/en-us/nuget/nuget-org/trusted-publishing).
