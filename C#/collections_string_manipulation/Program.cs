using System;
using System.Collections.Generic;

namespace TaskManager
{
    class Program
    {
        static void Main(string[] args)
        {
            // Create a list to store tasks
            List<string> tasks = new List<string>();

            int choice;

            do
            {
                // Display menu
                Console.WriteLine("\n=== Task Manager ===");
                Console.WriteLine("1. Add Task");
                Console.WriteLine("2. Remove Task");
                Console.WriteLine("3. Show All Tasks");
                Console.WriteLine("4. Exit");
                Console.Write("Enter choice: ");

                choice = Convert.ToInt32(Console.ReadLine());

                switch(choice)
                {
                case 1:
                    // Add Task
                    Console.Write("Enter task: ");
                    string task = Console.ReadLine();
                    task = task.Trim();

                    if(task != "")
                        {
                            tasks.Add(task);
                            Console.WriteLine("Task Added!");
                        }
                    else
                        {
                            Console.WriteLine("Task cannot be empty!");
                        }
                    break;
                
                case 2:
                    // Remove Task
                    if (tasks.Count == 0)
                        {
                            Console.WriteLine("No tasks found to remove!");
                        }
                    else
                        {
                          // Show all tasks with numbers
                          Console.WriteLine("\nYour Tasks:");
                          for (int i=0; i < tasks.Count; i++)
                            {
                                Console.WriteLine($"{i + 1}. {tasks[i]}");
                            }  
                            Console.Write("Enter task number to remove: ");
                            int removeNum = Convert.ToInt32(Console.ReadLine());
                            int index = removeNum - 1;

                            if (index >= 0 && index < tasks.Count)
                            {
                                tasks.RemoveAt(index);
                                Console.WriteLine("Task Removed!");
                            }
                            else
                            {
                                Console.WriteLine("Invalid task number!");
                            }
                        }
                        break;

                case 3:
                    // Show All Tasks
                    if (tasks.Count == 0)
                        {
                            Console.WriteLine("No tasks found to display!");
                        }
                        else
                        {
                            Console.WriteLine("\n=== YOUR TASKS ===");
                            for(int i = 0; i<tasks.Count; i++)
                            {
                                Console.WriteLine($"{i + 1}. {tasks[i]}");
                            }
                            Console.WriteLine($"Total: {tasks.Count} tasks.");
                        }
                    break;
                
                case 4:
                Console.WriteLine("Goodbye!");
                break;

                default:
                Console.WriteLine("Invalid choice!");
                break;
            }
            
            }
            while (choice != 4);
            }


        }
}
