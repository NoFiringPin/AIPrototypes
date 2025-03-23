using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI; // Required for interacting with Slider UI
using TMPro;

public class SliderScript : MonoBehaviour
{
    public MoveBar moveBar; // Reference to the MoveBar script
    private Slider slider; // Reference to the Slider component
    public TextMeshProUGUI bpmText;

    void Start ()
    {
        slider = GetComponent<Slider>(); // Get the Slider component
        slider.onValueChanged.AddListener(OnSliderValueChanged); // Subscribe to the Slider's value change event
    }

    void OnSliderValueChanged (float value)
    {
        moveBar.SetSpeedBasedOnBPM(value); // Update MoveBar's speed based on the Slider's value

        if (bpmText != null)
        {
            bpmText.text = $"{Mathf.RoundToInt(value)} BPM";
        }
    }
}