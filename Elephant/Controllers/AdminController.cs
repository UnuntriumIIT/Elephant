using Microsoft.AspNetCore.Mvc;
using Newtonsoft.Json;
using System;
using System.Linq;
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

        public async Task<IActionResult> Catalog()
        {
            using (var client = new HttpClient())
            {
                var uri = new Uri("http://admin_api:5000/api/catalog");
                var response = await client.GetAsync(uri);
                string json = await response.Content.ReadAsStringAsync();
                var jsonResult = JsonConvert.DeserializeObject(json).ToString();
                var result = JsonConvert.DeserializeObject<List<Product>>(jsonResult);
                ViewData["products"] = result ?? new List<Product>();

                var uri1 = new Uri("http://admin_api:5000/api/category");
                var response1 = await client.GetAsync(uri1);
                string json1 = await response1.Content.ReadAsStringAsync();
                var jsonResult1 = JsonConvert.DeserializeObject(json1).ToString();
                var result1 = JsonConvert.DeserializeObject<List<Category>>(jsonResult1);
                ViewData["categoriesAssign"] = result1 ?? new List<Category>();
            }
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
                ViewData["categories"] = result ?? new List<Category>();
            }
            return View();
        }

        public async Task<IActionResult> AddCategory()
        {
            ViewData["UUID"] = Guid.NewGuid().ToString();
            using (var client = new HttpClient())
            {
                var uri = new Uri("http://admin_api:5000/api/category");
                var response = await client.GetAsync(uri);
                string json = await response.Content.ReadAsStringAsync();
                var jsonResult = JsonConvert.DeserializeObject(json).ToString();
                var result = JsonConvert.DeserializeObject<List<Category>>(jsonResult);
                ViewData["catsForChilds"] = result ?? new List<Category>();
            }
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
                ViewData["ParentID"] = result[0].ParentId;

                var uri2 = new Uri("http://admin_api:5000/api/category");
                var response2 = await client.GetAsync(uri2);
                string json2 = await response2.Content.ReadAsStringAsync();
                var jsonResult2 = JsonConvert.DeserializeObject(json2).ToString();
                var result2 = JsonConvert.DeserializeObject<List<Category>>(jsonResult2);
                ViewData["catsForChilds"] = result2 ?? new List<Category>();

                var uri1 = new Uri("http://admin_api:5000/api/categorychilds/" + id);
                var response1 = await client.GetAsync(uri1);
                string json1 = await response1.Content.ReadAsStringAsync();
                var jsonResult1 = JsonConvert.DeserializeObject(json1).ToString();
                var result1 = JsonConvert.DeserializeObject<List<Category>>(jsonResult1);
                ViewData["child_categories"] = result1 ?? new List<Category>();
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

        public async Task<IActionResult> AddProduct()
        {
            ViewData["UUIDp"] = Guid.NewGuid().ToString();
            using (var client = new HttpClient())
            {
                var uri = new Uri("http://admin_api:5000/api/category");
                var response = await client.GetAsync(uri);
                string json = await response.Content.ReadAsStringAsync();
                var jsonResult = JsonConvert.DeserializeObject(json).ToString();
                var result = JsonConvert.DeserializeObject<List<Category>>(jsonResult);
                ViewData["catsForProducts"] = result ?? new List<Category>();
            }
            return View();
        }

        public async Task<IActionResult> DeleteProduct(string id)
        {
            using (var client = new HttpClient())
            {
                var uri = new Uri("http://admin_api:5000/api/catalog/" + id);
                await client.DeleteAsync(uri);
            }
            return Redirect("/admin/catalog");
        }

        public async Task<IActionResult> EditProduct(string id)
        {
            using (var client = new HttpClient())
            {
                var uri = new Uri("http://admin_api:5000/api/catalog/" + id);
                var response = await client.GetAsync(uri);
                string json = await response.Content.ReadAsStringAsync();
                var jsonResult = JsonConvert.DeserializeObject(json).ToString();
                var result = JsonConvert.DeserializeObject<List<Product>>(jsonResult);
                ViewData["ProductId"] = result.Where(a => a.Id.ToString() == id).First().Id;
                ViewData["ProductName"] = result.Where(a => a.Id.ToString() == id).First().Name;
                ViewData["ProductImgSrc"] = result.Where(a => a.Id.ToString() == id).First().Image_src;
                ViewData["ProductPrice"] = result.Where(a => a.Id.ToString() == id).First().Price;
                ViewData["ProductQuantity"] = result.Where(a => a.Id.ToString() == id).First().Quantity;
                ViewData["ProductCategoryId"] = result.Where(a => a.Id.ToString() == id).First().Category_id;

                var uri1 = new Uri("http://admin_api:5000/api/category");
                var response1 = await client.GetAsync(uri1);
                string json1 = await response1.Content.ReadAsStringAsync();
                var jsonResult1 = JsonConvert.DeserializeObject(json1).ToString();
                var result1 = JsonConvert.DeserializeObject<List<Category>>(jsonResult1);
                ViewData["catsForProducts"] = result1 ?? new List<Category>();
            }
            return View();
        }
    }
}
