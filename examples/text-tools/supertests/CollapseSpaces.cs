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
