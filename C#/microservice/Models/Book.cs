using System.ComponentModel.DataAnnotations;

namespace microservice.Models
{
    public class Book
    {
        public int Id { get; set; }

        [Required]
        [StringLength(100)]
        public string? Title { get; set; }

        [Required]
        [StringLength(50)]
        public string? Author { get; set; }

        [Range(1000, 2024)]
        public int Year { get; set; }

        [Range(0, 1000)]
        public decimal Price { get; set; }
    }
}