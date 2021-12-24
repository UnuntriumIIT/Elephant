using System;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace DataAPI
{
    [Table("Img")]
    public class Img
    {
        [DatabaseGenerated(DatabaseGeneratedOption.Identity)]
        public Guid Id { get; set; }

        [Required]
        public byte[] Image { get; set; }

        [ForeignKey("User")]
        [Required]
        public Guid UserId { get; set; }
    }
}
