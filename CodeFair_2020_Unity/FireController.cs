using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[System.Serializable]
public class Floor
{
    public GameObject[] Node;
}

public class FireController : MonoBehaviour
{
    //1. x, y 번지게 함.
    //2. z축으로도 번지게 함.(계단으로만)
    //3. 연기 이펙트

    public GameObject fire_prefeb;
    public GameObject safefire_prefeb;
    public GameObject arrow_prefeb;

    private float t = 0.0f;
    private float spread_threshold = 5.0f;
    private int rand_floor;
    private int rand_node;
    private bool fire_available = true;
    private int[,] isfire = new int [8,7];
    public Floor[] floor;
    /*
    2m/s 번지는 속도
        연기는 수평으로 0.5m/s 수직으로 2.5m/s
        사람 1m/s*/

    private void Start()
    {
        
        for (int i = 0; i < 8; i++)
        {
            for(int j = 0; j < 7; j++)
            {
                isfire[i, j] = 0;
                if (floor[i].Node[j] == null)
                {
                    Debug.Log(i + "번째 층" + j + "번째 층에 노드가 할당되지 않았습니다.");
                }
            }
        }
    }

    private void Update()
    {
        
        //Fire_spread();

    }

    public void Fire_start_Button()
    {
        for (int i = 0; i < 8; i++)
        {
            for (int j = 0; j < 7; j++)
            {
                if (isfire[i, j] == 0)
                {
                    fire_available = true;
                }
                
            }
        }

        if(fire_available == true)
        {
            while (true)
            {
                rand_floor = Random.Range(0, 8);
                rand_node = Random.Range(0, 7);
                if (isfire[rand_floor, rand_node] == 0)
                {
                    Debug.Log((rand_floor + 1) + "층" + (rand_node + 1) + "번째 노드에 불이 났습니다.");
                    Vector3 randPos = floor[rand_floor].Node[rand_node].transform.position;
                    Instantiate(fire_prefeb, randPos + new Vector3(0, 8, 0), Quaternion.identity);

                    isfire[rand_floor, rand_node] = 1;
                    fire_available = false;
                    break;
                }
            }
        }
        else
        {
            Debug.Log("모든 노드에 불이 났습니다.");
        }

    }

    public void safeFire_start_Button()
    {
        for (int i = 0; i < 8; i++)
        {
            for (int j = 0; j < 7; j++)
            {
                if (isfire[i, j] == 0)
                {
                    fire_available = true;
                }

            }
        }

        if (fire_available == true)
        {
            while (true)
            {
                rand_floor = Random.Range(0, 8);
                rand_node = Random.Range(0, 7);
                if (isfire[rand_floor, rand_node] == 0)
                {
                    Debug.Log((rand_floor + 1) + "층" + (rand_node + 1) + "번째 노드에 안전한 불이 났습니다.");
                    Vector3 randPos = floor[rand_floor].Node[rand_node].transform.position;
                    Instantiate(safefire_prefeb, randPos + new Vector3(0, 8, 0), Quaternion.identity);

                    isfire[rand_floor, rand_node] = 1;
                    fire_available = false;
                    break;
                }
            }
        }
        else
        {
            Debug.Log("모든 노드에 불이 났습니다.");
        }

    }

    void Fire_spread()
    {
        
        t += Time.deltaTime;
        
        if(t > spread_threshold)
        {
            Floor_spread();
            t = 0;
        }
    }

    void Floor_spread()
    {
        
    }

}
