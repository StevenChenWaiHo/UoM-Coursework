package maze;

/** Exception for when a maze structure that is ragged is inputted*/

public class RaggedMazeException extends InvalidMazeException{
    public RaggedMazeException(String message){
        super(message);
    }
}
