package main

import "fmt"

var heads,tails int = 1,1

//抛硬币统计
func switch_1(coin string) {
	switch coin {
	case "heads":
		heads++
	case "tails":
		tails++
	default:
		fmt.Println("landed on edge!")
	}
}

//无tag的switch，相当于if-else if-else if-else
func switch_2(x int) int {
	switch {
	case x > 0:
		return +1
	default:
		return 0
	case x < 0:
		return -1
	}
}

//go run switch.go
func main() {
	//if - else
	if switch_2(3) == 1 {
		switch_1("heads")
	} else if switch_2(0) == 0 {
		switch_1("tails")
	} else {
		switch_1("no exist)")
	}

	//补充
	switch_1("tails")
	switch_1("no exist)")

	//打印结果
	fmt.Println(heads, " ", tails)
}
