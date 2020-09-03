// Dup1 prints the text of each line that appears more than
// once in the standard input, preceded by its count.
package main

import (
	"bufio"
	"fmt"
	"os"
)

func main() {
	counts := make(map[string]int)      //map类似于hash
	input := bufio.NewScanner(os.Stdin)
	for input.Scan() {                  //读取输入, CTRL+D结束
		counts[input.Text()]++
	}
	// NOTE: ignoring potential errors from input.Err()
	for line, n := range counts {       //输出
		fmt.Printf("%d\t%s\n", n, line)
	}
}
