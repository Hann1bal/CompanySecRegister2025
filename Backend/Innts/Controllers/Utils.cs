
using System.Collections;
using System.Collections.Concurrent;
using System.Reflection;

namespace Innts.Controllers.Utils;

[AttributeUsage(AttributeTargets.Property)]
public class IgnoreOnUpdateAttribute : Attribute { }

public static class EntityMapper
{
    public static TModel MapToEntity<TModel, TDto>(TDto dto, TModel entity)
        where TModel : class
    {
        var dtoProperties = typeof(TDto).GetProperties();

        foreach (var dtoProp in dtoProperties)
        {
            if (dtoProp.GetCustomAttribute<IgnoreOnUpdateAttribute>() != null)
                continue;

            var entityProp = typeof(TModel).GetProperty(dtoProp.Name);
            if (entityProp == null || !entityProp.CanWrite) continue;

            var value = dtoProp.GetValue(dto);
            if (!IsEmpty(value))
            {
                entityProp.SetValue(entity, value);
            }
        }

        return entity;
    }
    private static readonly ConcurrentDictionary<Type, object> _defaultValues = new();

    private static object GetDefaultValue(Type type)
    {
        return _defaultValues.GetOrAdd(type, t =>
            t.IsValueType ? Activator.CreateInstance(t) : null);
    }
    private static bool IsEmpty(object value)
    {
        return value switch
        {
            null => true,
            string s => string.IsNullOrWhiteSpace(s),
            ICollection c => c.Count == 0,
            IEnumerable e => !e.GetEnumerator().MoveNext(),
            _ => value.Equals(GetDefaultValue(value.GetType()))
        };
    }
}

