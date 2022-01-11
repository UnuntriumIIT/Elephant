using data;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using System;
using System.IO;
using SixLabors.ImageSharp;

namespace Elephant.Controllers
{
    public class HomeController : Controller
    {
        private readonly UserContext _context;

        public HomeController(UserContext context)
        {
            _context = context;
        }

        [HttpGet]
        public IActionResult Index(Guid id, int w, int h)
        {
            if (id == Guid.Empty)
            {

            }
            return View();
        }

        [HttpPost]
        public IActionResult Index(IFormFile files)
        {
            if (files != null)
            {
                if (files.Length > 0)
                {
                    var objfiles = new Img()
                    {
                        Id = Guid.NewGuid(),
                        Image = null
                    };

                    var target = new MemoryStream();
                    files.CopyTo(target);
                    objfiles.Image = target.ToArray();

                    _context.Imgs.Add(objfiles);
                    _context.SaveChanges();

                    Image image = Image.Load(objfiles.Image);
                    
                    ViewBag.ImageW = image.Width;
                    ViewBag.ImageH = image.Height;
                    ViewBag.ImageDataUrl = string.Format("data:image/jpg;base64,{0}", Convert.ToBase64String(objfiles.Image));
                }
            }
            return View();
        }
    }   
}
