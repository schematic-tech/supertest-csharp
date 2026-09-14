using System;

namespace Schematic
{
    /// <summary>Input-domain assumptions for Supertests.</summary>
    public static class Assumptions
    {
        /// <summary>Continues if true; otherwise exits the current process with status zero.</summary>
        /// <remarks>
        /// Run one input per process. A false assumption terminates all threads
        /// and does not execute finally blocks. It is not an assertion failure.
        /// </remarks>
        /// <param name="condition">Whether this input is in the admitted domain.</param>
        public static void Assume(bool condition)
        {
            if (!condition)
            {
                Environment.Exit(0);
            }
        }
    }
}
