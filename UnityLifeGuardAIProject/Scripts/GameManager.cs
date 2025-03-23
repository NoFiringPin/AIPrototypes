using System.Collections;
using System.Collections.Generic;
using TMPro;
using UnityEngine;

public class GameManager : MonoBehaviour
{
    public static GameManager Instance;

    // Scenario/Story management
    public GameObject feedbackCanvas;   // Reference to feedback canvas
    public GameObject[] canvases;       // Array to hold multiple canvases
    public GameObject[] positions;      // Array to hold multiple animation positions
    private int currentIndex = 0;       // Index to track both canvases and positions

    // Score management
    public int playerScore = 0;
    public TextMeshProUGUI scoreText;
    public TextMeshProUGUI errorText;

    private float errorDisplayDuration = 1.5f;
    private bool showingErrorMessage = false;  // To track if error message is being shown

    // Reference to the ScenarioTracker (not merged, still used in AIResponseManager)
    public ScenarioTracker storyTracker;

    // Choices management
    private Dictionary<string,bool> choiceSent = new Dictionary<string,bool>();

    private void Awake ()
    {
        // Ensure that only one instance of GameManager exists
        if (Instance == null)
        {
            Instance = this;
        }
        else if (Instance != this)
        {
            Destroy(gameObject); // Destroy any duplicate instances
        }
    }

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

        // Initialize score display
        errorText.gameObject.SetActive(false);
        UpdateScoreDisplay();
    }

    // Update the score display in the UI
    void UpdateScoreDisplay ()
    {
        scoreText.text = "Score: " + playerScore.ToString();
    }

    // Method to move to the next canvas and position
    public void NextChoice ()
    {
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
                // Activate both the feedbackCanvas GameObject and its Canvas component
                feedbackCanvas.SetActive(true);
                feedbackCanvas.GetComponent<Canvas>().enabled = true;
            }

            // Deactivate the last canvas and position
            canvases[currentIndex].SetActive(false);
            positions[currentIndex].SetActive(false);
        }
    }

    // Method to go back to the previous canvas and position
    public void GoBack ()
    {
        if (currentIndex > 0)
        {
            canvases[currentIndex].SetActive(false);
            positions[currentIndex].SetActive(false);

            currentIndex--;

            canvases[currentIndex].SetActive(true);
            positions[currentIndex].SetActive(true);
        }
    }

    // Manage the points system and move to the next choice
    public void AddOrSubtractPoints (int points)
    {
        // Allow both positive and negative points to be added to the score
        playerScore += points;
        UpdateScoreDisplay();

        // If the player earns points (positive score), proceed to the next choice
        if (points > 0)
        {
            NextChoice();
        }
    }



    // Method to show the error message (if desired for negative points)
    public void ShowErrorMessage (string customMessage = "Invalid operation!")
    {
        if (!showingErrorMessage)
        {
            showingErrorMessage = true;
            errorText.gameObject.SetActive(true);
            errorText.text = customMessage;

            StartCoroutine(HideErrorMessage());
        }
    }

    // Coroutine to hide the error message after a delay
    private System.Collections.IEnumerator HideErrorMessage ()
    {
        yield return new WaitForSeconds(errorDisplayDuration);
        errorText.gameObject.SetActive(false);
        showingErrorMessage = false;
    }

    // Method to send a choice, but only once per choice
    public void AddScenarioOption (string choice)
    {
        if (!string.IsNullOrEmpty(choice))
        {
            if (!choiceSent.ContainsKey(choice) || !choiceSent[choice])
            {
                // Add the choice and mark it as sent
                storyTracker.AddChoice(choice);
                choiceSent[choice] = true;
            }
            else
            {
                Debug.Log("Choice has already been sent: " + choice);
            }
        }
    }
}
