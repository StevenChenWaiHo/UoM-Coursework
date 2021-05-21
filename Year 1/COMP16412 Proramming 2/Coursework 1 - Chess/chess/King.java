package chess;

public class King extends Piece {

    public King(PieceColour c){
        colour = c;
        if(c == PieceColour.WHITE){
            setSymbol("♔");
        }
        else{
            setSymbol("♚");   
        }
    }
    
    @Override
    public boolean isLegitMove(int i0, int j0, int i1, int j1){
        // Move 1 Square Vertically, Horizontally or Diagonally
        if(Math.abs((i0+j0)-(i1+j1)) == 1 || (Math.abs(i1-i0) == Math.abs(j1-j0) && Math.abs(i1-i0)== 1)){
            // Have Piece at Destination and No Piece Blocking
            if(Board.hasPiece(i1,j1)){
                // Destination Piece is an Opponent
                if(colour != Board.getPiece(i1,j1).getColour()){
                    return true;                
                }
                // Destination Piece is a Ally
                else{
                    return false;                
                }
            }
            // No Piece at Destination
            else{
                return true;
            }
        }
        else{
            return false;        
        }
    }	
}
