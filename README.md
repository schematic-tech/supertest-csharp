# Supertest for C#

```sh
dotnet add package SchematicTech.Supertest
dotnet add package xunit.v3.assert
```

From the [text-tools example](examples/text-tools):

```csharp
using Schematic;
using Xunit;

namespace TextTools;

public static class CollapseSpaces
{
    [Supertest]
    public static void CollapsingSpacesAgainChangesNothing(string text)
    {
        string once = Text.CollapseSpaces(text);
        string twice = Text.CollapseSpaces(once);

        Assert.Equal(once, twice);
    }
}
```

See the [Getting Started Documentation](https://docs.schematic.tech/pup).

## Example

Try [text-tools](https://github.com/schematic-tech/supertest-csharp/tree/main/examples/text-tools), a space-normalization example with a supertest.

## License

This library is available under either MIT or Apache-2.0, at your option.
