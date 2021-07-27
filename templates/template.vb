' BOJ 1000 C# 9.0 (.NET)
' 출처: https://www.acmicpc.net/help/language 
Module Main
 
  Sub Main()
    Dim s() As String = Nothing
 
    s = Console.ReadLine().Split(" "c)
    Console.WriteLine(CInt(s(0)) + CInt(s(1)))
  End Sub
 
End Module