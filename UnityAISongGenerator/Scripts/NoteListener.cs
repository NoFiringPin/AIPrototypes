using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[RequireComponent(typeof(AudioSource))] // Ensures there's an AudioSource component attached to the GameObject
public class NoteListener : MonoBehaviour
{
    private AudioSource audioSource; // Reference to the AudioSource component
    public string noteToListen;

    void Start ()
    {
        // Get the AudioSource component attached to the GameObject
        audioSource = GetComponent<AudioSource>();
    }

    void OnTriggerEnter2D (Collider2D other)
    {
        // Check if the other collider has the "PlayBar" tag
        if (other.CompareTag("PlayBar"))
        {
            // Play the audio component
            Debug.Log("Audio attempted to play");
            audioSource.Play();
            
        }
    }

    private void OnCollisionEnter2D (Collision2D collision)
    {
        if (collision.gameObject.tag == "PlayBar")
        {
            Debug.Log("Audio attempted to play");
            audioSource.Play();
        }
    }

    private void OnTriggerExit2D (Collider2D collision)
    {
        if (collision.gameObject.tag == "PlayBar")
        {
            Debug.Log("Audio attempted to stop");
            audioSource.Stop();
        }
    }
}