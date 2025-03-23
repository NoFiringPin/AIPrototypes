using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class SongReader : MonoBehaviour
{
    private List<Button> songList = new List<Button>();
    public List<SongInformation> songInfo = new List<SongInformation>();
    public Button[] songs; // This will be used to store up to 5 buttons from songList
    public List<string> chosenSongs = new List<string>(); // List to store chosen songs information as strings


    void Start ()
    {
        UpdateSongs();
    }

    void Update ()
    {
        UpdateSongs(); // Dynamically update songs every frame (or under certain conditions for optimization)
        ReadSongsFromButtons();
        PopulateChosenSongs(); // Call method to populate chosenSongs list
    }

    public void AddSong (string name,string artist,string genre)
    {
        SongInformation newSong = new SongInformation();
        newSong.songName = name;
        newSong.artist = artist;
        newSong.genre = genre;
        songInfo.Add(newSong);
    }

    private void UpdateSongs ()
    {
        songList.Clear();
        foreach (Transform child in transform)
        {
            var button = child.GetComponent<Button>();
            if (button != null)
            {
                songList.Add(button);
            }
        }

        // Ensure no more than 5 songs are allowed
        int count = Mathf.Min(5,songList.Count);
        songs = new Button[count];
        for (int i = 0; i < count; i++)
        {
            songs[i] = songList[i];
        }
    }

    private void ReadSongsFromButtons ()
    {
        songInfo.Clear(); // Clear the existing list to avoid duplications
        foreach (Button songButton in songs)
        {
            SongInformation songInformation = songButton.GetComponentInChildren<SongInformation>(); // Assumes SongInformation is on a child object
            if (songInformation != null)
            {
                songInfo.Add(songInformation);
            }
        }
    }



    private void PopulateChosenSongs ()
    {
        chosenSongs.Clear(); // Clear the existing list to avoid duplications
        // Loop through each songInfo and add a formatted string to chosenSongs
        foreach (var song in songInfo)
        {
            string songDetails = $"{song.songName} by {song.artist}"; // Formatting string
            chosenSongs.Add(songDetails);
        }
    }
    private void OnDisable ()
    {
        // Optionally, log the chosen songs when the object is disabled
        foreach (var chosenSong in chosenSongs)
        {
            Debug.Log(chosenSong);
        }
    }
}
