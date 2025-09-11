// This file is used by Code Analysis to maintain SuppressMessage
// attributes that are applied to this project.
// Project-level suppressions either have no target or are given
// a specific target and scoped to a namespace, type, member, etc.

using System.Diagnostics.CodeAnalysis;

[assembly: SuppressMessage(
    "StyleCop.CSharp.DocumentationRules",
    "SA1600:Elements should be documented",
    Scope = "module",
    Justification = "Too noisy")]

[assembly: SuppressMessage(
    "StyleCop.CSharp.LayoutRules",
    "SA1512:Single-line comments should not be followed by blank line",
    Scope = "module",
    Justification = "Readability is KING")]

[assembly: SuppressMessage(
    "StyleCop.CSharp.LayoutRules",
    "SA1507:Code should not contain multiple blank lines in a row",
    Scope = "module",
    Justification = "Readability is KING")]

[assembly: SuppressMessage(
    "StyleCop.CSharp.OrderingRules",
    "SA1201:Elements should appear in the correct order",
    Scope = "module",
    Justification = "Self documented code When properties and fields go together")]

[assembly: SuppressMessage(
    "StyleCop.CSharp.LayoutRules",
    "SA1515:Single-line comment should be preceded by blank line",
    Scope = "module",
    Justification = "Sometimes comments should go right after code")]

[assembly: SuppressMessage(
    "StyleCop.CSharp.LayoutRules",
    "SA1516:Elements should be separated by blank line",
    Scope = "module",
    Justification = "Self documented code When properties and fields go together")]

[assembly: SuppressMessage(
    "StyleCop.CSharp.OrderingRules",
    "SA1212:Property accessors should follow order",
    Scope = "module",
    Justification = "Things are 'set'ted before they are 'get'ted")]
