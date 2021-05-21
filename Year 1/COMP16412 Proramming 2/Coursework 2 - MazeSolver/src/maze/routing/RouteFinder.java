package maze.routing;

import maze.*;
import java.util.Stack;
import java.util.List;
import java.util.ArrayList;

import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.io.Serializable;

import java.io.IOException;
import java.io.FileNotFoundException;
import java.io.StreamCorruptedException;

/* RouteFinder class holds the logics of solving maze*/

public class RouteFinder implements Serializable{
    private Maze maze;
    private Stack<Tile> route = new Stack<Tile>();
    private List<Tile> explored = new ArrayList<Tile>();
    private boolean finished;

    /** RouteFinder class  constructor
    @param m The maze to solve*/
    public RouteFinder(Maze m){
        maze = m;
        finished = false;
    }

    /** Get the maze in RouteFinder
    @return The maze in RouteFinder*/
    public Maze getMaze(){
        return maze;
    }

    /** Get the solved/solving route in RouteFinder
    @return The solved/solving route in RouteFinder*/
    public List<Tile> getRoute(){
        return route;
    }

    /** Get boolean finished in RouteFinder
    @return Boolean finished in RouteFinder*/
    public boolean isFinished(){
        return finished;
    }

    /** Load object RouteFinder from file
    @param path The path to the File
    @return The RouteFinder object stored in file
    @throws java.io.FileNotFoundException
    @throws java.lang.ClassNotFoundException
    @throws java.io.StreamCorruptedException
    @throws java.io.IOException */
    public static RouteFinder load(String path) throws FileNotFoundException, ClassNotFoundException, StreamCorruptedException, IOException{
        try(
        FileInputStream routeFile = new FileInputStream(path);
        ObjectInputStream routeStream = new ObjectInputStream(routeFile);
        )
        {
            return (RouteFinder) routeStream.readObject();
        } catch(FileNotFoundException e){
            throw e;
        } catch(ClassNotFoundException e){
            throw e;
        } catch(StreamCorruptedException e){
            throw e;
        } catch(IOException e){
            throw e;
        }
    }

    /** Save current RouteFinder objec to a File
    @param path THe path to store file
    @throws java.io.IOException */
    public void save(String path) throws IOException{
        try(
        FileOutputStream routeFile = new FileOutputStream(path);
        ObjectOutputStream routeStream = new ObjectOutputStream(routeFile);
        )
        {
            routeStream.writeObject(this);
        } catch(IOException e){
            throw e;
        }
    }

    /** Move one step to solove the maze
    @return Boolean true when solved
    @throws maze.routing.NoRouteFoundException */
    public boolean step() throws NoRouteFoundException{
        if(!finished){
            if(route.isEmpty()){
                route.push(maze.getEntrance());
                return false;
            }
            ArrayList<Tile> options = new ArrayList<Tile>();
            Tile current = route.peek();
            explored.add(current);
            if(current == maze.getExit()){
                finished = true;
                return true;
            }
            // Find all options from current
            for(Maze.Direction t : Maze.Direction.values()){
                if(maze.getAdjacentTile(current,t).isNavigable() && !explored.contains(maze.getAdjacentTile(current,t))){
                    options.add(maze.getAdjacentTile(route.peek(),t));
                }
            }
            if(options.size() == 0){
                if(route.peek() == maze.getEntrance()){
                    throw new NoRouteFoundException("\nNo routes found");
                }
                route.pop();
                return false;
            }
            // Compare heuristic between options
            Tile minOption = null;
            for(Tile o : options){
                if(heuristic(o) < heuristic(minOption)){
                    minOption = o;
                }
            }
            route.push(minOption);
            return false;
        }
        return true;
    }

    /** Heuristic function to estimate gain
    @param t The tile to compute distance
    @return The displacement between tile and exit*/
    private double heuristic(Tile t){
        if(t == null){
            return Double.POSITIVE_INFINITY;
        }
        int distanceX = maze.getTileLocation(maze.getExit()).getX() - maze.getTileLocation(t).getX();
        int distanceY = maze.getTileLocation(maze.getExit()).getY() - maze.getTileLocation(t).getY();
        return Math.sqrt(distanceX * distanceX + distanceY * distanceY);
    }

    /** Return a string representation of the maze and routes
    @return A string representation of the maze and routes*/
    public String toString(){
        int maxCol = 0;
        String stringMaze = "";
        for(int row = 0; row < maze.getTiles().size(); row++){
            stringMaze += String.valueOf(maze.getTiles().size()-row-1) + "  ";
            maxCol = Math.max(maxCol, maze.getTiles().get(row).size());
            for(int col = 0; col < maze.getTiles().get(row).size(); col++){
                // Print explored path
                if(route.contains(maze.getTiles().get(row).get(col))){
                    stringMaze += "*" + " ";
                }
                // Print route path
                else if(explored.contains(maze.getTiles().get(row).get(col))){
                    stringMaze += "-" + " ";
                }
                else{
                    stringMaze += maze.getTiles().get(row).get(col).toString() + " ";
                }
            }
            stringMaze = stringMaze + "\n";
        }
        stringMaze = stringMaze + "\n";
        for(int j = 0; j < Math.floor(Math.log10(maze.getTiles().size())) + 1; j++){
            stringMaze += " ";
        }
        stringMaze += "  ";
        for(int i = 0; i < maxCol; i++){
            stringMaze += i + " ";
        }
        return stringMaze;
    }
}
