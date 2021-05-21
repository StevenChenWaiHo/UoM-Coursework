package maze.routing;

/** Exception for when no route are found*/

public class NoRouteFoundException extends Exception{
    public NoRouteFoundException(String message){
        super(message);
    }
}
