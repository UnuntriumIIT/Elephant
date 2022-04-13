using System;
using System.Collections.Generic;

namespace Elephant.Models
{
    public class CatalogResponse
    {
        public Guid Id { get; set; }
        public string Name { get; set; }
        public List<Dictionary<string, string>> ChildCategories { get; set; }
        public List<Dictionary<string, string>> Products { get; set; }
    }
}
