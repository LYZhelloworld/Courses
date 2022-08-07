using UnityEngine;
using System.Collections;

public class TRS : MonoBehaviour {
	public int speed = 0;
	public int rotSpeed = 10;
	public float scaleSpeed = 0.001f;
	public bool activate;
	// Use this for initialization
	void Start () {
	}
	
	// Update is called once per frame
	void Update () {
		transform.Translate(Vector3.forward * speed * Time.deltaTime); 			
		transform.Rotate(Vector3.up, rotSpeed * Time.deltaTime);
		transform.localScale += new Vector3(0, scaleSpeed, 0);

	}
}
