using BitSplash.AI.GPT;
using System.Collections;
using System.Collections.Generic;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace BitSplash.AI.GPT.Extras
{
    public class ResponseManager : MonoBehaviour
    {
        public StoryTrackerScript storyTracker;
        public string QuestionPrompt;
        public TMP_Text AnswerField;
        public Button SubmitButton;
        public Button RetryButton;

        // this is the role you want the AI to take as
        public string ChatDirection = "As a history professor, answer what would happen to the Manhattan Project and World War II if these events happened?";

        // The list of facts store important decisions the player made in order to send it to the AI
        public List<string> Facts;
        public bool TrackConversation = false;
        public int MaximumTokens = 500;
        [Range(0f,1f)]

        // Temperature affects how random we want the responses to be, 0 is for consistency and no randomness
        public float Temperature = 0f;

        ChatGPTConversation Conversation;

        void Start ()
        {
            Facts = storyTracker.storyChoices;
            SetUpConversation();
        }

        // This function sets up all the AI parameters at the beginning of the scene

        void SetUpConversation ()
        {
            Conversation = ChatGPTConversation.Start(this)
                .MaximumLength(MaximumTokens)
                .SaveHistory(TrackConversation)
                .System(string.Join("\n",Facts) + "\n" + ChatDirection);
            Conversation.Temperature = Temperature;
        }

        // This function sends data to the chat bot
        public void SendClicked ()
        {
            Globals.gameHasEnded = true;
            Globals.responseHasFailed = false;
            RetryButton.interactable = false;
            AnswerField.gameObject.SetActive (true);
            var facts = string.Join("\n",Facts);
            Conversation.Say(facts + "\n" + QuestionPrompt);
            SubmitButton.interactable = false;
            Debug.Log("Question sent");
        }

        // When an answer is received we are able to see it in the debug menu and the whole response in the text box
        void OnConversationResponse (string text)
        {
            Globals.responseHasFailed = false;
            Globals.responseSuccess = true;
            Debug.Log("Response Received");
            AnswerField.text = text;
            SubmitButton.interactable = true;
        }

        // If there are errors then we show it here
        void OnConversationError (string text)
        {
            Globals.responseHasFailed = true;
            RetryButton.interactable = true;
            Debug.Log("Error : " + text);
            Conversation.RestartConversation();
            AnswerField.text = "Error, Timed Out. Please Restart Program.";
            SubmitButton.interactable = true;
        }

        private void OnValidate ()
        {
            SetUpConversation();
        }

        // Update is called once per frame
        void Update ()
        {

        }
    }

}