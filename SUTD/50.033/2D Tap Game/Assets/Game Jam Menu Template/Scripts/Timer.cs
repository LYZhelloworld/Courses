using UnityEngine;
using System.Collections.Generic;

public class Timer : MonoBehaviour {

	private ShowPanels showPanels;
	public GameObject scoreText;
	public GameObject rankText;
	private ScoreController controller;
	public float gameTime = 10;
	private float timer; // Timer
	private bool start = false;

	[HideInInspector] public static List<int> rank;

	void Awake() {
		controller = GetComponent<ScoreController> ();
		showPanels = GetComponent<ShowPanels> ();
		rank = new List<int>(new int[] {0, 0, 0});
	}

	// Use this for initialization
	void Start () {
		
	}
	
	// Update is called once per frame
	void Update () {

	}

	private string GenericRank(int newScore) {
		rank.Add (newScore);
		rank.Sort ();
		rank.Reverse ();
		rank.RemoveAt(3);

		return string.Format ("1. {0}\n2. {1}\n3. {2}", rank [0], rank [1], rank [2]);
	}

	void OnGUI() {
		if (start && (Time.time - timer > gameTime)) {
			showPanels.ShowScorePanel (); // Show score board
			showPanels.HideGamePanel (); // Hide game
			int newScore = controller.getCounter();
			scoreText.GetComponent<UnityEngine.UI.Text>().text = newScore.ToString();
			rankText.GetComponent<UnityEngine.UI.Text> ().text = GenericRank (newScore);

			start = false; // Remove timer
		}
	}

	public void StartTimer () {
		timer = Time.time;
		start = true;
	}
}
