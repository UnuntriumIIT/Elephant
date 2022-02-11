using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace data.Repository
{
    public interface ICacheRepo
    {
        Img GetSingle(Guid id);
        Img[] GetAllByTag(string tag);
        void Insert(Img img);
    }
}
