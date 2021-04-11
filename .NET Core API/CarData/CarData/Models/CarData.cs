using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace CarData.Models
{
    public class CarData
    {
        public int Id { get; set; }
        public string Brand { get; set; }
        public string Model { get; set; }
        public int Year { get; set; }
        public string Package { get; set; }
        public float Price { get; set; }
        public string Currency { get; set; }
    }
}
