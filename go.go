package main
//
import (
   "bufio"
   "errors"
   "fmt"
   "os"
   "strings"
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
      fmt.Println("main")
      panic(err)
   }
   var lines []string
   scanner := bufio.NewScanner(file)
   for scanner.Scan() {
      lines = append(lines, scanner.Text())
   }
   if scanner.Err() != nil {
      fmt.Println("main")
      panic(scanner.Err())
   }
   //
   tic := time.Now()
   for i,puz := range(lines) {
      fmt.Printf("Puzzle number: %d\n", i)
      fmt.Printf("Puzzle: %v\n", puz)
      display(solve(puz, squares, peers, units), squares)
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
func solve(puzzle string, squares []string, peers map[string]strset, units map[string][]string) board {
   // parse_grid functionality
   vals := make(board)
   for i := 0; i < 81; i++ {
      vals[ squares[i] ] = "123456789"
   }
   for i := 0; i < 81; i++ {
      key := squares[i]
      puz_string := puzzle[i:i + 1]
      if puz_string != "." {
         nvals, err := assign(vals, key, puz_string, peers, units)
         if err != nil {
            fmt.Println("solve1")
            panic(err)
         } else {
            vals = nvals
         }
      }
   }
   //
   solved, err := search(vals, peers, units, squares)
   if err != nil {
      fmt.Println("solve2")
      panic(err)
   }
   return solved
}
//
//////////////////////////////////////////////////////////////////////
//
func search(values board, peers map[string]strset, units map[string][]string, squares []string) (board, error) {
   if values == nil {
      fmt.Println("here")
      return nil, errors.New("function search: values undefined")
   }
   //
   solved := true
   for _,sq := range squares {
      if len(values[sq]) != 1 {
         solved = false
      }
   }
   if solved {
      return values, nil
   }
   //
   min := -1
   min_sq := "none"
   for _,sq := range squares {
      if min == -1 || (len(values[sq]) > 1 && len(values[sq]) < min) {
         min_sq = sq
         min = len(values[sq])
      }
   }
   for i,_ := range values[min_sq] {
      assignment, err := assign(copyVals(values), min_sq, values[min_sq][i:i + 1], peers, units)
      if err != nil {
         fmt.Println("search1")
         panic(err)
      }
      searched, err := search(assignment, peers, units, squares)
      if err != nil {
         fmt.Println("search2")
         panic(err)
      }
      if searched != nil {
         return searched, nil
      }
   }
   return nil, errors.New("function search: ended with no solution")
}
//
//////////////////////////////////////////////////////////////////////
//
func copyVals(vals board) board {
   nvals := make(board)
   for k,v := range vals {
      nvals[k] = v
   }
   return nvals
}
//
//////////////////////////////////////////////////////////////////////
//
func assign(values board, square string, d string, peers map[string]strset, units map[string][]string) (board, error) {
   other_vals := strings.Replace(values[square], d, "", -1)
   for i := 0; i < len(other_vals); i++ {
      vals, err := eliminate(values, square, other_vals[ i : i + 1], peers, units)
      if err != nil {
         fmt.Printf("call to eliminate:\n*** %v\n\n%s\n\n%v\n\n%v\n\n%v\n\n", values, square, other_vals[i:i+1], peers, units)
         return nil, errors.New("function assign: elimination failed")
      } else {
         values = vals
      }
   }
   return values, nil
}
//
//////////////////////////////////////////////////////////////////////
//
func eliminate(values board, sq string, d string, peers map[string]strset, units map[string][]string) (board, error) {
   if !strings.Contains(values[sq], d) {
      return values, nil
   }
   //
   values[sq] = strings.Replace(values[sq], d, "", -1)
   if len(values[sq]) == 0 {
      return nil, errors.New("function eliminate: lenght of values[sq] == 0")
   } else if len(values[sq]) == 1 {
      d2 := values[sq]
      for peer,_ := range peers[sq] {
         done, err := eliminate(values, peer, d2, peers, units)
         if err != nil {
            fmt.Println("debug flag 1")
            return nil, errors.New("function eliminate: previous eliminate failed")
         }
         values = done
      }
   }
   //
   for _,u := range units[sq] {
      var dplaces []string
      for i,_ := range u {
         place := string(u[i])
         if strings.Contains(values[place], d) {
            dplaces = append(dplaces, place)
         }
      }
      //
      if len(dplaces) == 0 {
         fmt.Println("debug flat 2")
         return nil, errors.New("function eliminate: length of dplaces is 0")
      } else if len(dplaces) == 1 {
         if new_vals, err := assign(values, dplaces[0], d, peers, units); err != nil {
            fmt.Println("debug flag 3")
            return nil, errors.New("function eliminate: assignment failed")
         } else {
            values = new_vals
         }
      }
   }
   //
   return values, nil
}
//
//////////////////////////////////////////////////////////////////////
//
func display(b board, squares []string) {
   var s string = ""
   for i := 0; i < 81; i++ {
      s += b[ squares[i] ] + " "
      if i % 3 == 0 {
         s += "| "
      }
      if i % 9 == 0 {
         s += "\n---------------------------------\n"
      }
   }
   fmt.Println(s)
}
//
// End of file
