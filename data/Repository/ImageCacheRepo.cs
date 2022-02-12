using System;
using System.Collections.Generic;
using System.Linq;

namespace data.Repository
{
    public class ImageCacheRepo : ICacheRepo
    {
        private readonly UserContext _context;
        private readonly ICacheService _cache;

        public ImageCacheRepo(UserContext context, ICacheService cache)
        {
            _context = context;
            _cache = cache;
        }

        public Img GetSingle(Guid id)
        {/*
            var cached = _cache.Get<Img>(id.ToString());

            if (cached != null)
            {
                return cached;
            } else
            {
                var result = _context.Imgs.Find(id);
                return _cache.Set<Img>(id.ToString(), result);
            }*/
            return _context.Imgs.Find(id);
        }

        public void UpdateInCacheResize(Guid id)
        {
            var cached = _cache.Get<Img>(id.ToString());
            
            if (cached != null)
            {
                while (cached.ParentId == Guid.Parse("00000000-0000-0000-0000-000000000000"))
                {
                    cached = _cache.Get<Img>(id.ToString());
                    _cache.Set<Img>(id.ToString(), _context.Imgs.Find(id));
                }
            }
        }

        public Img[] GetAllByTag(string tag)
        {
            var ids = _context.Imgs.Where(t => t.SearchWord == tag).ToArray();
            var resultList = new List<Img>();
            foreach(var id in ids)
            {
                var cached = _cache.Get<Img>(id.ToString());
                if (cached != null)
                {
                    resultList.Add(cached);
                }
                else
                {
                    var result = _context.Imgs.Find(id);
                    resultList.Add(_cache.Set<Img>(id.ToString(), result));
                }
            }
            return resultList.ToArray();
        }

        public void Insert(Img img)
        {
            _context.Add(img);
            _cache.Set<Img>(img.Id.ToString(), img);
            _context.SaveChanges();
        }
    }
}
