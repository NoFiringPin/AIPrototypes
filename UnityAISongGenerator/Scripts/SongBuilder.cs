using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class SongBuilder : MonoBehaviour
{
    public RawImage[] songNotePrefabs; // An array holding the different note prefabs
    public string songSequence = "F F D G C#";
    public int songNoteLimit = 5;
    public float horizontalSpacing = 100f; // Spacing between notes
    public NoteGrabber noteGrabber;
    private int lastNoteCount = 0;

    // Use Start to ensure all setup is done once
    void Start ()
    {
        BuildSong();
    }

    private void Update ()
    {
        // Check if new notes were added since the last update
        if (noteGrabber.notes.Count != lastNoteCount)
        {
            // Update songSequence only if there are new notes
            songSequence = string.Join(" ",noteGrabber.notes.ToArray());
            BuildSong(); // Rebuild the song with the new sequence
            lastNoteCount = noteGrabber.notes.Count; // Update the last note count
        }
    }

    void BuildSong ()
    {
        // Splitting the song sequence into individual notes
        string[] notes = songSequence.Split(' ');
        Vector3 startPosition = transform.position; // Storing the starting position

        int noteCount = 0;

        foreach (string note in notes)
        {
            if (noteCount >= songNoteLimit)
                break; // Limiting the number of notes as per songNoteLimit

            // Attempt to find a prefab that matches the current note
            RawImage notePrefab = FindNotePrefab(note);
            if (notePrefab != null)
            {
                // Instantiate the note prefab
                RawImage instance = Instantiate(notePrefab,this.transform);
                // Position the instantiated note
                instance.transform.position = startPosition + new Vector3(horizontalSpacing * noteCount,0,0);

                noteCount++; // Increment the note counter since a note was successfully built
            }
        }
    }

    RawImage FindNotePrefab (string note)
    {
        foreach (RawImage prefab in songNotePrefabs)
        {
            // Here you might need to adapt how you check if a prefab matches a note
            // Assuming prefab names directly match note names for simplicity
            if (prefab.name.Equals(note))
            {
                return prefab;
            }
        }

        return null; // Return null if no matching prefab is found
    }
}