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
    public class CartController : Controller
    {
        public async Task<IActionResult> Index()
        {
            ViewData["JWT"] = Request.Cookies["auth"];
            var jwt = Request.Cookies["auth"];
            if (jwt != null)
            {
                var handler = new JwtSecurityTokenHandler();
                var token = handler.ReadJwtToken(jwt);
                ViewData["Role"] = token.Payload["role"];
            }
            else
            {
                ViewData["Role"] = null;
            }
            using (var client = new HttpClient(new HttpClientHandler { AllowAutoRedirect = false, UseCookies = false }))
            {
                var uri = new Uri("http://gateway:5003/api/cart?token=" + Request.Cookies["auth"]);
                var response = await client.GetAsync(uri);
                string json = await response.Content.ReadAsStringAsync();
                if (json != "null\n") 
                {
                    var jsonResult = JsonConvert.DeserializeObject(json).ToString();
                    var result = JsonConvert.DeserializeObject<CartResponse>(jsonResult);
                    if (result != null)
                    {
                        ViewData["CartProducts"] = result.Products ?? new List<CartProduct>();
                        ViewData["Total"] = result.Total;
                    }
                }
                else
                {
                    ViewData["Total"] = 0;
                }
            }
            return View();
        }

        public async Task<IActionResult> Plus(string Id, string pathToRedirect)
        {
            using (var client = new HttpClient(new HttpClientHandler { AllowAutoRedirect = false, UseCookies = false }))
            {
                var uri = new Uri("http://gateway:5003/api/cart?parameter="+Id+"&token=" + Request.Cookies["auth"]);
                await client.PostAsync(uri, new StringContent(""));
            }
            return Redirect(pathToRedirect);
        }

        public async Task<IActionResult> Remove(string Id)
        {
            using (var client = new HttpClient(new HttpClientHandler { AllowAutoRedirect = false, UseCookies = false }))
            {
                var uri = new Uri("http://gateway:5003/api/cart?endpoint=deleteall&parameter=" + Id + "&token=" + Request.Cookies["auth"]);
                await client.DeleteAsync(uri);
            }
            return Redirect("/cart");
        }

        public async Task<IActionResult> Minus(string Id)
        {
            using (var client = new HttpClient(new HttpClientHandler { AllowAutoRedirect = false, UseCookies = false }))
            {
                var uri = new Uri("http://gateway:5003/api/cart?parameter=" + Id + "&token=" + Request.Cookies["auth"]);
                await client.DeleteAsync(uri);
            }
            return Redirect("/cart");
        }
    }
}
