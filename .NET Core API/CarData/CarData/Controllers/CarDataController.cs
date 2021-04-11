using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using CarData.Models;

namespace CarData.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class CarDataController : ControllerBase
    {
        private readonly CarDataContext _context;

        public CarDataController(CarDataContext context)
        {
            _context = context;
        }

        // GET: api/CarData
        [HttpGet]
        public async Task<ActionResult<IEnumerable<Models.CarData>>> GetCarDataTable()
        {
            return await _context.CarDataTable.ToListAsync();
        }

        // GET: api/CarData/5
        [HttpGet("id={id}")]
        public async Task<ActionResult<Models.CarData>> GetCarDataWithId(int id)
        {
            Models.CarData carData = await _context.CarDataTable.FirstAsync(cd => cd.Id == id);
            if (carData == null) return NotFound();
            else return carData;
        }

        [HttpGet("brand={brand}")]
        public IQueryable<Models.CarData> GetCarDataWithBrand(string brand)
        {
            var carData = _context.CarDataTable.Where(cd => cd.Brand.ToLower().Contains(brand.ToLower()));
            return carData;
        }

        [HttpGet("yearUpLimit={yearUp}")]
        public IQueryable<Models.CarData> GetCarDataWithYearUp(int yearUp)
        {
            var carData = _context.CarDataTable.Where(cd => cd.Year <= yearUp);
            return carData;
        }

        [HttpGet("yearDownLimit={yearDown}")]
        public IQueryable<Models.CarData> GetCarDataWithYearDown(int yearDown)
        {
            var carData = _context.CarDataTable.Where(cd => cd.Year >= yearDown);
            return carData;
        }

        [HttpGet("priceUpLimit={priceUp}")]
        public IQueryable<Models.CarData> GetCarDataWithPriceUp(int priceUp)
        {
            var carData = _context.CarDataTable.Where(cd => cd.Price <= priceUp);
            return carData;
        }

        [HttpGet("priceDownLimit={priceDown}")]
        public IQueryable<Models.CarData> GetCarDataWithPriceDown(int priceDown)
        {
            var carData = _context.CarDataTable.Where(cd => cd.Price <= priceDown);
            return carData;
        }
        /*
        // PUT: api/CarData/5
        // To protect from overposting attacks, enable the specific properties you want to bind to, for
        // more details, see https://go.microsoft.com/fwlink/?linkid=2123754.
        [HttpPut("{id}")]
        public async Task<IActionResult> PutCarData(string id, Models.CarData carData)
        {
            if (id != carData.Currency)
            {
                return BadRequest();
            }

            _context.Entry(carData).State = EntityState.Modified;

            try
            {
                await _context.SaveChangesAsync();
            }
            catch (DbUpdateConcurrencyException)
            {
                if (!CarDataExists(id))
                {
                    return NotFound();
                }
                else
                {
                    throw;
                }
            }

            return NoContent();
        }

        // POST: api/CarData
        // To protect from overposting attacks, enable the specific properties you want to bind to, for
        // more details, see https://go.microsoft.com/fwlink/?linkid=2123754.
        [HttpPost]
        public async Task<ActionResult<Models.CarData>> PostCarData(Models.CarData carData)
        {
            _context.CarDataTable.Add(carData);
            try
            {
                await _context.SaveChangesAsync();
            }
            catch (DbUpdateException)
            {
                if (CarDataExists(carData.Currency))
                {
                    return Conflict();
                }
                else
                {
                    throw;
                }
            }

            return CreatedAtAction("GetCarData", new { id = carData.Currency }, carData);
        }

        // DELETE: api/CarData/5
        [HttpDelete("{id}")]
        public async Task<ActionResult<Models.CarData>> DeleteCarData(string id)
        {
            var carData = await _context.CarDataTable.FindAsync(id);
            if (carData == null)
            {
                return NotFound();
            }

            _context.CarDataTable.Remove(carData);
            await _context.SaveChangesAsync();

            return carData;
        }
        */
        private bool CarDataExists(string id)
        {
            return _context.CarDataTable.Any(e => e.Currency == id);
        }
    }
}
