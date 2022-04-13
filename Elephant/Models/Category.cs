using System;

namespace Elephant.Models
{
    public class Category
    {
        public Guid Id { get; set; }
        public string Name { get; set; }
        public string ParentId { get; set; }
    }
}
