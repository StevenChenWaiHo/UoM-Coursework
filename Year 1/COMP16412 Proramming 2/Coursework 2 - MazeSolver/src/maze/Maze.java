package maze;

import java.io.BufferedReader;
import java.io.FileReader;
import java.util.List;
import java.util.ArrayList;
import java.io.Serializable;

import java.io.IOException;
import java.io.FileNotFoundException;

/** Maze class to hold the structure of the maze*/

public class Maze implements Serializable{
    private Tile entrance = null;
    private Tile exit = null;
    private List<List<Tile>> tiles = new ArrayList<List<Tile>>();

    /** Maze class private constructor */
    private Maze(){}

        /** Create maze instance using txt file
        @param path File path of the txt file
        @return A maze instance with maze structure given by the txt file
        @throws maze.InvalidMazeException
        @throws java.io.FileNotFoundException
        @throws java.io.IOException */
        public static Maze fromTxt(String path) throws InvalidMazeException, FileNotFoundException, IOException{
            try (
            BufferedReader bufferedReader = new BufferedReader(
            new FileReader(path)
            )
            ) {
                Maze maze = new Maze();
                //Initialize Entrance and Exit
                maze.entrance = null;
                maze.exit = null;

                int rowIndex = 0;

                String line = bufferedReader.readLine();
                int lineLength = line.length();
                // Until End Of File
                while (line != null){
                    if(lineLength != line.length()){
                        throw new RaggedMazeException("\nMaze is ragged");
                    }
                    maze.tiles.add(new ArrayList<Tile>());
                    for(int colIndex = 0; colIndex < line.length(); colIndex++){
                        Tile t;
                        // Char is e
                        if(line.charAt(colIndex) == 'e'){
                            t = Tile.fromChar(line.charAt(colIndex));
                            // Check for multiple entrance
                            if(maze.entrance == null){
                                maze.tiles.get(rowIndex).add(t);
                                try{
                                    maze.setEntrance(t);
                                } catch(IllegalArgumentException e){
                                    throw e;
                                } catch(MultipleEntranceException e){
                                    throw e;
                                }
                            }
                            else{
                                throw new MultipleEntranceException("\nMultiple entrance detected");
                            }
                        }
                        // Char is x
                        else if(line.charAt(colIndex) == 'x'){
                            t = Tile.fromChar(line.charAt(colIndex));
                            // Check for multiple exit
                            if(maze.exit == null){
                                maze.tiles.get(rowIndex).add(t);
                                try{
                                    maze.setExit(t);
                                } catch(IllegalArgumentException e){
                                    throw e;
                                } catch(MultipleExitException e){
                                    throw e;
                                }
                            }
                            else{
                                throw new MultipleExitException("\nMultiple exit detected");
                            }
                        }
                        // Char is a unknown character
                        else if(line.charAt(colIndex) != '.' && line.charAt(colIndex) != '#'){
                            throw new InvalidMazeException("\nUnknown character in txt file");
                        }
                        // Char is . or #
                        else{
                            t = Tile.fromChar(line.charAt(colIndex));
                            maze.tiles.get(rowIndex).add(t);
                        }
                    }
                    rowIndex++;
                    line = bufferedReader.readLine();
                }
                if(maze.entrance == null){
                    throw new NoEntranceException("\nNo entrance detected");
                }
                if(maze.exit == null){
                    throw new NoExitException("\nNo exit detected");
                }
                bufferedReader.close();
                return maze;
            } catch (FileNotFoundException e) {
                throw e;
            } catch (IOException e) {
                throw e;
            }
        }

        /** Get adjacent tile
        @param t Tile of the origin
        @param d Direction to destination
        @return The tile of the direction specified*/
        public Tile getAdjacentTile(Tile t, Direction d){
            int rowDir = 0;
            int colDir = 0;
            switch(d){
                case NORTH:
                rowDir = 1;
                break;
                case SOUTH:
                rowDir = -1;
                break;
                case EAST:
                colDir = 1;
                break;
                case WEST:
                colDir = -1;
                break;
                default:
                System.out.print("Invalid Direction");
            }
            int x = this.getTileLocation(t).getX() + colDir;
            int y = this.getTileLocation(t).getY() + rowDir;
            return this.getTileAtLocation(new Coordinate(x, y));
        }

        /** Get entrance tile from a maze instance
        @return The entrance tile*/
        public Tile getEntrance(){
            return entrance;
        }

        /** Get exit tile from a maze instance
        @return The exit tile*/
        public Tile getExit(){
            return exit;
        }

        /** Get tile at the specified coordinates
        @param c Coordinates of the tile
        @return The tile at the specified coordinates*/
        public Tile getTileAtLocation(Coordinate c){
            if(c.getX() > tiles.get(0).size() - 1 || c.getY() > tiles.size() - 1 || c.getX() < 0 || c.getY() < 0){
                return Tile.fromChar('#');
            }
            return tiles.get(tiles.size() - c.getY() - 1).get(c.getX());
        }

        /** Get coordinates of the tile
        @param t The tile
        @return Coordinates of the tile*/
        public Coordinate getTileLocation(Tile t){
            for(int row = 0; row < tiles.size(); row++){
                for(int col = 0; col < tiles.get(row).size(); col++){
                    if(tiles.get(tiles.size() - row - 1).get(col) == t){
                        return new Coordinate(col, row);
                    }
                }
            }
            return null;
        }

        /** Get tiles from a maze instance
        @return The tiles*/
        public List<List<Tile>> getTiles(){
            return tiles;
        }

        /** Set entrance of a maze instance
        @param t The entrance tile
        @throws maze.MultipleEntranceException
        @throws java.lang.IllegalArgumentException */
        private void setEntrance(Tile t) throws MultipleEntranceException, IllegalArgumentException{
            if(entrance != null){
                throw new MultipleEntranceException("\nMultiple entrance detected");
            }
            for(int col = 0; col < tiles.size(); col++){
                if(tiles.get(col).contains(t)){
                    entrance = t;
                    return;
                }
            }
            throw new IllegalArgumentException("\nSetting entrance not in maze");
        }

        /** Set exit of a maze instance
        @param t The exit tile
        @throws maze.MultipleExitException
        @throws java.lang.IllegalArgumentException */
        private void setExit(Tile t) throws MultipleExitException, IllegalArgumentException{
            if(exit != null){
                throw new MultipleExitException("\nMultiple exit detected");
            }
            for(int col = 0; col < tiles.size(); col++){
                if(tiles.get(col).contains(t)){
                    exit = t;
                    return;
                }
            }
            throw new IllegalArgumentException("\nSetting exit not in maze");
        }


        /** Get the string of the structure of the maze
        @return String of the structure of the maze*/
        public String toString(){
            int maxCol = 0;
            String stringMaze = "";
            for(int row = 0; row < tiles.size(); row++){
                stringMaze += String.valueOf(tiles.size()-row-1) + "  ";
                maxCol = Math.max(maxCol, tiles.get(row).size());
                for(int col = 0; col < tiles.get(row).size(); col++){
                    stringMaze += tiles.get(row).get(col).toString() + " ";
                }
                stringMaze = stringMaze + "\n";
            }
            stringMaze = stringMaze + "\n";
            for(int j = 0; j < Math.floor(Math.log10(tiles.size())) + 1; j++){
                stringMaze += " ";
            }
            stringMaze += "  ";
            for(int i = 0; i < maxCol; i++){
                stringMaze += i + " ";
            }
            return stringMaze;
        }

        /** Coordinate class to hold the coordinates of a tile*/

        public class Coordinate{
            private int x;
            private int y;

            /** Coordinate constructor
            @param x x-coordinates
            @param y y-coordinates*/
            public Coordinate(int x, int y){
                this.x = x;
                this.y = y;
            }

            /** Get x-coordinates of a instance
            @return The x-coordinates of a instance*/
            public int getX(){
                return x;
            }

            /** Get y-coordinates of a instance
            @return The y-coordinates of a instance*/
            public int getY(){
                return y;
            }

            /** Get string format of the coordinates
            @return The x and y coordinates of a instance by the format (x, y)*/
            public String toString(){
                return "(" + x + ", " + y + ")";
            }
        }

        /** Direction constants*/

        public enum Direction{
            NORTH,SOUTH,EAST,WEST
        }
    }
