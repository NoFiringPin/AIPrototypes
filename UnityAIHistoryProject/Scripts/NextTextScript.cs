using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class NextTextScript : MonoBehaviour
{
    public GameObject[] textboxes;
    private int currentIndex = 0;

    public void SwitchImage ()
    {
        textboxes[currentIndex].gameObject.SetActive(false);

        currentIndex++;
        if (currentIndex >= textboxes.Length)
        {
            currentIndex = 0;
        }

        textboxes[currentIndex].gameObject.SetActive(true);
    }
}
