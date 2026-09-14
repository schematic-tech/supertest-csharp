using System;

namespace Schematic
{
    /// <summary>Marks a method as a Supertest without executing or wrapping it.</summary>
    [AttributeUsage(AttributeTargets.Method, AllowMultiple = false, Inherited = false)]
    public sealed class SupertestAttribute : Attribute
    {
    }
}
