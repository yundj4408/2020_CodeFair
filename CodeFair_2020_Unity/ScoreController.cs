using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class ScoreController : MonoBehaviour
{
    public Text arrived_text;
    public Text Person_text;
    public int arrived = 0;
    public int Person = 0;

    private void Update()
    {
        Person_text.text = "총 인원 : " + Person;
        arrived_text.text = "도착 : " + arrived;
    }

}
