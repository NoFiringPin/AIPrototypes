using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using TMPro;

public class StoryTrackerScript : MonoBehaviour
{
    // This script keeps track of all the story choices in the game
    // and stores it so it can be called for later

    public List<string> storyChoices;
    public TextMeshProUGUI choiceSummary;
    public bool callPrintChoices;

    // Update is called once per frame
    void Update()
    {
        PrintStoryChoices();
    }

    public void AddChoice(string choice)
    {
        storyChoices.Add(choice);
    }

    public void PrintStoryChoices()
    {
        if (callPrintChoices)
        {
           foreach (string choice in storyChoices)
            {
                Debug.Log(choice);
            }
           choiceSummary.text = string.Join("\n", storyChoices);
        }
    }
}
