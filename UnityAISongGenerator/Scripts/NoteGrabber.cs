using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using TMPro;
using System.Text.RegularExpressions;

public class NoteGrabber : MonoBehaviour
{
    public TextMeshProUGUI aiInputText;
    public TextMeshProUGUI outputNotes;
    public string readText;
    public string[] stringsToRead;
    public string writtenText;
    public int maxCharSize;
    public List<string> notes = new List<string>(); // Assuming you're working with string representations
    private int lastProcessedIndex = 0;



    // Start is called before the first frame update
    void Start ()
    {

    }

    // Update is called once per frame
    void Update ()
    {
        readText = aiInputText.text;
        ExtractAndSetWrittenText();
    }

    void ExtractAndSetWrittenText ()
    {
        if (writtenText.Length >= maxCharSize)
            return; // Avoid processing if already at max size
                    // Ensure lastProcessedIndex is not out of bounds
        if (lastProcessedIndex >= readText.Length)
        {
            // Potentially reset lastProcessedIndex here, or simply return
            // lastProcessedIndex = 0; // Reset if the text has been fully processed/changed.
            return; // Skip processing as there is no new text to process.
        }
        string newText = readText.Substring(lastProcessedIndex); // Process new text only
        string pattern = @"\b[A-G](?: - [A-G])*\b";
        MatchCollection matches = Regex.Matches(newText,pattern);
        foreach (Match match in matches)
        {
            if (writtenText.Length + match.Value.Length + 1 > maxCharSize)
                break; // +1 for '\n'
            writtenText += match.Value + "\n";
            notes.Add(match.Value);
            lastProcessedIndex += match.Index + match.Length; // Update last processed index correctly considering match.Index is relative to newText
        }
        outputNotes.text = writtenText.TrimEnd(); // Apply the trim at the end
    }
}