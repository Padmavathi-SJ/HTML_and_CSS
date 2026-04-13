using System;
using System.Collections.Generic;

namespace PersonOOP
{
    class Person
    {
        // Properties (auto-implemented)
        public string Name { get; set; }
        public int Age { get; set; }

        // onstructor (special method that runs when object is created)
        public Person()
        {
            Name = "Unknown";
            Age = 0;
        }

        // Parameterized constructor to initialize properties
        public Person(string name, int age)
        {
            Name = name;
            Age = age;
        }

        // Method to introduce the person
        public void Introduce()
        {
            Console.WriteLine($"Hello! My name is {Name} and I am {Age} years old.");

            if (Age < 18)
            {
                Console.WriteLine($" I'm a young student!");
            }
            else if (Age >= 18 && Age < 60)
            {
                Console.WriteLine($" I'm an adult.");
            }
            else
            {
                Console.WriteLine($" I'm a senior citizen!");
            }
        }

        // Method to display person details
        public void DisplayInfo()
        {
            Console.WriteLine($"Name: {Name}, Age: {Age}");
        }

        //Method to check if person is adult
        public bool IsAdult()
        {
            return Age >= 18;
        }

        // Method to celebrate birthday (increases age by 1)
        public void HaveBirthday()
        {
            Age++;
            Console.WriteLine($"Happy Birthday {Name}! You are now {Age} years old");
        }
    }

    class Program
    {
        static void Main(string[] args)
        {
           // Method 1: Create person using default constructor
           Person person1 = new Person();
           person1.Name = "smitha";
           person1.Age = 25;

           //Method 2: Create person using parameterized constructor
           Person person2 = new Person("Padma", 30);

           // Method 3: Create person using object initializer syntax
           Person person3 = new Person
           {
               Name = "Ravi",
               Age = 15
           };

           // Create a list of persons
           List<Person> people = new List<Person>();
           people.Add(person1);
           people.Add(person2);
           people.Add(person3);

           // Add more persons
           people.Add(new Person("Anitha", 45));
           people.Add(new Person("Suresh", 65));

           // Call Introduce() method on each person
           Console.WriteLine("=== Introductions ===\n");
           foreach (Person person in people)
            {
                person.Introduce();
                Console.WriteLine();
            }

            //Additional Information 
           foreach (Person person in people)
            {
                Console.Write($"{person.Name} is ");
                if(person.IsAdult())
                    Console.WriteLine("an adult.");
                else
                    Console.WriteLine("a minor.");
            }

            //Birthday celebration 
            Console.WriteLine("\n=== Birthday Celebration ===\n");
            Person birthdayPerson = people[0];
            Console.WriteLine($"Before Birthday: {birthdayPerson.Name} is {birthdayPerson.Age} years old");
            birthdayPerson.HaveBirthday();

    

        }
    }
}