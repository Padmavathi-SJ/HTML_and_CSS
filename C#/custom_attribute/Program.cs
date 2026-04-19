using System;
using System.Reflection;

namespace ReflectionDemo
{
    // 1. create the custom attribute
    [AttributeUsage(AttributeTargets.Method)]
    class RunnableAttribute :  Attribute
    {
        
    }

    // 2. create some classes with runnable methods
    class Animal
    {
        [Runnable]
        public void Dog()
        {
            Console.WriteLine("Woof! Woof!");
        }

        [Runnable]
        public void Cat()
        {
            Console.WriteLine("Meow! Meow!");
        }

        public void Bird()
        {
            Console.WriteLine("Chirp! Chirp!");
        }
    }

    class Sports
    {
        [Runnable]
        public void Cricket()
        {
            Console.WriteLine("Playing Cricket! ");
        }

        [Runnable]
        public void Football()
        {
            Console.WriteLine("Playing Football! ");
        }
    }

    class Program
    {
        static void Main()
        {
            Console.WriteLine("===Finding and Running Methods with [Runnable] ===\n");

            // 3. Get the current assembly
            Assembly assembly = Assembly.GetExecutingAssembly();

            // 4. Get all types
            Type[] allTypes = assembly.GetTypes();

            // 5. Loop through each type
            foreach (Type type in allTypes)
            {
                // skip the attribute and Program classes
                if (type.Name == "RunnableAttribute" || type.Name == "Program")
                continue;

                Console.WriteLine($"Class: {type.Name}");

                //create an object of this class
                object obj = Activator.CreateInstance(type);

                // Get all methods of this class
                MethodInfo[] methods = type.GetMethods();

                //check each method
                foreach (MethodInfo method in methods)
                {
                    //check if method has [Runnable] attribute
                    if (method.IsDefined(typeof(RunnableAttribute), false))
                    {
                        Console.Write($" -< Running {method.Name}(): ");
                        method.Invoke(obj, null); //Run the method
                    }
                }
                Console.WriteLine();
            }

        }
    }
}