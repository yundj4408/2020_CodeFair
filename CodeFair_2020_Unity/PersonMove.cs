using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PersonMove : MonoBehaviour
{
    private PersonRayCast PersonRayCastScrips;
    private ScoreController scoreController;
    public GameObject EventSystem;
    public float dist_threshold = 6.0f;
    private float dist;
    private Animator animator;

    UnityEngine.AI.NavMeshAgent agent;


    //플레이어 키보드 움직임 변수
    public float player_Speed = 5.0f;
    public GameObject target;
    private Vector3 dir;
    private float h;
    private float v;


    private void Start()
    {
        PersonRayCastScrips = this.gameObject.GetComponent<PersonRayCast>();
        animator = this.gameObject.GetComponent<Animator>();
        scoreController = EventSystem.GetComponent<ScoreController>();

        if (target == null) target = GameObject.Find("Target");
        agent = GetComponent<UnityEngine.AI.NavMeshAgent>();

    }

    void Update()
    {

        Move();

        //NavMesh AI 움직임 부분

    }

    void Move()
    {
        dist = Vector3.Distance(this.transform.position, target.transform.position);

        if (dist < dist_threshold) //target에 도착했을 때,
        {
            Debug.Log("Arrived!");
            animator.SetBool("run", false);
            scoreController.arrived += 1;
        }
        else //target이 멀리있을 때
        {
            agent.SetDestination(target.transform.position);
            animator.SetBool("run", true);
        }
    }

    /*
    void Move()
    {
        h = Input.GetAxis("Horizontal");
        v = Input.GetAxis("Vertical");

        dir = Vector3.right * h + Vector3.forward * v;

        this.transform.Translate(dir * player_Speed * Time.deltaTime);

        if (h != 0 || v != 0)
        {
            animator.SetBool("run", true);
        }
        else animator.SetBool("run", false);
    }*/

}
