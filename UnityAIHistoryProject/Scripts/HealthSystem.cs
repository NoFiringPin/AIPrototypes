using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using TMPro;

public class HealthSystem : MonoBehaviour
{
    public float currentHealth;
    public TextMeshProUGUI healthText;
    private float maxHealth = 100f;
    public healthScript healthbar;

   


    // Start is called before the first frame update
    void Start()
    {
    }


    // Update is called once per frame
    void Update()
    {
        UpdateHealthBar();
        currentHealth = Globals.playerStressLevel;
        currentHealth = Mathf.Max(0f,Globals.playerStressLevel);



    }

    void UpdateHealthBar()
    {
        healthbar.UpdateHealthBar(maxHealth,currentHealth);
        int roundedHealth = Mathf.RoundToInt(currentHealth);
        healthText.text = $"{roundedHealth}%";
    }

}
