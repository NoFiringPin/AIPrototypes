using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PositionManager : MonoBehaviour
{
    public GameObject[] positions;  // Array to hold multiple positions
    private int currentPositionIndex = 0;  // Keep track of the current position

    // Start is called before the first frame update
    void Start ()
    {
        // Ensure only the first position is active initially
        for (int i = 0; i < positions.Length; i++)
        {
            positions[i].SetActive(i == 0);
        }
    }

    // Method to activate the next position based on the current question or canvas
    public void PositionTurnOn ()
    {
        if (currentPositionIndex < positions.Length - 1)
        {
            positions[currentPositionIndex].SetActive(false);  // Turn off the current position
            currentPositionIndex++;
            positions[currentPositionIndex].SetActive(true);   // Turn on the next position
        }
    }

    // Method to deactivate the current position and go back to the previous one
    public void PositionTurnOff ()
    {
        if (currentPositionIndex > 0)
        {
            positions[currentPositionIndex].SetActive(false);  // Turn off the current position
            currentPositionIndex--;
            positions[currentPositionIndex].SetActive(true);   // Turn on the previous position
        }
    }
}
