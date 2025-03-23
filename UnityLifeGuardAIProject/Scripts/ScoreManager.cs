using UnityEngine;
using TMPro;

public class ScoreManager : MonoBehaviour
{
    // Reference to the player's score
    public int playerScore = 0;

    // UI Text to display the score and error message
    public TextMeshProUGUI scoreText;
    public TextMeshProUGUI errorText;
    public GameObject FeedbackCanvas;

    // Time for error message to be displayed
    private float errorDisplayDuration = 1.5f;
    private bool showingErrorMessage = false;  // To track if error message is being shown

    void Start ()
    {
        playerScore = 0;
        scoreText.gameObject.SetActive(false);
        errorText.gameObject.SetActive(false);
        UpdateScoreDisplay();
    }

    // Update the score display in the UI
    void UpdateScoreDisplay ()
    {
        scoreText.text = "Score: " + playerScore.ToString();
    }

    public void PointsCounter (int points)
    {
        // Only allow negative points if the score is greater than 0
        if (points < 0 && playerScore <= 0)
        {
            // Prevent artificially reducing the score further
            ShowErrorMessage("Cannot reduce score below zero!");
            return;
        }

        // Allow both positive and valid negative points to be added to the score
        playerScore += points;
        UpdateScoreDisplay();

        // If the player earns points (positive score), proceed to the next choice
        if (points > 0)
        {
            ScenarioManager.Instance.NextChoice();
        }
        else
        {
            // Optional: If you want to show an error message when subtracting points
            ShowErrorMessage();
        }
    }

    public void FinalQuestion (bool isFinal)
    {
        if (isFinal)
        {
            FeedbackCanvas.gameObject.GetComponent<Canvas>().enabled = true;
            scoreText.gameObject.SetActive(true);
        }
    }

    // Method to show the error message (if desired for negative points)
    public void ShowErrorMessage (string customMessage = "Invalid operation!")
    {
        if (!showingErrorMessage) // Prevents multiple error messages
        {
            showingErrorMessage = true;
            errorText.gameObject.SetActive(true);
            errorText.text = customMessage; // Show the custom error message

            // Start a coroutine to hide the error message after a delay
            StartCoroutine(HideErrorMessage());
        }
    }

    // Coroutine to hide the error message after a delay
    private System.Collections.IEnumerator HideErrorMessage ()
    {
        yield return new WaitForSeconds(errorDisplayDuration);
        errorText.gameObject.SetActive(false);
        showingErrorMessage = false; // Allow error message to be shown again later
    }
}
