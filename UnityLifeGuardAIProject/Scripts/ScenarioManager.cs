using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ScenarioManager : MonoBehaviour
{
    public static ScenarioManager Instance;

    private void Awake ()
    {
        // Ensure that only one instance of ScenarioManager exists
        if (Instance == null)
        {
            Instance = this;
        }
        else if (Instance != this)
        {
            Destroy(gameObject); // Destroy any duplicate instances
        }
    }

    public GameObject feedbackCanvas;   // Reference to feedback canvas
    public GameObject[] canvases;       // Array to hold multiple canvases
    public GameObject[] positions;      // Array to hold multiple animation positions
    private int currentIndex = 0;       // Index to track both canvases and positions

    // Start is called before the first frame update
    void Start ()
    {
        // Initialize canvases and positions
        for (int i = 0; i < canvases.Length; i++)
        {
            canvases[i].SetActive(i == 0);  // Only activate the first canvas
        }

        for (int i = 0; i < positions.Length; i++)
        {
            positions[i].SetActive(i == 0); // Only activate the first position
        }

        // Ensure the feedback canvas is initially inactive
        if (feedbackCanvas != null)
        {
            feedbackCanvas.SetActive(false);
        }
    }

    // Method to move to the next canvas and position
    public void NextChoice ()
    {
        // Check if the current index is the last one
        if (currentIndex < canvases.Length - 1 && currentIndex < positions.Length - 1)
        {
            // Deactivate the current canvas and position
            canvases[currentIndex].SetActive(false);
            positions[currentIndex].SetActive(false);

            // Increment the index
            currentIndex++;

            // Activate the next canvas and position
            canvases[currentIndex].SetActive(true);
            positions[currentIndex].SetActive(true);
        }
        else if (currentIndex == canvases.Length - 1 && currentIndex == positions.Length - 1)
        {
            // If the player is on the last item, activate the feedback canvas
            if (feedbackCanvas != null)
            {
                feedbackCanvas.SetActive(true);   // Turn on the feedback canvas
            }

            // Optionally deactivate the last canvas and position if required
            canvases[currentIndex].SetActive(false);
            positions[currentIndex].SetActive(false);
        }
    }

    // Method to go back to the previous canvas and position
    public void GoBack ()
    {
        if (currentIndex > 0)
        {
            // Deactivate the current canvas and position
            canvases[currentIndex].SetActive(false);
            positions[currentIndex].SetActive(false);

            // Decrement the index
            currentIndex--;

            // Activate the previous canvas and position
            canvases[currentIndex].SetActive(true);
            positions[currentIndex].SetActive(true);
        }
    }
}
