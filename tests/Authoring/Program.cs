using System.Diagnostics;
using System.Reflection;
using Schematic;
using static Schematic.Assumptions;

internal static class Program
{
    private static int calls;

    [Supertest]
    private static int MarkedFunction(int value)
    {
        calls++;
        return value + 1;
    }

    private static void Check(bool condition, string message)
    {
        if (!condition)
        {
            throw new InvalidOperationException(message);
        }
    }

    private static int NestedAssumption()
    {
        Assume(false);
        throw new InvalidOperationException("helper continued");
    }

    private static (int Status, string Output, string Error) RunProbe(string mode)
    {
        var start = new ProcessStartInfo(Environment.ProcessPath!)
        {
            RedirectStandardOutput = true,
            RedirectStandardError = true,
            UseShellExecute = false,
        };
        if (Path.GetFileNameWithoutExtension(start.FileName) == "dotnet")
        {
            start.ArgumentList.Add(typeof(Program).Assembly.Location);
        }
        start.ArgumentList.Add(mode);
        using var child = Process.Start(start)!;
        var output = child.StandardOutput.ReadToEndAsync();
        var error = child.StandardError.ReadToEndAsync();
        if (!child.WaitForExit(10_000))
        {
            child.Kill(entireProcessTree: true);
            throw new InvalidOperationException("runtime probe timed out");
        }
        return (child.ExitCode, output.GetAwaiter().GetResult(), error.GetAwaiter().GetResult());
    }

    private static int Main(string[] args)
    {
        if (args.Length != 0)
        {
            Console.WriteLine("entered");
            switch (args[0])
            {
                case "false":
                    try
                    {
                        _ = NestedAssumption();
                    }
                    catch (Exception)
                    {
                        Console.WriteLine("caught as failure");
                    }
                    Console.WriteLine("continued");
                    return 91;
                case "true":
                    var evaluations = 0;
                    Assume(++evaluations == 1);
                    Check(evaluations == 1, "condition evaluated more than once");
                    Console.WriteLine("continued");
                    return 0;
                case "assertion":
                    Assume(true);
                    Check(false, "ordinary assertion failure");
                    return 92;
                default:
                    return 64;
            }
        }

        var method = typeof(Program).GetMethod(nameof(MarkedFunction),
            BindingFlags.NonPublic | BindingFlags.Static)!;
        Check(method.GetCustomAttribute<SupertestAttribute>() != null, "missing marker");
        Check(calls == 0, "marker executed the method");
        Check(MarkedFunction(2) == 3 && calls == 1, "marker changed ordinary behavior");
        var usage = typeof(SupertestAttribute).GetCustomAttribute<AttributeUsageAttribute>()!;
        Check(usage.ValidOn == AttributeTargets.Method && !usage.AllowMultiple && !usage.Inherited,
            "marker must apply once to a method");

        var admitted = RunProbe("true");
        Check(admitted.Status == 0 && admitted.Output.Contains("continued"), "true assumption stopped");
        var rejected = RunProbe("false");
        Check(rejected.Status == 0, "false assumption failed: " + rejected.Error);
        Check(rejected.Output.Trim() == "entered" && rejected.Error == "", "false assumption continued");
        var failure = RunProbe("assertion");
        Check(failure.Status != 0 && failure.Error.Contains("ordinary assertion failure"),
            "ordinary failure was suppressed");
        Console.WriteLine("C# marker and assumption checks passed");
        return 0;
    }
}
