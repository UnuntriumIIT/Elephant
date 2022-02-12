﻿using data;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using System;
using System.IO;
using SixLabors.ImageSharp;
using data.Repository;

namespace Elephant.Controllers
{
    public class HomeController : Controller
    {
        private readonly ICacheRepo _repo;

        public HomeController(ICacheRepo repo)
        {
            _repo = repo;
        }

        [HttpGet]
        public IActionResult Index(string id)
        {
            if (id != "" && id != null)
            {
                return Redirect("/Home/Download/"+id);
            }
            return View();
        }

        [HttpPost]
        public IActionResult Index(IFormFile files, string tag)
        {
            if (files != null)
            {
                if (files.Length > 0)
                {
                    var inputImage = new Img()
                    {
                        Id = Guid.NewGuid(),
                        Image = null
                    };

                    var target = new MemoryStream();
                    files.CopyTo(target);
                    inputImage.Image = target.ToArray();

                    Image image = Image.Load(inputImage.Image);

                    ViewBag.ID = inputImage.Id;
                    ViewBag.ImageW = image.Width;
                    ViewBag.ImageH = image.Height;
                    ViewBag.ImageDataUrl = string.Format("data:image/jpg;base64,{0}", Convert.ToBase64String(inputImage.Image));
                    ViewBag.Tag = tag;

                    inputImage.SearchWord = tag;
                    inputImage.Width = image.Width;
                    inputImage.Height = image.Height;


                    _repo.Insert(inputImage);
                }
            }
            return View();
        }

        [HttpPost]
        public IActionResult Resize(Guid id, int width, int height)
        {

            return Redirect("http://127.0.0.1:5000/resize/" + id.ToString() + '/' + width.ToString() + '/' + height.ToString());
        }

        [HttpGet]
        public IActionResult Download(string id)
        {
            //_repo.UpdateInCacheResize(Guid.Parse(id));
            var img = _repo.GetSingle(Guid.Parse(id));
            var childImg = _repo.GetSingle(img.ParentId);/*
            Response.Clear();
            Response.Headers.Clear();
            Response.ContentType = "image/jpg";
            Response.Headers.Append("Content-Length", childImg.Image.Length.ToString());
            
            Response.Headers.Append("Connection", "close");
            Response.Body.WriteAsync(childImg.Image, 0, childImg.Image.Length);*/
            return File(childImg.Image, "image/jpg", img.SearchWord + ".jpg");
        }
    }   
}
