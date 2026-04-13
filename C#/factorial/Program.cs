using System;

namespace Factorial
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.Write("Enter a positive integer: ");
            int num = Convert.ToInt32(Console.ReadLine());

            if(num < 0)
            {
                Console.WriteLine("Error: Please enter a positive number.");
            }

            long factorial = 1;
            for (int i = 1; i<=num; i++)
            {
                factorial *= i;
            }

            Console.WriteLine($"\n{num}! = {factorial}");
        }
    }
}