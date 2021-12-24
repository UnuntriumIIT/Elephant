using Microsoft.EntityFrameworkCore;

namespace data
{
    public class UserContext : DbContext
    {
        public DbSet<Img> Imgs { get; set; }

        public UserContext(DbContextOptions options) : base(options)
        {
        }

        protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
        {
            optionsBuilder.UseNpgsql("Server=postgres;Port=5432;Database=elephant;UserId=postgres;Password=admin;");
        }

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            modelBuilder.Entity<Img>(entity =>
            {
                entity.HasKey(e => e.Id);

                entity.Property(e => e.Id)
                    .HasColumnName("Id");

                entity.Property(e => e.Image)
                    .HasColumnName("Image")
                    .IsRequired();
            });
        }
    }
}
