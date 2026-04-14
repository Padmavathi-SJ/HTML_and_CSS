using System;
using System.Threading.Tasks;

namespace AsyncProgramming
{
    class Program
    {
        static async Task Main(string[] args)
        {
            // record start time
            DateTime start = DateTime.Now;

            // Slow way(one by one)
            await SlowWay();

            // fast way (all at once)
            await FastWay();

            Console.WriteLine($"\n Total time: {(DateTime.Now - start).Seconds} seconds");

        }

        // SLOW WAY(One by One)
        static async Task SlowWay()
        {
            try
            {
                string weather = await GetWeatherAsync();
                Console.WriteLine($" {weather}");

                string news = await GetNewsAsync();
                Console.WriteLine($" {news}");

                string stocks = await GetStockAsync();
                Console.WriteLine($" {stocks}");

                Console.WriteLine($"\n Total: 3+2+4 = 9 seconds");
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error: {ex.Message}");
            }
        }

        // FAST WAY (ALL at once)
        static async Task FastWay()
        {
            try
            {
                // start all tasks together (don't wait yet)
                Task<string> weatherTask = GetWeatherAsync();
                Task<string> newsTask = GetNewsAsync();
                Task<string> stocksTask = GetStockAsync();

                Console.WriteLine(" started al 3 tasks at once!");
                Console.WriteLine("They are running together in the background....");

                // Wait for All to finish
                await Task.WhenAll(weatherTask, newsTask, stocksTask);

                // show results
                Console.WriteLine("Results:");
                Console.WriteLine($" {weatherTask.Result}");
                Console.WriteLine($" {newsTask.Result}");
                Console.WriteLine($" {stocksTask.Result}");

                Console.WriteLine($" Total: Only 4 seconds (longest task!) ");
                Console.WriteLine("That's 5 seconds faster!");
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error in one or more tasks: {ex.Message}");
            }
        }

        // Simulated API Methods

        // Weather API - 3 seconds (always works)
        static async Task<string> GetWeatherAsync()
        {
            await Task.Delay(3000); // simulate 3 seconds delay
            return "Sunny, 75F";
        }

        // News API - 2 seconds (might fail 50% of the time){
        static async Task<string> GetNewsAsync()
        {
            await Task.Delay(2000);

            // Random failure to test error handling
            Random rand = new Random();
            if (rand.Next(0, 2) == 0)
              throw new Exception("News API is down!");

            return "C# Async is awesome!";
        }

        // stock API - 4 seconds (always works){
        static async Task<string> GetStockAsync()
        {
            await Task.Delay(4000);
            return "stocks rates in peak";
        }
    }
    }
    