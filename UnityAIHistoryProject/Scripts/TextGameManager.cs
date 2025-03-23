using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using TMPro;
using UnityEngine.UI;

public class TextGameManager : MonoBehaviour
{
    // Store an array of TextMesh Dialogues so it's easier to see and edit in the inspector
    public TextMeshProUGUI[] dialogues;

    // Create a list of images so the background can dynamically change
    public Texture[] images;
    public bool[] imagesToTurnOn;
    public TextMeshProUGUI textBox;
    public GameObject nextDialogueButton;
    [SerializeField] private int currentDialogueIndex = 1;
    [Space]
    public GameObject background;
    public GameObject decisionPoint;
    private int currentImageIndex = -1;
    private Texture currentImage;
    public float typingSpeed = 0.1f;
    private bool isTextFullyDisplayed = false;
    [SerializeField] private bool isEnd;

    private void Update ()
    {
        if (Input.GetMouseButtonDown(0))
        {
            NextDialogue();
        }

    }

    // This function manages showing the text dialogue on screen
    public void NextDialogue ()
    {
        if (isTextFullyDisplayed)
        {
            if (currentDialogueIndex < dialogues.Length)
            {
                StopAllCoroutines(); // stop any previous typing animation
                StartCoroutine(TypeSentence(dialogues[currentDialogueIndex].text));
                UpdateBackground(currentDialogueIndex);
                currentDialogueIndex++;
                isTextFullyDisplayed = false;
            }

            else if (isEnd == false)
            {
                decisionPoint.SetActive(true);
                nextDialogueButton.SetActive(false);

            }
        }
        else
        {
            StopAllCoroutines(); // stop the current typing animation
            textBox.text = dialogues[currentDialogueIndex - 1].text; // immediately display full text
            isTextFullyDisplayed = true;
        }
    }

    // This function manages changing the background
    private void UpdateBackground (int dialogueIndex)
    {
        if (dialogueIndex < images.Length && imagesToTurnOn[dialogueIndex])
        {
            currentImageIndex = dialogueIndex;
            currentImage = images[currentImageIndex];
            background.GetComponent<RawImage>().texture = currentImage;
        }
    }
    // This function types out the dialogue from the list of dialogues onto the main text box
    IEnumerator TypeSentence (string sentence)
    {
        textBox.text = "";
        foreach (char letter in sentence.ToCharArray())
        {
            textBox.text += letter;
            yield return new WaitForSeconds(typingSpeed);
        }
        isTextFullyDisplayed = true;
    }
}
