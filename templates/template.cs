// BOJ 1000 C# 9.0 (.NET)
//출처: https://www.acmicpc.net/help/language 
using System;

namespace Baekjoon {
    class Program {
        static void Main() {
            string s = Console.ReadLine();
            string[] ss = s.Split();
            int a = int.Parse(ss[0]);
            int b = int.Parse(ss[1]);
            Console.WriteLine(a+b);
        }
    }
}