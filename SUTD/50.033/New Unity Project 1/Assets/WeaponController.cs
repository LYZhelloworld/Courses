using UnityEngine;
using System.Collections;

public class WeaponController : MonoBehaviour {

	public GameObject shot;
	public Transform shotSpawn;
	public float fireRate;
	public float delay;

	// Use this for initialization
	void Start () {
		InvokeRepeating ("Fire", delay, fireRate);
	}
	
	// Update is called once per frame
	void Update () {
		
	}

	void Fire () {
		Instantiate (shot, new Vector3 (shotSpawn.position.x, shotSpawn.position.y, shotSpawn.position.z - 2), shotSpawn.rotation);
	}
}
