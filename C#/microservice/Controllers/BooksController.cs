using Microsoft.AspNetCore.Mvc;
using microservice.Models;
using microservice.Services;
using Microsoft.Extensions.Logging;

namespace microservice.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class BooksController : ControllerBase
    {
        private readonly IBookService _bookService;
        private readonly ILogger<BooksController> _logger;

        public BooksController(IBookService bookService, ILogger<BooksController> logger)
        {
            _bookService = bookService;
            _logger = logger;
        }

        [HttpGet]
        public async Task<ActionResult<IEnumerable<Book>>> GetBooks()
        {
            try
            {
                var books = await _bookService.GetAllBooksAsync();
                _logger.LogInformation($"Retrieved {books.Count} books.");
                return Ok(books);
            }
            catch(Exception ex)
            {
                _logger.LogError($"Error getting books: {ex.Message}");
                return StatusCode(500, "Internal server error");
            }
        }

        [HttpGet("{id}")]
        public async Task<ActionResult<Book>> GetBook(int id)
        {
            try
            {
                var book = await _bookService.GetBookByIdAsync(id);

                if (book == null)
                {
                    _logger.LogWarning($"Book with ID {id} not found");
                    return NotFound($"Book with ID {id} not found");
                }
                return Ok(book);
            }
            catch(Exception ex)
            {
                _logger.LogError($"Error getting book {id}: {ex.Message}");
                return StatusCode(500, "Internal server error");
            }
        }

        [HttpPost]
        public async Task<ActionResult<Book>> CreateBook(Book book)
        {
            try
            {
                if (!ModelState.IsValid)
                {
                    return BadRequest(ModelState);
                }

                var createdBook = await _bookService.CreateBookAsync(book);
                _logger.LogInformation($"Created new book with ID {createdBook.Id}");
                return CreatedAtAction(nameof(GetBook), new { id = createdBook.Id}, createdBook);
            }
            catch(Exception ex)
            {
                _logger.LogError($"Error creating book: {ex.Message}");
                return StatusCode(500, "Internal server error");
            }
        }

        [HttpPut("{id}")]
        public async Task<IActionResult> UpdateBook(int id, Book book)
        {
            try
            {
                if (id != book.Id)
                {
                    return BadRequest("ID mismatch");
                }
                if (!ModelState.IsValid)
                {
                    return BadRequest(ModelState);
                }

                var updatedBook = await _bookService.UpdateBookAsync(id, book);

                if(updatedBook == null)
                {
                    _logger.LogWarning($"Book with ID {id} not found for update");
                    return NotFound($"Book with ID {id} not found");
                }

                _logger.LogInformation($"Updated book with ID {id}");
                return Ok(updatedBook);
            }
            catch (Exception ex)
            {
                _logger.LogError($"Error updating book {id}: {ex.Message}");
                return StatusCode(500, "Internal server error");
            }
        }

        [HttpDelete("{id}")]
        public async Task<IActionResult> DeleteBook(int id)
        {
            try
            {
                var result = await _bookService.DeleteBookAsync(id);

                if (!result)
                {
                    _logger.LogWarning($"Book with ID {id} not found for deletion");
                    return NotFound($"Book with ID {id} not found");
                }

                _logger.LogInformation($"Deleted book with ID {id}");
                return NoContent();
            }
            catch(Exception ex)
            {
                _logger.LogError($"Error deleting book {id}: {ex.Message}");
                return StatusCode(500, "Internal server error");
            }
        }
    }
}