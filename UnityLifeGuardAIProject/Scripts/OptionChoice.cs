using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class OptionChoice : MonoBehaviour
{
    public GameObject[] canvases;  // Array to hold multiple canvases
    private int currentCanvasIndex = 0;

    // Start is called before the first frame update
    void Start ()
    {
        // Ensure only the first canvas is active initially
        for (int i = 0; i < canvases.Length; i++)
        {
            canvases[i].SetActive(i == 0);
        }
    }

    // Method to switch to the next canvas
    public void CorrectChoice ()
    {
        if (currentCanvasIndex < canvases.Length - 1)
        {
            canvases[currentCanvasIndex].SetActive(false);
            currentCanvasIndex++;
            canvases[currentCanvasIndex].SetActive(true);
        }
    }

    // Method to go back to the previous canvas
    public void GoBack ()
    {
        if (currentCanvasIndex > 0)
        {
            canvases[currentCanvasIndex].SetActive(false);
            currentCanvasIndex--;
            canvases[currentCanvasIndex].SetActive(true);
        }
    }
}
