using Microsoft.EntityFrameworkCore;
using microservice.Models;

namespace microservice.Data
{
    public class ApplicationDbContext : DbContext
    {
        public ApplicationDbContext(DbContextOptions<ApplicationDbContext> options)
            : base(options)
        {
        }
        
        public DbSet<Book> Books { get; set; }
    }
}