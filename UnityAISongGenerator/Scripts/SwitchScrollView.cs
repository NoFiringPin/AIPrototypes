using UnityEngine;
using UnityEngine.UI;

public class SwitchScrollView : MonoBehaviour
{
    // Reference to the ScrollViews
    public Transform originalScrollViewContent;
    public Transform targetScrollViewContent;


    void Awake ()
    {
        // Ensure the button has a listener for click events
        GetComponent<Button>().onClick.AddListener(OnClick);

    }
    void OnClick ()
    {
        // Switch the button's parent to the target ScrollView
        // Note: The button must be a direct child of the content object of the ScrollView
        if (transform.parent == originalScrollViewContent)
        {
            transform.SetParent(targetScrollViewContent,false);
        }
        else
        {
            transform.SetParent(originalScrollViewContent,false);
        }
    }
}