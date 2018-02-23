using System;
using System.Collections;
using System.Collections.Generic;
using System.Threading;
using UnityEngine;
using System.IO;

public class Base_station : MonoBehaviour {


    public static Queue<Vehicle> vQueue;
    private Vehicle car;
    private float DEFAULT_SPEED = 3.0f;
    private Intersection centerIntersect;
    public List<Vector3> path0, path1, path2, path3;
    private List<CarData> export_data;

	// Use this for initialization
	void Start () {
        vQueue = new Queue<Vehicle>();
        centerIntersect = new Intersection("figure8");

        //--------------------------------------------------------------------------------------
        // JSON Testing

        //CarData testObj = new CarData();
        //testObj.name = "Hoodie";
        //testObj.commands = "FORWARD,RIGHT,FORWARD,RIGHT,FORWARD,RIGHT,FORWARD,RIGHT";
        //WriteCarData(testObj);
        // ReadCarData();
        // GetCarUpdate("test");
        //--------------------------------------------------------------------------------------

        // Left and down path
        // TODO: Pick target location, then finish current path, find path with target and take all points to get there
        path0 = new List<Vector3>();
        path0.Add(new Vector3(-2f, 1f, 2f));
        path0.Add(new Vector3(-4f, 1f, 2f));
        path0.Add(new Vector3(-7f, 1f, 2f));
        path0.Add(new Vector3(-7f, 1f, -4f));
        path0.Add(new Vector3(-7f, 1f, -7f));
        path0.Add(new Vector3(-4f, 1f, -7f));
        path0.Add(new Vector3(2f, 1f, -7f));
        path0.Add(new Vector3(2f, 1f, -4f));
        path0.Add(new Vector3(2f, 1f, -2f));


        path1 = new List<Vector3>();
        path1.Add(new Vector3(-2f, 1f, -2f));
        path1.Add(new Vector3(-2f, 1f, -3f));
        path1.Add(new Vector3(-2f, 1f, -5f));
        path1.Add(new Vector3(-3.5f, 1f, -5f));
        path1.Add(new Vector3(-5f, 1f, -5f));
        path1.Add(new Vector3(-5f, 1f, -3.5f));
        path1.Add(new Vector3(-5f, 1f, -2f));
        path1.Add(new Vector3(-3.5f, 1f, -2f));
        path1.Add(new Vector3(-2f, 1f, -2f));

        // Right and up path
        path2 = new List<Vector3>();
        path2.Add(new Vector3(2f, 1f, -2f));
        path2.Add(new Vector3(4f, 1f, -2f));
        path2.Add(new Vector3(7f, 1f, -2f));
        path2.Add(new Vector3(7f, 1f, 2.5f));
        path2.Add(new Vector3(7f, 1f, 7f));
        path2.Add(new Vector3(2.5f, 1f, 7f));
        path2.Add(new Vector3(-2f, 1f, 7f));
        path2.Add(new Vector3(-2f, 1f, 3.5f));
        path2.Add(new Vector3(-2f, 1f, 2f));

        path3 = new List<Vector3>();
        path3.Add(new Vector3(2f, 1f, 2f));
        path3.Add(new Vector3(2f, 1f, 3.5f));
        path3.Add(new Vector3(2f, 1f, 5f));
        path3.Add(new Vector3(3.5f, 1f, 5f));
        path3.Add(new Vector3(5f, 1f, 5f));
        path3.Add(new Vector3(5f, 1f, 3.5f));
        path3.Add(new Vector3(5f, 1f, 2f));
        path3.Add(new Vector3(3.5f, 1f, 2f));
        path3.Add(new Vector3(2f, 1f, 2f));

        ShowPaths();
    }

    private void ShowPaths()
    {
        for (int i = 0; i < path0.Count; i++)
        {
            GameObject waypoint = GameObject.CreatePrimitive(PrimitiveType.Sphere);
            waypoint.transform.position = path0[i];
            Collider collider = waypoint.GetComponent<Collider>();
            collider.enabled = false;

        }
        for (int i = 0; i < path1.Count; i++)
        {
            GameObject waypoint = GameObject.CreatePrimitive(PrimitiveType.Sphere);
            waypoint.transform.position = path1[i];
            Collider collider = waypoint.GetComponent<Collider>();
            collider.enabled = false;
        }
        for (int i = 0; i < path2.Count; i++)
        {
            GameObject waypoint = GameObject.CreatePrimitive(PrimitiveType.Sphere);
            waypoint.transform.position = path2[i];
            Collider collider = waypoint.GetComponent<Collider>();
            collider.enabled = false;
        }
        for (int i = 0; i < path3.Count; i++)
        {
            GameObject waypoint = GameObject.CreatePrimitive(PrimitiveType.Sphere);
            waypoint.transform.position = path3[i];
            Collider collider = waypoint.GetComponent<Collider>();
            collider.enabled = false;
        }
    }
	
	// Update is called once per frame
	//void Update () {
    //
    //}

    public List<Vector3> GetNewPath(string name, Vector3 currPos)
    {
        // Might need to force initial car position to be a point on the path
        // TODO : Add option to disable U-Turn
        GameObject vehicle = GameObject.Find(name);
        if (vehicle != null)
        {
            car = (Vehicle)vehicle.GetComponent("Vehicle");
        }
        List<Vector3> newPath = new List<Vector3>();
        int prevPath = car.GetCurrPathID();
        int randPath = UnityEngine.Random.Range(0, 4);
        newPath = DetermineIntersectionPath(newPath, prevPath, randPath);
        int numPoints = newPath.Count;
        car.SetCurrPathID(randPath);

        switch (randPath)
        {
            case 0:
                newPath = CopyVec3ArrayList(newPath, this.path0);
                break;
            case 1:
                newPath = CopyVec3ArrayList(newPath, this.path1);
                break;
            case 2:
                newPath = CopyVec3ArrayList(newPath, this.path2);
                break;
            case 3:
                newPath = CopyVec3ArrayList(newPath, this.path3);
                break;
            default:
                Debug.Log("Error in getNewPath");
                break;
        }

        return newPath;
    }

    public void ExportCarCommands(string name, string dataString, int cmdID)
    {
        CarData dataObj = new CarData();
        dataObj.name = name;
        dataObj.commands = dataString;
        dataObj.ID = cmdID;

        Thread aThread = new Thread(dataObj.ThreadWriteCarData);
        aThread.Start();
        #if UNITY_EDITOR
                UnityEditor.AssetDatabase.Refresh();
        #endif
        //WriteCarData(dataObj);
    }

    private List<Vector3> DetermineIntersectionPath(List<Vector3> path, int prevPathID, int newPathID)
    {
        Vector3 path0Enter = new Vector3(-2f, 1f, 2f);
        // Vector3 left01 = new Vector3(-2f, 1f, 0f);
        Vector3 path1Enter = new Vector3(-2f, 1f, -2f);
        // Vector3 bot01 = new Vector3(0f, 1f, -2f);
        Vector3 path2Enter = new Vector3(2f, 1f, -2f);
        // Vector3 top23 = new Vector3(0f, 1f, 2f);
        Vector3 path3Enter = new Vector3(2f, 1f, 2f);
        // Vector3 right23 = new Vector3(2f, 1f, 0f);
        switch (prevPathID)
        {
            case 0:
                if(newPathID == 0){
                    path.Add(path3Enter);
                }
                break;
            case 1:
                if(newPathID == 3){
                    path.Add(path2Enter);
                }
                break;
            case 2:
                if(newPathID == 2){
                    path.Add(path1Enter);
                }
                break;
            case 3:
                if(newPathID == 1){
                    path.Add(path0Enter);
                }
                break;
            default:
                Debug.LogError("Error in DetermineIntersectionPath");
                break;
        }
        return path;
    }

    private List<Vector3> CopyVec3ArrayList(List<Vector3> newList, List<Vector3> copyList)
    {
        for (int i=0; i<copyList.Count; i++)
        {
            newList.Add(copyList[i]);
        }
        return newList;
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

    private void ReadCarData(string name)
    {
        string filePath = "Assets/"+name+".json";

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

    public void UpdateCar(string name)
    {
        string filePath = "Assets/"+name+"Status.json";
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
                        car.SkipNodes(simQueueLen - loadedData.actionQueue.Length);
                    }
                    // Simulation is ahead
                    else
                    {
                        car.RedoNodes(loadedData.actionQueue.Length - simQueueLen);
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
            path = "Assets/"+data.name+"Control.json";
        #endif
        #if UNITY_STANDALONE
            path = "Assets/"+data.name+"Control.json";
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
        public string name;
        public string commands;
        public int ID;

        public void ThreadWriteCarData()
        {
            string dataString = JsonUtility.ToJson(this);
            Debug.Log(dataString);

            string path = null;
            #if UNITY_EDITOR
                path = "Assets/"+name+"Control.json";
            #endif
            #if UNITY_STANDALONE
                path = "Assets/"+name+"Control.json";
            #endif

            using (FileStream fs = new FileStream(path, FileMode.Create))
            {
                using (StreamWriter writer = new StreamWriter(fs))
                {
                    writer.Write(dataString);
                }
            }
        }
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
