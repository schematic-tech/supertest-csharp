# Supertest for C#

```sh
dotnet add package SchematicTech.Supertest
```

```csharp
using System;
using Schematic;
using static Schematic.Assumptions;

public static class Arithmetic
{
    [Supertest]
    public static void IntegerDivisionIsBounded(int value, int divisor)
    {
        Assume(value >= 0 && divisor > 0);
        if (value / divisor > value)
            throw new Exception("Quotient exceeded the dividend");
    }
}
```

See the [Getting Started Documentation](https://docs.schematic.tech/pup).

## License

This library is available under either MIT or Apache-2.0, at your option.
