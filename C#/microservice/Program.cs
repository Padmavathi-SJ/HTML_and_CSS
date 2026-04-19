using Microsoft.EntityFrameworkCore;
using microservice.Data;
using microservice.Services;
using microservice.Middleware;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddControllers();
builder.Services.AddDbContext<ApplicationDbContext>(options =>
    options.UseInMemoryDatabase("BooksDatabase"));
builder.Services.AddScoped<IBookService, BookService>();
builder.Services.AddLogging();

var app = builder.Build();

app.UseMiddleware<ExceptionMiddleware>();
app.UseHttpsRedirection();
app.UseAuthorization();
app.MapControllers();

using (var scope = app.Services.CreateScope())
{
    var context = scope.ServiceProvider.GetRequiredService<ApplicationDbContext>();
    if (!context.Books.Any())
    {
        context.Books.AddRange(
            new microservice.Models.Book { Title = "The Great Gatsby", Author = "F. Scott Fitzgerald", Year = 1925, Price = 12.99m },
            new microservice.Models.Book { Title = "To Kill a Mockingbird", Author = "Harper Lee", Year = 1960, Price = 14.99m },
            new microservice.Models.Book { Title = "1984", Author = "George Orwell", Year = 1949, Price = 11.99m }
        );
        context.SaveChanges();
    }
}

app.Run();