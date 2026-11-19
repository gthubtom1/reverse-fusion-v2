package main

import (
	"fmt"
	"os"
)

// serial: 16 hex chars; last byte is XOR checksum of first 15
func valid(s string) bool {
	if len(s) != 16 {
		return false
	}
	sum := byte(0)
	for i := 0; i < 15; i++ {
		sum ^= hexVal(s[i])
	}
	return sum == hexVal(s[15])
}

func hexVal(c byte) byte {
	switch {
	case c >= '0' && c <= '9':
		return c - '0'
	case c >= 'a' && c <= 'f':
		return c - 'a' + 10
	default:
		return 0xFF
	}
}

func main() {
	if len(os.Args) < 2 {
		fmt.Println("INVALID")
		return
	}
	if valid(os.Args[1]) {
		fmt.Println("VALID")
	} else {
		fmt.Println("INVALID")
	}
}
