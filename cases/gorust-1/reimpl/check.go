package main

import "fmt"

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

func main() {
	cases := []string{"0123456789abcdef", "0123456789abcdea", "abc", "0123456789abcdefx", "ffffffffffffffff", "1111111111111111"}
	ok := true
	for _, c := range cases {
		r := valid(c)
		fmt.Printf("%s -> %v\n", c, r)
		if c=="0123456789abcdef" && !r { ok=false }
		if (c=="0123456789abcdea"||c=="abc"||c=="0123456789abcdefx") && r { ok=false }
		if (c=="ffffffffffffffff"||c=="1111111111111111") && !r { ok=false }
	}
	fmt.Println("ALL_MATCH", ok)
}
