package chess;

public class Rook extends Piece {

    public Rook(PieceColour c){
        colour = c;
        if(c == PieceColour.WHITE){
            setSymbol("♖");
        }
        else{
            setSymbol("♜");   
        }
    }
    
    @Override
    public boolean isLegitMove(int i0, int j0, int i1, int j1){
        int dI,dJ;
        // Rook either Moving Vertically or Horizontally
        if(Math.abs(i1-i0) > 0 ^ Math.abs(j1-j0) > 0){
            // Moving Horizontally
            if(i1 == i0){
                dJ = Math.abs(j1-j0)/(j1-j0);
                dI = 0;
            }
            // Moving Vertically
            else{
                dI = Math.abs(i1-i0)/(i1-i0);
                dJ = 0;
            }
            // Iterate thorugh the Path
            for(int i=i0+dI,j=j0+dJ;i!=i1||j!=j1;i+=dI,j+=dJ){
                // A Piece is Blocking Bishop's Path
                if(Board.hasPiece(i,j)){
                    return false;                
                }
            }
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
        // Moving in Invalid Direction
        else{
           return false; 
        }
    }	
}
