using Microsoft.AspNetCore.Mvc;
using System;
using System.Collections.Generic;
using System.Linq;
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
                var uri = new Uri("http://admin_api:5000/api/categories");
                var response = await client.GetAsync(uri);
                string textResult = await response.Content.ReadAsStringAsync();
            }
            return View();
        }

        public IActionResult AddCategory()
        {
            return View();
        }
    }
}
