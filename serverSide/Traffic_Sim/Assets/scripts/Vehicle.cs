﻿using System.Collections;
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
    private bool checkingCollision = false;
    private Vector3 carNormal;


    // Use this for initialization
    void Start () {
        // Finding base station (simulation version of forming connection)
        GameObject bstation = GameObject.Find("Base_Station");
        if (bstation != null)
        {
            station = (Base_station)bstation.GetComponent("Base_station");


            currPath = station.GetNewPath(name, transform.position);
            int randPoint = Random.Range(0, currPath.Count);
            transform.position = currPath[randPoint];
            curr = randPoint;
        }
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
        checkingCollision = true;
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
        carNormal = currPath[curr] - transform.position;
        carNormal.Normalize();

        transform.LookAt(currPath[curr]);
        CheckIfInsideIntersection();
        if(!isInsideIntersection)
        {
            CheckForCollisions(currPath[curr]);
        }
            
        if (transform.position != currPath[curr])
        {
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
                Debug.Log("Getting new path");
                currPath = station.GetNewPath(name, transform.position);
                List<string> export_path = ConvertPathToString();
                ExportStringPath(export_path);
                curr = 0;
            }
        }
	}

    private void ExportStringPath(List<string> string_path)
    {
        Debug.Log(string_path.Count);
        string dataString = JsonUtility.ToJson(string_path);

        string path = null;
        #if UNITY_EDITOR
            path = "Assets/car_path.json";
        #endif
        #if UNITY_STANDALONE
            path = "Assets/car_path.json";
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

    public List<string> ConvertPathToString()
    {
        // TODO
        List<string> stringPath = new List<string>();
        List<string> newCommands;
        Vector3 normal = carNormal;
        for(int i=curr; i<currPath.Count; i++)
        {
            newCommands = DetermineDirection(transform.position, normal, currPath[curr]);
            normal = DetermineNewNormal(normal, newCommands[0]);
            for(int j=0; j<newCommands.Count; j++)
            {
                stringPath.Add(newCommands[j]);
            }
            newCommands.Clear();
        }
        return stringPath;
    }

    // Called by ConvertPathToString to determine directions needed between nodes
    private List<string> DetermineDirection(Vector3 position, Vector3 normal, Vector3 target)
    {
        // TODO
        List<string> directions = new List<string>();
        if(position.x != target.x)
        {
            if(normal.x == 0)
            {
                if(target.x - position.x < 0)
                {
                    if(normal.z > 0)
                    {
                        directions.Add("LEFT");
                        directions.Add("UP");
                    }
                    if(normal.z < 0)
                    {
                        directions.Add("RIGHT");
                        directions.Add("UP");
                    }
                }
                if(target.x - position.x > 0)
                {
                    if(normal.z > 0)
                    {
                        directions.Add("RIGHT");
                        directions.Add("UP");
                    }
                    if(normal.z < 0)
                    {
                        directions.Add("LEFT");
                        directions.Add("UP");
                    }
                }
            }
            else
            {
                directions.Add("UP");
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
                        directions.Add("UP");
                    }
                    if(normal.x < 0)
                    {
                        directions.Add("LEFT");
                        directions.Add("UP");
                    }
                }
                if(target.z - position.z > 0)
                {
                    if(normal.x > 0)
                    {
                        directions.Add("LEFT");
                        directions.Add("UP");
                    }
                    if(normal.x < 0)
                    {
                        directions.Add("RIGHT");
                        directions.Add("UP");
                    }
                }
            }
            else
            {
                directions.Add("UP");
            }
        }
        return directions;
    }

    private Vector3 DetermineNewNormal(Vector3 normal, string command)
    {
        // TODO
        Vector3 newNormal = new Vector3(0, 0, 0);
        if(command.Equals("UP"))
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
                newNormal = new Vector3(1, 0, 0);
            }
            else if(normal.z < 0)
            {
                newNormal = new Vector3(-1, 0, 0);
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
                newNormal = new Vector3(-1, 0, 1);
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
        // TODO - This needs to do path length of UP, left , right queue not point queue
        return currPath.Count;
    }

    public int GetCurr()
    {
        return curr;
    }
}
