using UnityEngine;
using System.Collections;

public class ObjectAccess : MonoBehaviour {
	GameObject obj1;
	Transform obj2;
	//Transform obj3;
	// Use this for initialization
	void Start () {
		obj1 = GameObject.Find("Cube 1");//finding by name via GameObject Static Class
		obj2 = transform.Find("Cube 1");//finding by name via transform instance
		//obj3 = transform.parent.Find("Cube");

	}
	
	// Update is called once per frame
	void Update () {
		obj1.transform.localScale -= new Vector3(0, 0.01f, 0);
		obj2.transform.localScale += new Vector3(0, 0.01f, 0);
	}
}
