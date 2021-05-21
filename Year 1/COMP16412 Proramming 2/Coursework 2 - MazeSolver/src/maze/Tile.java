package maze;

import java.io.Serializable;

/** Tile class to hold tile type*/

public class Tile implements Serializable{
    private Type type;

    /** Private tile constructor
    @param t Type of tile*/
    private Tile(Type t){
        type = t;
    }

    /** Create tile instance using char
    @param c Character of the type of the tile
    @return A tile instance with the specified type*/
    protected static Tile fromChar(char c){
        switch(c){
            case '#':
                return new Tile(Type.WALL);
            case '.':
                return new Tile(Type.CORRIDOR);
            case 'e':
                return new Tile(Type.ENTRANCE);
            case 'x':
                return new Tile(Type.EXIT);
            default:
                System.out.print("\nUnknow character in Text file");
                return null;
        }
    }

    /** Get the type of the tile
    @return The type of the tile*/
    public Type getType(){
        return type;
    }

    /** Return the boolean value of navigability
    @return The boolean value of navigability*/
    public boolean isNavigable(){
        switch(type){
            case WALL:
                return false;
            case CORRIDOR:
                return true;
            case ENTRANCE:
                return true;
            case EXIT:
                return true;
            default:
                System.out.print("\nUnknown character in maze");
                return false;
        }
    }

    /** Return the char of the type of the tile
    @return The char of the type of the tile*/
    public String toString(){
        switch(type){
            case WALL:
                return "#";
            case CORRIDOR:
                return ".";
            case ENTRANCE:
                return "e";
            case EXIT:
                return "x";
            default:
                System.out.print("\nUnknown character in maze");
                return null;
        }
    }

    /**Tile type constants*/

    public enum Type{
        CORRIDOR,ENTRANCE,EXIT,WALL
    }

}
