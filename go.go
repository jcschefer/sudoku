package main
//
import (
   "fmt"
   "os"
   "bufio"
   "time"
)
//
type strset map[string]bool
type board map[string]string
//
//////////////////////////////////////////////////////////////////////
//
func main() {
   var digits  string = "123456789"
   var rows    string = "ABCDEFGHI"
   var cols    string = digits
   var squares []string = cross(rows, cols)
   //
   var unitlist [][]string
   for i := 0; i < 9; i++ {
      unitlist = append(unitlist, cross(rows, string(cols[i])))
      unitlist = append(unitlist, cross(string(rows[i]), cols))
   }
   rs := []string{"ABC", "DEF", "GHI"}
   cs := []string{"123", "456", "789"}
   for i := 0; i < 3; i++ {
      for j := 0; j < 3; j++ {
         unitlist = append(unitlist, cross(rs[i], cs[j]))
      }
   }
   //
   units := make(map[string][]string)
   for i := 0; i < len(squares); i++ {
      for j := 0; j < len(unitlist); j++ {
         if contains(unitlist[j], squares[i]) {
            units[squares[i]] = unitlist[j]
         }
      }
   }
   //
   peers := make(map[string]strset)
   for _,s := range squares  {
      mypeers := make(strset)
      for _,peer := range units[s] {
         if peer != s {
            mypeers[peer] = true
         }
      }
      peers[s] = mypeers
   }
   //
   file, err := os.Open("puzzles.txt")
   if err != nil {
      panic(err)
   }
   var lines []string
   scanner := bufio.NewScanner(file)
   for scanner.Scan() {
      lines = append(lines, scanner.Text())
   }
   if scanner.Err() != nil {
      panic(scanner.Err())
   }
   //
   tic := time.Now()
   for i,puz := range(lines) {
      fmt.Printf("Puzzle number: %d\n", i)
      fmt.Printf("Puzzle: %v\n", puz)
      display(solve(puz, squares))
   }
   toc := time.Now()
   fmt.Printf("\n\nRuntime: %d seconds", toc.Sub(tic))
}
//
//////////////////////////////////////////////////////////////////////
//
func cross(a string, b string) []string {
   var toReturn []string
   for x := 0; x < len(a); x++ {
      for k := 0; k < len(b); k++ {
         toReturn = append(toReturn, string(a[x]) + string(b[k]))
      }
   }
   return toReturn
}
//
//////////////////////////////////////////////////////////////////////
//
func contains(a []string, b string) bool {
   for x := 0; x < len(a); x++ {
      if a[x] == b {
         return true
      }
   }
   return false
}
//
//////////////////////////////////////////////////////////////////////
//
func solve(puzzle string, squares []string) string {
   // parse_grid functionality
   vals := make(board)
   for _,sq := range squares {
      
   }
}
//
//////////////////////////////////////////////////////////////////////
//
func assign(values board, square string, d string) (board, bool) {
   other_vals = strings.Replace(vals[square], d, "", -1)
   for 
}
//
//////////////////////////////////////////////////////////////////////
//
func display(b string) {
   var s string = ""
   for i := 0; i < 81; i++ {
      s += b[i] + " "
      if i == 3 or i == 6 {
         s += "| "
      }
      if i == 9{
         s += "\n---------------------------------\n"
      }
   }
}
//
// End of file
