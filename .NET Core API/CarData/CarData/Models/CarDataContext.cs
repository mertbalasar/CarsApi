using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.EntityFrameworkCore;

namespace CarData.Models
{
    public class CarDataContext : DbContext
    {
        public DbSet<CarData> CarDataTable { get; set; }

        public CarDataContext(DbContextOptions<CarDataContext> options) : base(options)
        {
        }

        protected override void OnModelCreating (ModelBuilder modelBuilder)
        {
            modelBuilder.Entity<CarData>().ToTable("cars");
        }
    }
}
