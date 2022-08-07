using UnityEngine;
using System.Collections;

public class ThrowObject : MonoBehaviour {
	
	public GameObject projectile;
	public AudioClip shootSound;
	
	
	public float throwSpeed = 200f;
	private AudioSource source;
	private float volLowRange = .5f;
	private float volHighRange = 1.0f;
	
	
	void Awake () {
		
		source = GetComponent<AudioSource>();
		
	}
	
	
	void Update () {
		
		if (Input.GetButtonDown("Fire1"))
		{
			float vol = Random.Range (volLowRange, volHighRange);
			source.PlayOneShot(shootSound,vol);
			GameObject throwThis = Instantiate (projectile, transform.position, transform.rotation) as GameObject;
			throwThis.GetComponent<Rigidbody>().AddRelativeForce (new Vector3(0,0,throwSpeed));
		}
		
	}
}