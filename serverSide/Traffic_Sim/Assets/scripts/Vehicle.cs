using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.IO;

public class Vehicle : MonoBehaviour {
    public Transform target;
    public float speed;
    public bool isInsideIntersection = false;
    public bool collisionDetected = false;

    private int curr = 0;
    private List<Vector3> currPath;
    private int currPathID;
    private Base_station station;
    private float DEFAULT_SPEED = 3.0f;
    private Vector3 carNormal;
    private int cmdID = 0;
    
    private string export_string;
    private List<string> stringPath;
    private List<string> directions;


    // Use this for initialization
    void Start () {
        // Finding base station (simulation version of forming connection)
        GameObject bstation = GameObject.Find("Base_Station");
        if (bstation != null)
        {
            station = (Base_station)bstation.GetComponent("Base_station");

            InitCar();
            //currPath = station.GetNewPath(name, transform.position);
            //int randPoint = Random.Range(0, currPath.Count);
            //transform.position = currPath[randPoint];
            //curr = randPoint;
        }
        stringPath = new List<string>();
        directions = new List<string>();
	}

    private void InitCar()
    {
        List<Vector3> startPath = new List<Vector3>();
        switch(name)
        {
            case "Pen":
                SetCurrPathID(0);
                startPath.Add(new Vector3(-7f, 1f, 2f));
                startPath.Add(new Vector3(-7f, 1f, -4f));
                startPath.Add(new Vector3(-7f, 1f, -7f));
                startPath.Add(new Vector3(-4f, 1f, -7f));
                startPath.Add(new Vector3(2f, 1f, -7f));
                startPath.Add(new Vector3(2f, 1f, -4f));
                startPath.Add(new Vector3(2f, 1f, -2f));
                break;
            case "Hoodie":
                SetCurrPathID(0);
                startPath.Add(new Vector3(-7f, 1f, -7f));
                startPath.Add(new Vector3(-4f, 1f, -7f));
                startPath.Add(new Vector3(2f, 1f, -7f));
                startPath.Add(new Vector3(2f, 1f, -4f));
                startPath.Add(new Vector3(2f, 1f, -2f));
                break;
            case "Pineapple":
                SetCurrPathID(1);
                startPath.Add(new Vector3(-5f, 1f, -3.5f));
                startPath.Add(new Vector3(-5f, 1f, -2f));
                startPath.Add(new Vector3(-3.5f, 1f, -2f));
                startPath.Add(new Vector3(-2f, 1f, -2f));
                break;
            case "Apple":
                SetCurrPathID(2);
                startPath.Add(new Vector3(7f, 1f, 2.5f));
                startPath.Add(new Vector3(7f, 1f, 7f));
                startPath.Add(new Vector3(2.5f, 1f, 7f));
                startPath.Add(new Vector3(-2f, 1f, 7f));
                startPath.Add(new Vector3(-2f, 1f, 3.5f));
                startPath.Add(new Vector3(-2f, 1f, 2f));
                break;
            case "bigPine":
                SetCurrPathID(2);
                startPath.Add(new Vector3(2.5f, 1f, 7f));
                startPath.Add(new Vector3(-2f, 1f, 7f));
                startPath.Add(new Vector3(-2f, 1f, 3.5f));
                startPath.Add(new Vector3(-2f, 1f, 2f));
                break;
            default:
                Debug.Log("Invalid car name in InitCar");
                break;
        }
        currPath = startPath;
    }

    void CheckIfInsideIntersection()
    {
        if (transform.position.x > -4.0 && transform.position.x < 4.0)
        {
            if(transform.position.z > -4.0 && transform.position.z < 4.0)
            {
                if(isInsideIntersection == false)
                {
                    isInsideIntersection = true;
                    station.AddToQueue(this.name);
                    //Debug.Log(transform.name + " has entered the intersection");
                }

            }
            else if (isInsideIntersection == true)
            {
                isInsideIntersection = false;
                station.RemoveFromQueue(this.name);
            }

        }
        else if (isInsideIntersection == true)
        {
            isInsideIntersection = false;
            station.RemoveFromQueue(this.name);
        }
    }

    void CheckForCollisions(Vector3 targetPoint)
    {
        Vector3 fwd = transform.TransformDirection(Vector3.forward);
        Vector3 targetVector3 = targetPoint - transform.position;
        
        targetVector3.Normalize();
        
        Vector3 scaledTarget = targetVector3;
        scaledTarget.Scale(new Vector3(0.5f, 0.5f, 0.5f));
        //Debug.Log(scaledTarget);

        Debug.DrawRay(transform.position + targetVector3, targetVector3);
        if (Physics.Raycast(transform.position + targetVector3, targetVector3, 1.5f))
        {
            collisionDetected = true;
            speed = 0.0f;
        }
        else
        {
            collisionDetected = false;
            if (!isInsideIntersection)
            {
                speed = DEFAULT_SPEED;
            }
            else if(speed > 0)
            {
                speed = DEFAULT_SPEED;
            }
        }
    }

    // Update is called once per frame
    void Update () {
        if(currPath == null)
        {
            currPath = station.GetNewPath(name, transform.position);
        }

        transform.LookAt(currPath[curr]);
        CheckIfInsideIntersection();
        if(!isInsideIntersection)
        {
            CheckForCollisions(currPath[curr]);
        }
            
        if (transform.position != currPath[curr])
        {
            // Update vehicle's normal vector3
            carNormal = currPath[curr] - transform.position;
            carNormal.Normalize();

            // Move vehicles slightly towards target
            float step = speed * Time.deltaTime;
            transform.position = Vector3.MoveTowards(transform.position, currPath[curr], step);
        }
        // Car has reached a new node
        else
        {
            curr++;
            //station.UpdateCar(name); //check if car is matching real world
            if(curr >= currPath.Count)
            {
                currPath = station.GetNewPath(name, transform.position);
                curr = 0;
                ConvertPathToStringList();
                export_string = ConvertListToString(stringPath);
                station.ExportCarCommands(name, export_string, cmdID++);
            }
        }
	}

    private string ConvertListToString(List<string> string_path)
    {
        string dataString = string_path[0];
        for(int i=1; i<string_path.Count; i++)
        {
            dataString += ","+string_path[i];
        }

        return dataString;
    }

    public void ConvertPathToStringList()
    {
        stringPath.Clear();
        Vector3 normal = new Vector3(carNormal.x, carNormal.y, carNormal.z);
        Vector3 carPosition = new Vector3(transform.position.x, transform.position.y, transform.position.z);
        for(int i=curr; i<currPath.Count; i++)
        {
            DetermineDirection(carPosition, normal, currPath[i]);
            carPosition = currPath[i];
            if(directions.Count > 0)
            {
                normal = DetermineNewNormal(normal, directions[0]);
                for(int j=0; j<directions.Count; j++)
                {
                    stringPath.Add(directions[j]);
                }
            }
        }
    }

    // Called by ConvertPathToString to determine directions needed between nodes
    private void DetermineDirection(Vector3 position, Vector3 normal, Vector3 target)
    {
        directions.Clear();
        if(position.x != target.x)
        {
            if(normal.x == 0)
            {
                if(target.x - position.x < 0)
                {
                    if(normal.z > 0)
                    {
                        directions.Add("LEFT");
                        directions.Add("FORWARD");
                    }
                    if(normal.z < 0)
                    {
                        directions.Add("RIGHT");
                        directions.Add("FORWARD");
                    }
                }
                if(target.x - position.x > 0)
                {
                    if(normal.z > 0)
                    {
                        directions.Add("RIGHT");
                        directions.Add("FORWARD");
                    }
                    if(normal.z < 0)
                    {
                        directions.Add("LEFT");
                        directions.Add("FORWARD");
                    }
                }
            }
            else
            {
                directions.Add("FORWARD");
            }
        }
        if(position.z != target.z)
        {
            if(normal.z == 0)
            {
                if(target.z - position.z < 0)
                {
                    if(normal.x > 0)
                    {
                        directions.Add("RIGHT");
                        directions.Add("FORWARD");
                    }
                    if(normal.x < 0)
                    {
                        directions.Add("LEFT");
                        directions.Add("FORWARD");
                    }
                }
                if(target.z - position.z > 0)
                {
                    if(normal.x > 0)
                    {
                        directions.Add("LEFT");
                        directions.Add("FORWARD");
                    }
                    if(normal.x < 0)
                    {
                        directions.Add("RIGHT");
                        directions.Add("FORWARD");
                    }
                }
            }
            else
            {
                directions.Add("FORWARD");
            }
        }
    }

    private Vector3 DetermineNewNormal(Vector3 normal, string command)
    {
        Vector3 newNormal = new Vector3(0, 0, 0);
        if(command.Equals("FORWARD"))
        {
            newNormal = normal;
        }
        else if(command.Equals("LEFT"))
        {
            if(normal.x > 0)
            {
                newNormal = new Vector3(0, 0, 1);
            }
            else if(normal.x < 0)
            {
                newNormal = new Vector3(0, 0, -1);
            }
            else if(normal.z > 0)
            {
                newNormal = new Vector3(-1, 0, 0);
            }
            else if(normal.z < 0)
            {
                newNormal = new Vector3(1, 0, 0);
            }
        }
        else if(command.Equals("RIGHT"))
        {
            if(normal.x > 0)
            {
                newNormal = new Vector3(0, 0, -1);
            }
            else if(normal.x < 0)
            {
                newNormal = new Vector3(0, 0, 1);
            }
            else if(normal.z > 0)
            {
                newNormal = new Vector3(1, 0, 0);
            }
            else if(normal.z < 0)
            {
                newNormal = new Vector3(-1, 0, 0);
            }
        }
        else
        {
            Debug.LogError("Error in DetermineNewNormal.");
        }

        return newNormal;
    }

    public void SkipNodes(int numNodes)
    {
        // If enough nodes available
        if(curr+numNodes < GetCurrPathLength())
        {
            this.transform.position = currPath[curr+numNodes];
            curr += numNodes;
        }
        else
        {
            Debug.LogError("In SkipNodes, trying to skip more nodes than there are available.");
        }
    }
    
    public void RedoNodes(int numNodes)
    {
        // If enough nodes available
        if(curr >= numNodes)
        {
            this.transform.position = currPath[curr-numNodes];
            curr -= numNodes;
        }
        else
        {
            Debug.LogError("In RedoNodes, trying to redo more nodes than there are available.");
        }
    }
    
    public void ChangeSpeed(float newSpeed)
    {
        speed = newSpeed;
    }

    public int GetCurrPathID()
    {
        return this.currPathID;
    }

    public void SetCurrPathID(int newID)
    {
        this.currPathID = newID;
    }

    public int GetCurrPathLength()
    {
        // TODO - This needs to do path length of FORWARD, left , right queue not point queue
        return currPath.Count;
    }

    public int GetCurr()
    {
        return curr;
    }
}
