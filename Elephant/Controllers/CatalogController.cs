using Elephant.Models;
using Microsoft.AspNetCore.Mvc;
using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.IdentityModel.Tokens.Jwt;
using System.Linq;
using System.Net.Http;
using System.Threading.Tasks;

namespace Elephant.Controllers
{
    public class CatalogController : Controller
    {
        public async Task<IActionResult> Index(string id)
        {
            ViewData["JWT"] = Request.Cookies["auth"];
            var jwt = Request.Cookies["auth"];
            if (jwt != null)
            {
                var handler = new JwtSecurityTokenHandler();
                var token = handler.ReadJwtToken(jwt);
                ViewData["Role"] = token.Payload["role"];
            } else
            {
                ViewData["Role"] = null;
            }
            
            Console.WriteLine(ViewData["JWT"]);
            Console.WriteLine(ViewData["Role"]);
            if (id != null)
            {
                if (id != "NULL")
                {
                    ViewData["CatID"] = id;
                    using var client1 = new HttpClient();
                    var uri1 = new Uri("http://gateway:5003/api/user?endpoint=catalog&parameter=products&other_parameter=" + id);
                    var response1 = await client1.GetAsync(uri1);
                    string json1 = await response1.Content.ReadAsStringAsync();
                    var jsonResult1 = JsonConvert.DeserializeObject(json1).ToString();
                    var result1 = JsonConvert.DeserializeObject<CatalogResponse>(jsonResult1);
                    ViewData["CatalogProds"] = result1 ?? new CatalogResponse();
                    if (result1.ChildCategories.Count > 0)
                    {
                        List<CatalogResponse> prods = new();
                        foreach (var item in result1.ChildCategories)
                        {
                            var q = item.TryGetValue("Id", out string idcat);
                            using var client2 = new HttpClient();
                            var uri2 = new Uri("http://gateway:5003/api/user?endpoint=catalog&parameter=products&other_parameter=" + idcat);
                            var response2 = await client2.GetAsync(uri2);
                            string json2 = await response2.Content.ReadAsStringAsync();
                            var jsonResult2 = JsonConvert.DeserializeObject(json2).ToString();
                            var result2 = JsonConvert.DeserializeObject<CatalogResponse>(jsonResult2);
                            prods.Add(result2);
                        }
                        ViewData["Childs"] = prods;
                    }
                } else
                {
                    ViewData["CatID"] = id;
                    using var client1 = new HttpClient();
                    var uri1 = new Uri("http://gateway:5003/api/user?endpoint=catalog&parameter=products&other_parameter=" + id);
                    var response1 = await client1.GetAsync(uri1);
                    string json1 = await response1.Content.ReadAsStringAsync();
                    var jsonResult1 = JsonConvert.DeserializeObject(json1).ToString();
                    var result1 = JsonConvert.DeserializeObject<CatalogResponse>(jsonResult1);
                    ViewData["CatalogProds"] = result1 ?? new CatalogResponse();
                }
                
            }
            using (var client = new HttpClient())
            {
                var uri = new Uri("http://gateway:5003/api/user?endpoint=catalog&parameter=categories");
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
