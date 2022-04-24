using Microsoft.AspNetCore.Mvc;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace Elephant.Controllers
{
    public class ErrorController : Controller
    {
        public IActionResult Not_found()
        {
            return View();
        }

        public IActionResult Forbidden()
        {
            return View();
        }
    }
}
