using UnityEngine;
using System.Collections;

using System;
using System.Runtime.Serialization.Formatters.Binary;
using System.IO;

public class GameController : MonoBehaviour {

	public GameObject[] hazards;
	public Vector3 spawnValues;
	public int hazardCount;
	public float spawnWait;
	public float startWait;
	public float waveWait;

	public GUIText scoreText;
	private int score;

	// Use this for initialization
	void Start () {
		score = 0;
		UpdateScore ();
		StartCoroutine (SpawnWaves ());
	}
	
	// Update is called once per frame
	void Update () {
	
	}

	IEnumerator SpawnWaves() {
		yield return new WaitForSeconds (startWait);
		while (true) {
			for (int i = 0; i < hazardCount; ++i) {
				GameObject hazard = hazards [UnityEngine.Random.Range (0, hazards.Length)];
				Vector3 spawnPosition = new Vector3 (UnityEngine.Random.Range (-spawnValues.x, spawnValues.x), spawnValues.y, spawnValues.z);
				Quaternion spawnRotation = Quaternion.identity;
				Instantiate (hazard, spawnPosition, spawnRotation);
				yield return new WaitForSeconds (spawnWait);
			}
			yield return new WaitForSeconds (waveWait);
		}
	}

	public void AddScore (int newScoreValue) {
		score += newScoreValue;
		UpdateScore ();
	}

	public void UpdateScore () {
		scoreText.text = "Score: " + score;
	}

	public void Save()
	{
		BinaryFormatter bf = new BinaryFormatter();
		FileStream file = File.Create(Application.persistentDataPath + "/playerInfo.dat");

		PlayerData data = new PlayerData();
		data.score = score;

		GameObject player = GameObject.FindWithTag ("Player");
		data.playerx = player.transform.position.x;
		data.playery = player.transform.position.y;
		data.playerz = player.transform.position.z;

		bf.Serialize(file, data);
		file.Close();
	}

	public void Load()
	{
		if(File.Exists(Application.persistentDataPath + "/playerInfo.dat"))
		{
			BinaryFormatter bf = new BinaryFormatter();
			FileStream file = File.Open(Application.persistentDataPath + "/playerInfo.dat", FileMode.Open);
			PlayerData data = (PlayerData) bf.Deserialize(file);
			file.Close();

			// update score
			score = data.score;
			UpdateScore ();

			// update player position
			GameObject player = GameObject.FindWithTag ("Player");
			player.transform.position = new
			Vector3(data.playerx,data.playery,data.playerz);
		}
	}
}

[Serializable]
class PlayerData {
	public int score;
	public float playerx;
	public float playery;
	public float playerz;
}