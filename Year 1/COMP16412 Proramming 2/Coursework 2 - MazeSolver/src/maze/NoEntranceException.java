package maze;

/** Exception for when a maze structure with no entrances is inputted*/

public class NoEntranceException extends InvalidMazeException{
    public NoEntranceException(String message){
        super(message);
    }
}
