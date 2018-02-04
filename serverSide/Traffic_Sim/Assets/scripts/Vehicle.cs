﻿using System.Collections;
using System.Collections.Generic;
using UnityEngine;

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
	
    // Function to get a random path that is not the current path
    int getNewPath()
    {
        int newPathID = 0;

        int rInt = Random.Range(0, 4);
        newPathID += rInt;

        // Alternatively could store ineligible paths whenever path is updated and then check against that
        // Currently all paths are allowed except U-turns
        switch (currPathID)
        {
            case 0:
                if (newPathID == 1)
                    newPathID = getNewPath();
                break;
            case 1:
                if (newPathID == 0)
                    newPathID = getNewPath();
                break;
            case 2:
                if (newPathID == 3)
                    newPathID = getNewPath();
                break;
            case 3:
                if (newPathID == 2)
                    newPathID = getNewPath();
                break;
        }
        return newPathID;
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
        Debug.Log(scaledTarget);

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
        if(name.Equals("Car"))
        {
            Vector3 normalVec = currPath[curr] - transform.position;
            normalVec.Normalize();
            Debug.Log("Normal "+normalVec);
        }
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
            station.UpdateCar(name); //check if car is matching real world
            if(curr >= currPath.Count)
            {
                currPath = station.GetNewPath(name, transform.position);
                curr = 0;
            }
        }
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

    public void SetCurrPathID(int newID)
    {
        this.currPathID = newID;
    }

    public int GetCurrPathLength()
    {
        // TODO - This needs to do path length of forward, left , right queue not point queue
        return currPath.Count;
    }

    public int GetCurr()
    {
        return curr;
    }
}
