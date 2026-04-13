using System;
using System.IO;

namespace FileIOExceptionHandling
{
    class Program
    {
        static void Main(string[] args)
        {
            string inputFile = "input.txt";
            string outputFile = "output.txt";

            try
            {
                // Read from input file
                if (!File.Exists(inputFile))
                {
                    Console.WriteLine("No input file found. Creating sample file....");
                    CreateSampleFile(inputFile);
                }

                Console.WriteLine($"Reading: {inputFile}");
                string content = File.ReadAllText(inputFile);

                // Process Data(count words, lines, characters)
                int lineCount = CountLines(content);
                int wordCount = CountWords(content);
                int charCount = content.Length;

                // Display Results
                Console.WriteLine("\n--- Results ---");
                Console.WriteLine($"Lines: {lineCount}");
                Console.WriteLine($"Words: {wordCount}");
                Console.WriteLine($"Characters: {charCount}");

                // Write to new file
                string report = $"File Reports\n";
                report += $"Date: {DateTime.Now}\n";
                report += $"Lines: {lineCount}\n";
                report += $"Words: {wordCount}\n";
                report += $"Characters: {charCount}\n";

                File.WriteAllText(outputFile, report);
                Console.WriteLine($"\n Results save to: {outputFile}");
            }
            catch (FileNotFoundException)
            {
                Console.WriteLine("Error: File not found!");
            }
            catch (IOException)
            {
                Console.WriteLine("Error: Cannot read/write file. It might be in use.");
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error: {ex.Message}");
            }
            
        }

        // Create a sample file with dummy content
        static void CreateSampleFile(string fileName)
        {
            string text = "Hello world! this is sample text file.\n";
            text += "C# programming is very fun and powerful too.\n";
            text += "Its very easy to learn and work with files in C#.\n";
            text += "Exception Handling makes our programs robust.\n";
            text += "Practice makes perfect! keep learning and, \n";
            text += "Do something great every day!";

            File.WriteAllText(fileName, text);
            Console.WriteLine("Sample file created\n");
        }

        // Count lines in text
        static int CountLines(string text)
        {
            if(string.IsNullOrEmpty(text))
            return 0;

            string[] lines = text.Split('\n');
            return lines.Length;
        }

        // Count words in text
        static int CountWords(string text)
        {
            if(string.IsNullOrEmpty(text))
            return 0;

            // Split by spaces, new lines, and punctuation
            char[] separators = { ' ', '\n', '\r', '.', ',', '!', '?', ':', ';'};
            string[] words = text.Split(separators, StringSplitOptions.RemoveEmptyEntries);
            return words.Length;
        }
    }
}