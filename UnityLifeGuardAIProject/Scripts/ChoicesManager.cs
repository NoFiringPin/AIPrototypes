using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ChoicesManager : MonoBehaviour
{
    public GameObject storyTrackerObject;
    [SerializeField] private ScenarioTracker storyTracker;

    // Dictionary to track whether a choice has already been made
    private Dictionary<string,bool> choiceSent = new Dictionary<string,bool>();

    // Method to send a choice, but only once per choice
    public void SendChoice (string choice)
    {
        if (!string.IsNullOrEmpty(choice))
        {
            // Check if this choice has already been sent
            if (!choiceSent.ContainsKey(choice) || !choiceSent[choice])
            {
                // Add the choice and mark it as sent
                storyTracker.AddChoice(choice);
                choiceSent[choice] = true;  // Mark this choice as sent
            }
            else
            {
                Debug.Log("Choice has already been sent: " + choice);
            }
        }
    }
}
