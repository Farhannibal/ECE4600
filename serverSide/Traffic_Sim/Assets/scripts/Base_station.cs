using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.IO;

public class Base_station : MonoBehaviour {


    public static Queue<Vehicle> vQueue;
    private Vehicle car;
    private float DEFAULT_SPEED = 3.0f;
    private Intersection centerIntersect;
    public List<Vector3> path1In, path1Out, path2In, path2Out;
    //public  GameObject waypoints = GameObject.Find("Waypoints");

    // private List<Transform> listOfPoints = waypoints.getComponentsInChildren<Transform>();

	// Use this for initialization
	void Start () {
        vQueue = new Queue<Vehicle>();
        centerIntersect = new Intersection("figure8");

        //--------------------------------------------------------------------------------------
        // JSON Testing

        CarData testObj = new CarData();
        testObj.commands = "UP,RIGHT,UP,RIGHT,UP,RIGHT,UP,RIGHT";
        WriteCarData(testObj);
        // ReadCarData();
        // GetCarUpdate("test");
        //--------------------------------------------------------------------------------------

        // Left and down path
        // TODO: Pick target location, then finish current path, find path with target and take all points to get there
        path1In = new List<Vector3>();
        path1In.Add(new Vector3(-2f, 1f, 2f));
        path1In.Add(new Vector3(-4f, 1f, 2f));
        path1In.Add(new Vector3(-7f, 1f, 2f));
        path1In.Add(new Vector3(-7f, 1f, -4f));
        path1In.Add(new Vector3(-7f, 1f, -7f));
        path1In.Add(new Vector3(-4f, 1f, -7f));
        path1In.Add(new Vector3(2f, 1f, -7f));
        path1In.Add(new Vector3(2f, 1f, -4f));
        path1In.Add(new Vector3(2f, 1f, -2f));


        path1Out = new List<Vector3>();
        path1Out.Add(new Vector3(-2f, 1f, -2f));
        path1Out.Add(new Vector3(-2f, 1f, -3f));
        path1Out.Add(new Vector3(-2f, 1f, -5f));
        path1Out.Add(new Vector3(-3.5f, 1f, -5f));
        path1Out.Add(new Vector3(-5f, 1f, -5f));
        path1Out.Add(new Vector3(-5f, 1f, -3.5f));
        path1Out.Add(new Vector3(-5f, 1f, -2f));
        path1Out.Add(new Vector3(-3.5f, 1f, -2f));
        path1Out.Add(new Vector3(-2f, 1f, -2f));

        // Right and up path
        path2In = new List<Vector3>();
        path2In.Add(new Vector3(2f, 1f, -2f));
        path2In.Add(new Vector3(4f, 1f, -2f));
        path2In.Add(new Vector3(7f, 1f, -2f));
        path2In.Add(new Vector3(7f, 1f, 2.5f));
        path2In.Add(new Vector3(7f, 1f, 7f));
        path2In.Add(new Vector3(2.5f, 1f, 7f));
        path2In.Add(new Vector3(-2f, 1f, 7f));
        path2In.Add(new Vector3(-2f, 1f, 3.5f));
        path2In.Add(new Vector3(-2f, 1f, 2f));

        path2Out = new List<Vector3>();
        path2Out.Add(new Vector3(2f, 1f, 2f));
        path2Out.Add(new Vector3(2f, 1f, 3.5f));
        path2Out.Add(new Vector3(2f, 1f, 5f));
        path2Out.Add(new Vector3(3.5f, 1f, 5f));
        path2Out.Add(new Vector3(5f, 1f, 5f));
        path2Out.Add(new Vector3(5f, 1f, 3.5f));
        path2Out.Add(new Vector3(5f, 1f, 2f));
        path2Out.Add(new Vector3(3.5f, 1f, 2f));
        path2Out.Add(new Vector3(2f, 1f, 2f));

        //ShowPaths();
    }

    private void ShowPaths()
    {
        for (int i = 0; i < path1In.Count; i++)
        {
            GameObject waypoint = GameObject.CreatePrimitive(PrimitiveType.Sphere);
            waypoint.transform.position = path1In[i];
            Collider collider = waypoint.GetComponent<Collider>();
            collider.enabled = false;

        }
        for (int i = 0; i < path1Out.Count; i++)
        {
            GameObject waypoint = GameObject.CreatePrimitive(PrimitiveType.Sphere);
            waypoint.transform.position = path1Out[i];
            Collider collider = waypoint.GetComponent<Collider>();
            collider.enabled = false;
        }
        for (int i = 0; i < path2In.Count; i++)
        {
            GameObject waypoint = GameObject.CreatePrimitive(PrimitiveType.Sphere);
            waypoint.transform.position = path2In[i];
            Collider collider = waypoint.GetComponent<Collider>();
            collider.enabled = false;
        }
        for (int i = 0; i < path2Out.Count; i++)
        {
            GameObject waypoint = GameObject.CreatePrimitive(PrimitiveType.Sphere);
            waypoint.transform.position = path2Out[i];
            Collider collider = waypoint.GetComponent<Collider>();
            collider.enabled = false;
        }
    }
	
	// Update is called once per frame
	void Update () {

    }

    public List<Vector3> GetNewPath(string name, Vector3 currPos)
    {
        // Might need to force initial car position to be a point on the path
        // TODO : Add option to disable U-Turn
        GameObject vehicle = GameObject.Find(name);
        if (vehicle != null)
        {
            car = (Vehicle)vehicle.GetComponent("Vehicle");
        }
        int randPath = UnityEngine.Random.Range(0, 4);
        car.SetCurrPathID(randPath);
        List<Vector3> newPath = new List<Vector3>();
        switch (randPath)
        {
            case 0:
                newPath = CopyVec3ArrayList(this.path1In);
                break;
            case 1:
                newPath = CopyVec3ArrayList(this.path1Out);
                break;
            case 2:
                newPath = CopyVec3ArrayList(this.path2In);
                break;
            case 3:
                newPath = CopyVec3ArrayList(this.path2Out);
                break;
            default:
                Debug.Log("Error in getNewPath");
                break;
        }

        return newPath;
    }

    private List<Vector3> CopyVec3ArrayList(List<Vector3> oldArray)
    {
        // Debug.Log(oldArray[0]);
        List<Vector3> newArray = new List<Vector3>();
        for (int i=0; i<oldArray.Count; i++)
        {
            newArray.Add(oldArray[i]);
        }
        return newArray;
    }

    public void AddToQueue(string name)
    {
        // Vehicle calls this when entering intersection
        GameObject vehicle = GameObject.Find(name);
        if (vehicle != null)
        {
            car = (Vehicle)vehicle.GetComponent("Vehicle");
            if (vQueue.Count != 0)
            {
                car.ChangeSpeed(0f);
                
            }
            vQueue.Enqueue(car);
        }
    }

    public void RemoveFromQueue(string name)
    {
        // Called when vehicle is allowed to pass through the intersection
        GameObject vehicle = GameObject.Find(name);
        if (vehicle != null)
        {
            car = (Vehicle)vehicle.GetComponent("Vehicle");
            car.ChangeSpeed(DEFAULT_SPEED);
            vQueue.Dequeue();
            if(vQueue.Count > 0)
            {
                Vehicle nextInLine = vQueue.Peek();
                nextInLine.ChangeSpeed(DEFAULT_SPEED);
            }
        }
    }

    private void ReadCarData()
    {
        string filePath = "Assets/carData.json";

        if (File.Exists(filePath))
        {
            // Read the json from the file into a string
            string dataAsJson = File.ReadAllText(filePath);
            // Pass the json to JsonUtility, and tell it to create a GameData object from it
            CarData loadedData = JsonUtility.FromJson<CarData>(dataAsJson);
        }
        else
        {
            Debug.LogError("Cannot load game data!");
        }
    }

    public void GetCarUpdate(string name)
    {
        string filePath = "Assets/carUpdate.json";
        if (File.Exists(filePath))
        {
            // Read the json from the file into a string
            string dataAsJson = File.ReadAllText(filePath);
            // Pass the json to JsonUtility, and tell it to create a GameData object from it
            CarUpdate loadedData = JsonUtility.FromJson<CarUpdate>(dataAsJson);

            // TODO:
            // 1.) Compare queues
            // 2.) If different, adjust sim car queue and position
            Debug.Log(loadedData.actionQueue);
            GameObject vehicle = GameObject.Find(name);
            if (vehicle != null)
            {
                car = (Vehicle)vehicle.GetComponent("Vehicle");
                int simQueueLen = car.GetCurrPathLength() - car.GetCurr(); // Path is full length, minus nodes we reached
                if (simQueueLen != loadedData.actionQueue.Length)
                {
                    // Simulation is behind 
                    if(simQueueLen > loadedData.actionQueue.Length)
                    {

                    }
                    else
                    {

                    }
                }
            }
        }
        else
        {
            Debug.LogError("Cannot load game data!");
        }
    }

    private void WriteCarData(CarData data)
    {
        string dataString = JsonUtility.ToJson(data);

        string path = null;
        #if UNITY_EDITOR
            path = "Assets/CarData.json";
        #endif
        #if UNITY_STANDALONE
            path = "Assets/CarData.json";
        #endif

        using (FileStream fs = new FileStream(path, FileMode.Create))
        {
            using (StreamWriter writer = new StreamWriter(fs))
            {
                writer.Write(dataString);
            }
        }
        #if UNITY_EDITOR
                UnityEditor.AssetDatabase.Refresh();
        #endif
    }

    [Serializable]
    public class CarData
    {
        public string commands;
    }

    [Serializable]
    public class CarUpdate
    {
        public int gear;
        public int speed;
        public string currentAction;
        public string[] actionQueue;

        // commands in mcont013.pysw
    }

}
