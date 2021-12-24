using data;
using System;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace services
{
    interface IDbService
    {
        void Add(Img img);

        Task<IEnumerable<Img>> GetAllAsync();

        Task<Img> GetByIdAsync(Guid id);

        Task RemoveAsync(Guid id);
    }
}
