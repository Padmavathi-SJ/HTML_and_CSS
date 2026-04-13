using System;

namespace PersonalInfo
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.Write("Enter your name: ");
            string name = Console.ReadLine();

            Console.Write("Enter your age: ");
            int age = Convert.ToInt32(Console.ReadLine());

            Console.Write("Enter your City: ");
            string city = Console.ReadLine();

            Console.WriteLine("\n=== Your profile ===");
            Console.WriteLine("Name: " + name);
            Console.WriteLine("Age: " + age);
            Console.WriteLine("City: " + city);
            
            if (age <= 18)
            {
                Console.WriteLine("\nYou are eligible to Vote.");

            }
            else
            {
                Console.WriteLine("\nYou are not eligible to Vote.");
            }
        }
    }
}