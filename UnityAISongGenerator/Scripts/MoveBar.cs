using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class MoveBar : MonoBehaviour
{
    public GameObject Bar;
    public GameObject endPoint;
    [SerializeField]private float Speed = 0.1f;
    bool isMoving = false;

    public void SetSpeedBasedOnBPM(float bpm)
    {
        Speed = bpm / 60f * 0.1f;
    }

    private void Update ()
    {
        if (isMoving == true)
        {
            Bar.transform.position += new Vector3((Speed) + Time.deltaTime,0,0);
            if (Bar.transform.position.x >= endPoint.transform.position.x && Bar.transform.position.y == endPoint.transform.position.y)
            {
                isMoving = false;
            }
        }


    }

    public void onPlayButtonClick ()
    {
        isMoving = true;
    }

}
