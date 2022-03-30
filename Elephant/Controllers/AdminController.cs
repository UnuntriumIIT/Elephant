using Microsoft.AspNetCore.Mvc;
using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using Elephant.Models;
using System.Net.Http;
using System.Threading.Tasks;

namespace Elephant.Controllers
{
    public class AdminController : Controller
    {
        public IActionResult Index()
        {
            return View();
        }

        public IActionResult Catalog()
        {
            return View();
        }

        public async Task<IActionResult> Categories()
        {
            using (var client = new HttpClient())
            {
                var uri = new Uri("http://admin_api:5000/api/category");
                var response = await client.GetAsync(uri);
                string json = await response.Content.ReadAsStringAsync();
                var jsonResult = JsonConvert.DeserializeObject(json).ToString();
                var result = JsonConvert.DeserializeObject<List<Category>>(jsonResult);
                ViewData["categories"] = result;
            }
            return View();
        }

        public IActionResult AddCategory()
        {
            ViewData["UUID"] = Guid.NewGuid().ToString();
            return View();
        }

        public async Task<IActionResult> EditCategory(string id)
        {
            using (var client = new HttpClient())
            {
                var uri = new Uri("http://admin_api:5000/api/category/"+id);
                var response = await client.GetAsync(uri);
                string json = await response.Content.ReadAsStringAsync();
                var jsonResult = JsonConvert.DeserializeObject(json).ToString();
                var result = JsonConvert.DeserializeObject<List<Category>>(jsonResult);
                ViewData["CategoryID"] = result[0].Id;
                ViewData["CategoryName"] = result[0].Name;
            }
            return View();
        }

        public async Task<IActionResult> DeleteCategory(string id)
        {
            using (var client = new HttpClient())
            {
                var uri = new Uri("http://admin_api:5000/api/category/" + id);
                await client.DeleteAsync(uri);
            }
            return Redirect("/admin/categories");
        }
    }
}
