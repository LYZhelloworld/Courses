using UnityEngine;
using System.Collections;

public class RestartGame : MonoBehaviour {

	private ShowPanels showPanels;

	void Awake () {
		showPanels = GetComponent <ShowPanels> ();
	}

	public void RestartClicked () {
		showPanels.HideScorePanel ();
		showPanels.ShowMenu ();
	}
}
