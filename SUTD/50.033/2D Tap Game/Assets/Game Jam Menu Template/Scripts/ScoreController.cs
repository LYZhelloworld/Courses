using UnityEngine;
using System.Collections;

public class ScoreController : MonoBehaviour {


	public GameObject clickText;
	//private int score;
	//public int scoreValue; 

	private int counter = 0;

	public void NewGame() {
		counter = 0; // lets start with zero
		GetComponent<Timer> ().StartTimer ();
	}

	void Update() {
		clickText.GetComponent<UnityEngine.UI.Text>().text = "Count: " + counter;
	}

	public void ClickEvent()
	{
		counter++;
		/*
		if (GUI.Button(new Rect(100,100,200,50), "Count: " + counter))
		{ // the IF is true = clicked, lets count one
			counter ++; 
		}*/
		//Debug.Log ("Count: " + counter);
	}

	public int getCounter() {
		return counter;
	}

}
