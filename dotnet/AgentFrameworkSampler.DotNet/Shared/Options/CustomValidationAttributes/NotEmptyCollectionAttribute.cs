namespace JCystems.AgentFrameworkSampler.DotNet.Shared.Options.CustomValidationAttributes
{

    using System.Collections;
    using System.ComponentModel.DataAnnotations;

    public class NotEmptyCollectionAttribute : ValidationAttribute
    {
        public NotEmptyCollectionAttribute() : base("The {0} field must not be empty.") { }

        public override bool IsValid(object value)
        {
            if (value == null)
            {
                // TODO? throw?
                return false; // A null collection is considered empty for this validation
            }

            if (value is ICollection collection)
            {
                return collection.Count > 0;
            }

            if (value is IEnumerable enumerable)
            {
                // Check if the enumerable has at least one element
                return enumerable.GetEnumerator().MoveNext();
            }

            return false; // Not a collection or enumerable
        }
    }
}
