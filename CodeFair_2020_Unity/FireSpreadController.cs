using System.Collections;
using System.Collections.Generic;
using UnityEngine;


public class FireSpreadController : MonoBehaviour
{
    private float t = 0;
    private float t_th = 5.0f;
    private bool spreaded = false;
    public GameObject fire_prefeb;

    private void Update()
    {
        
        if(this.transform.position.x>213 || this.transform.position.x < 10)
        {
            Destroy(this.gameObject);
        }

        Spread();
        
    }

   

    void Spread()
    {
        t += Time.deltaTime;

        if (t > t_th && spreaded == false)
        {
            Instantiate(fire_prefeb, this.transform.position + new Vector3(32, 0, 0), Quaternion.identity);
            Instantiate(fire_prefeb, this.transform.position + new Vector3(-32, 0, 0), Quaternion.identity);
            t = 0;
            spreaded = true;
        }
    }
}
