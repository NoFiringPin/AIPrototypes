using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using TMPro;

public class StoryTrackerScript : MonoBehaviour
{
    public List<string> storyChoices;
    public TextMeshProUGUI choiceSummary;
    public bool callPrintChoices;

    // Update is called once per frame
    void Update ()
    {
        PrintStoryChoices();
    }

    public void AddChoice (string choice)
    {
        storyChoices.Add(choice);
    }

    public void PrintStoryChoices ()
    {
        if (callPrintChoices)
        {
            foreach (string choice in storyChoices)
            {
                Debug.Log(choice);
            }
            choiceSummary.text = string.Join("\n",storyChoices);
        }
    }
}
