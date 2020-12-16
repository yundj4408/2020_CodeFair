using System.Collections;
using System.Collections.Generic;
using UnityEngine;

using System;
using System.Diagnostics;
using Debug = UnityEngine.Debug;


public class PythonController : MonoBehaviour
{

    public void start_Python()
    {
        var psi = new ProcessStartInfo();
        psi.FileName = @"C:\Users\KHS\AppData\Local\Programs\Python\Python38-32\python.exe"; //파이썬 설치 경로
        psi.Arguments = $"\"C:\\Users\\KHS\\Downloads\\CodeFair\\Assets\\Scripts\\Python\\system_test4.py\"";

        //3) Proecss configuration
        psi.UseShellExecute = false;
        psi.CreateNoWindow = true;
        psi.RedirectStandardOutput = true;
        psi.RedirectStandardError = true;

        //4) return value def
        var erros = "";
        var results = "";

        using (var process = Process.Start(psi))
        {
            erros = process.StandardError.ReadToEnd();
            results = process.StandardOutput.ReadToEnd();
        }
        
        Debug.Log(erros);
        Debug.Log(results);
    }
    
    /*public void test()
    {
        var engine = IronPython.Hosting.Python.CreateEngine();
        var scope = engine.CreateScope();

        try
        {
            //파일을 읽지 않고 스크립트를 바로작성
            var source = engine.CreateScriptSourceFromFile(@"test.py");
            source.Execute(scope);

            var getPythonFuncResult = scope.GetVariable<Func<string>>("getPythonFunc");
            Console.WriteLine("def 실행 테스트 : " + getPythonFuncResult());

            var sum = scope.GetVariable<Func<int, int, int>>("sum");
            Console.WriteLine(sum(1, 2));

            //파일을 읽지 않고 스크립트를 바로작성
            var source2 = engine.CreateScriptSourceFromString(@"print('스크립트를 직접작성해 출력 테스트')");
            source2.Execute(scope);

        }
        catch (Exception ex)
        {
            Console.WriteLine(ex.Message);
        }
    }*/
     
}
