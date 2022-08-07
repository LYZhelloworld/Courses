using UnityEngine;
using System.Collections;

public class FT : MonoBehaviour {
	// Use this for initialization	
	private Rigidbody rb;
	void Start () {
		rb = GetComponent<Rigidbody> ();
	}
	
	// Update is called once per frame
	void Update () {		
		if (Input.GetKey (KeyCode.UpArrow)) rb.AddForce (0,0,10);
		if (Input.GetKey (KeyCode.DownArrow)) rb.AddForce (0,0,-10);
		if (Input.GetKey (KeyCode.LeftArrow)) rb.AddForce (-10,0,0);
		if (Input.GetKey (KeyCode.RightArrow)) rb.AddForce (10,0,0);
	}
}
