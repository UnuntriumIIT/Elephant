using data;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using services;
using System;
using System.Drawing;
using System.IO;

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
        public IActionResult Index()
        {
            return View();
        }

        [HttpPost]
        public IActionResult Index(IFormFile files)
        {
            var idd = Guid.Empty;
            if (files != null)
            {
                if (files.Length > 0)
                {
                    var objfiles = new Img()
                    {
                        Id = Guid.NewGuid(),
                        Image = null
                    };

                    using (var target = new MemoryStream())
                    {
                        files.CopyTo(target);
                        objfiles.Image = target.ToArray();
                    }
                    idd = objfiles.Id;
                    _context.Imgs.Add(objfiles);
                    _context.SaveChanges();
                    Img img = _context.Imgs.Find(idd);
                    string imageBase64Data = Convert.ToBase64String(img.Image);
                    string imageDataURL = string.Format("data:image/jpg;base64,{0}", imageBase64Data);
                    ViewBag.ImageDataUrl = imageDataURL;
                    ViewBag.ImgId = idd;
                }
            }
            return View();
        }
    }   
}
