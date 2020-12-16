using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PersonRayCast : MonoBehaviour
{
    
    private RaycastHit hit;

    public float maxDistance = 5.0f;

    private Vector3 playerCenter;
    //private int fire_layerMask = 10;

    public bool isfire = false;


    void FixedUpdate()
    {
        ray_func(); // Raycast - 레이저를 쏘아 물체 인식

    }

    void ray_func()
    {
        playerCenter = new Vector3(this.transform.position.x, this.transform.position.y + this.transform.localScale.y, this.transform.position.z);  // 플레이어 위치 오프셋 조정

        if (Physics.Raycast(playerCenter, this.transform.forward, out hit, Mathf.Infinity)) // ray가 오브젝트와 부딪혔을 때,
        {
            if(hit.collider.CompareTag("fire")) // 상대 오브젝트의 태그가 fire일 결우,
            {
                isfire = true;
                //Debug.Log("Fire Detected!");
                Debug.DrawRay(playerCenter, this.transform.forward * hit.distance, Color.red);
            }
            
            
        }

        else //부딪히지 않을 경우, 
        {
            isfire = false;
            //Debug.Log("No detected!");
            Debug.DrawRay(playerCenter, this.transform.forward * maxDistance, Color.blue);
        }

    }
}
