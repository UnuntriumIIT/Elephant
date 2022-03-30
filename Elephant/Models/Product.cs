using System;

namespace Elephant.Models
{
    public class Product
    {
        public Guid Id { get; set; }
        public string Name { get; set; }
        public string Image_src { get; set; }
        public decimal Price { get; set; }
        public int Quantity { get; set; }
        public string Category_id { get; set; }
    }
}
