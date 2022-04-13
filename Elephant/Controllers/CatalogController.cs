using Elephant.Models;
using Microsoft.AspNetCore.Mvc;
using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Http;
using System.Threading.Tasks;

namespace Elephant.Controllers
{
    public class CatalogController : Controller
    {
        public async Task<IActionResult> Index(string id)
        {
            if (id != null)
            {
                ViewData["CatID"] = id;
                using var client1 = new HttpClient();
                var uri1 = new Uri("http://catalog_api:5001/api/catalog/products/" + id);
                var response1 = await client1.GetAsync(uri1);
                string json1 = await response1.Content.ReadAsStringAsync();
                var jsonResult1 = JsonConvert.DeserializeObject(json1).ToString();
                var result1 = JsonConvert.DeserializeObject<CatalogResponse>(jsonResult1);
                ViewData["CatalogProds"] = result1 ?? new CatalogResponse();
                if (result1.ChildCategories.Count > 0)
                {
                    List<CatalogResponse> prods = new();
                    foreach(var item in result1.ChildCategories)
                    {
                        var q = item.TryGetValue("Id", out string idcat);
                        using var client2 = new HttpClient();
                        var uri2 = new Uri("http://catalog_api:5001/api/catalog/products/" + idcat);
                        var response2 = await client2.GetAsync(uri2);
                        string json2 = await response2.Content.ReadAsStringAsync();
                        var jsonResult2 = JsonConvert.DeserializeObject(json2).ToString();
                        var result2 = JsonConvert.DeserializeObject<CatalogResponse>(jsonResult2);
                        prods.Add(result2);
                    }
                    ViewData["Childs"] = prods;
                }
            }
            using (var client = new HttpClient())
            {
                var uri = new Uri("http://catalog_api:5001/api/catalog/categories");
                var response = await client.GetAsync(uri);
                string json = await response.Content.ReadAsStringAsync();
                var jsonResult = JsonConvert.DeserializeObject(json).ToString();
                var result = JsonConvert.DeserializeObject<List<Category>>(jsonResult);
                ViewData["CatalogCats"] = result ?? new List<Category>();
            }
            return View();
        }
    }
}
