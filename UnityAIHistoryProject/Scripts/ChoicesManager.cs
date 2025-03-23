using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ChoicesManager : MonoBehaviour
{
    [Tooltip("Add the next dialogue trees here")]
    public GameObject[] dialogueTrees;
    [Tooltip("Add the buttons from your decisions here")]
    public GameObject[] buttonChoices;
    public GameObject previousDialogue;
    public int choice1Stress;
    public int choice2Stress;
    [Space]
    public string choice1Summary;
    public string choice2Summary;
    public GameObject storyTrackerObject;
    [SerializeField] private StoryTrackerScript storyTracker;

    public void OnEnable ()
    {
        storyTrackerObject = GameObject.FindGameObjectWithTag("Story Tracker");
    }

    public void ChoseChoice1 ()
    {
        for (int i = 0; i < dialogueTrees.Length; i++)
        {
            for (int x = 0; x < buttonChoices.Length; x++)
            {
                if (i == 0)
                {
                    previousDialogue.SetActive(false);
                    buttonChoices[x].SetActive(false);
                    dialogueTrees[i].SetActive(true);

                }
                else
                {
                    dialogueTrees[i].SetActive(false);
                }
            }
        }
        Globals.playerStressLevel += choice1Stress;
        print("Player Stress Level:" + Globals.playerStressLevel);
        if (!string.IsNullOrEmpty(choice1Summary))
        {
            storyTracker.AddChoice(choice1Summary);
        }

    }

    public void ChoseChoice2 ()
    {
        for (int i = 0; i < dialogueTrees.Length; i++)
        {
            for (int x = 0; x < buttonChoices.Length; x++)
            {
                if (i == 0)
                {
                    previousDialogue.SetActive(false);
                    buttonChoices[x].SetActive(false);
                    dialogueTrees[i].SetActive(false);
                }
                else
                {
                    dialogueTrees[i].SetActive(true);
                }
            }
        }

        Globals.playerStressLevel += choice2Stress;
        print("Player Stress Level:" + Globals.playerStressLevel);
        if (!string.IsNullOrEmpty(choice2Summary))
        {
            storyTracker.AddChoice(choice2Summary);
        }

    }
}