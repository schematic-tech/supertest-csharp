# Text tools

This is the C# version of the example in [Welcome to Super](https://docs.schematic.tech/super/).
It deliberately contains a bug: replacing pairs of spaces once does not collapse
a run of three spaces. The supertest checks that collapsing spaces again
leaves the result unchanged.

## Set up

With the .NET 8 SDK installed, run from the repository root:

```sh
cd examples/text-tools
dotnet build -c Release
```

The example uses the supertest library from this checkout.

## Check and fix

[Install the Super CLI and log in](https://docs.schematic.tech/super/get-started/), then run
from this example directory:

```sh
super link .
super check .
```

The CLI links the containing `supertest-csharp` repository. The `.` in `super check .`
selects only this example.

The check should fail. For example, `"a   b"` becomes `"a  b"` on the first call
and `"a b"` on the second. Super may find a different counterexample.

Review and apply the proposed fix, then check again:

```sh
super fix
super check .
```

The CLI asks before applying the fix and whether to include uncommitted changes.
