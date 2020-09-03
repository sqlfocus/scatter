package main


import (
	"fmt"
	"os"
)


func for_format_1() {
	var s, sep string
	//三段式用法: initialization; condition; post
	for i := 1; i < len(os.Args); i++ {
		s += sep + os.Args[i]
		sep = " "
	}
	fmt.Println(s)
}

func for_format_2() {
	var s, sep string
	//借助range遍历某数据区间
	for index,arg := range(os.Args[1:]) {
		s += sep + arg
		sep = " "

		index = index    //just for compiler happay
	}
	fmt.Println(s)
}

//go run for.go two param
func main() {
	for_format_1()
	for_format_2()
}
