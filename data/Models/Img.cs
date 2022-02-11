using System;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace data
{
    [Table("Img")]
    public class Img
    {
        [DatabaseGenerated(DatabaseGeneratedOption.Identity)]
        public Guid Id { get; set; }

        [Required]
        public byte[] Image { get; set; }

        public string SearchWord { get; set; }
        public int Width { get; set; }
        public int Height { get; set; }
        public Guid ParentId { get; set; }
    }
}
