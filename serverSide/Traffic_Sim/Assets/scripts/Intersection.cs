using System;

/// <summary>
/// Class defining intersection characteristics.
/// </summary>
public class Intersection
{
    public string name;
    public Boolean northWest = false;
    public Boolean northEast = false;
    public Boolean southWest = false;
    public Boolean southEast = false;

    public Intersection(string name)
	{
        this.name = name;
	}
}
