using UnityEngine;
using System.Collections;

public class MoveCube : MonoBehaviour {

	public float speed;
	private float timeLeft = 8.0f;

	// Use this for initialization
	void Start () {
		
	}
	
	// Update is called once per frame
	void Update () {
		Vector3 move = new Vector3 (Input.GetAxis ("Horizontal"), Input.GetAxis ("Vertical"), 0);
		transform.position += move * speed * Time.deltaTime;

		if (Input.GetMouseButtonDown (0)) {
			transform.localScale *= 0.9f;
		}

		timeLeft -= Time.deltaTime;
		if (timeLeft < 0) {
			Destroy (gameObject);
		}
	}

	/*
	void OnMouseDown () {
		transform.localScale *= 0.9f;
	}*/
}
