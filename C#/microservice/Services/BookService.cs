using Microsoft.EntityFrameworkCore;
using microservice.Models;
using microservice.Data;

namespace microservice.Services
{
    public class BookService : IBookService
    {
        private readonly ApplicationDbContext _context;
        
        public BookService(ApplicationDbContext context)
        {
            _context = context;
        }
        
        public async Task<List<Book>> GetAllBooksAsync()
        {
            return await _context.Books.ToListAsync();
        }
        
        public async Task<Book?> GetBookByIdAsync(int id)
        {
            return await _context.Books.FindAsync(id);
        }
        
        public async Task<Book> CreateBookAsync(Book book)
        {
            _context.Books.Add(book);
            await _context.SaveChangesAsync();
            return book;
        }
        
        public async Task<Book?> UpdateBookAsync(int id, Book book)
        {
            var existingBook = await _context.Books.FindAsync(id);
            if (existingBook == null)
                return null;
                
            existingBook.Title = book.Title;
            existingBook.Author = book.Author;
            existingBook.Year = book.Year;
            existingBook.Price = book.Price;
            
            await _context.SaveChangesAsync();
            return existingBook;
        }
        
        public async Task<bool> DeleteBookAsync(int id)
        {
            var book = await _context.Books.FindAsync(id);
            if (book == null)
                return false;
                
            _context.Books.Remove(book);
            await _context.SaveChangesAsync();
            return true;
        }
        
        public async Task<bool> BookExistsAsync(int id)
        {
            return await _context.Books.AnyAsync(b => b.Id == id);
        }
    }
}