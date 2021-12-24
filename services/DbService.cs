using data;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace services
{
    public class DbService : IDbService
    {
        private readonly UserContext _context;

        public DbService(UserContext context)
        {
            _context = context;
        }

        public void Add(Img img)
        {
            _context.Imgs.Add(img);
            _context.SaveChanges();
        }

        public async Task<IEnumerable<Img>> GetAllAsync()
        {
            IEnumerable<Img> result = _context.Imgs.ToList();
            return await Task.FromResult(result);
        }

        public async Task<Img> GetByIdAsync(Guid id)
        {
            Img img = _context.Imgs.SingleOrDefault(x => x.Id == id);
            return await Task.FromResult(img);
        }

        public async Task RemoveAsync(Guid id)
        {
            Img img = _context.Imgs.SingleOrDefault(x => x.Id == id);

            if (img != null)
            {
                _context.Imgs.Remove(img);
                await _context.SaveChangesAsync();
            }
        }
    }
}
