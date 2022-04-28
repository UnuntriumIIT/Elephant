using System.Collections.Generic;

namespace Elephant.Models
{
    public class CartResponse
    {
        public string User_Id { get; set; }
        public string Total { get; set; }
        public List<CartProduct> Products { get; set; }
    }
}
