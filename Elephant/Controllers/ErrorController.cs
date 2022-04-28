using Microsoft.AspNetCore.Mvc;
using System;
using System.Collections.Generic;
using System.IdentityModel.Tokens.Jwt;
using System.Linq;
using System.Threading.Tasks;

namespace Elephant.Controllers
{
    public class ErrorController : Controller
    {
        public IActionResult Not_found()
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
            return View();
        }

        public IActionResult Forbidden()
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
            return View();
        }
    }
}
