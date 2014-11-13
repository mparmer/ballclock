//Author: Mike Parmer
package main
import "fmt"
import "os"
import "strconv"
import "encoding/json"

var (
	pool				[]int
	pool_orig 	[]int
	min					[]int
	five_min		[]int
	hour				[]int
	bc_run_time	int
	minutes			int
)


//TODO USE Channels (queues) and goroutines instead of lists for the queues

func main() {
	minutes := 0
	balls		:= 0
	//BASIC ARGV CHECKING
	if len(os.Args) < 2 {
		fmt.Println("You must supply at least a number of balls, and/or a number of minutes to run.  Valid ball numbers are 27-127")
		os.Exit(0)
	}
	balls, err := strconv.Atoi(os.Args[1])
	if err != nil {
		fmt.Printf("%d is an invalid number. Valid numbers are 27-127", os.Args[1])
		os.Exit(0)
	}
	if 27 > balls || 127 < balls {
		fmt.Printf("%d is an invalid number. Valid numbers are 27-127", balls)
		os.Exit(0)
	}
	if len(os.Args) > 2 {
		mins, err := strconv.Atoi(os.Args[2])
		if err != nil {
			fmt.Printf("%d is an invalid number. Valid numbers are 27-127", os.Args[2])
			os.Exit(0)
		}
		minutes = mins
	}

	load(balls)
	//fmt.Printf("%d\n",pool)
	op := pool_orig[:]

	bc_run_time += 1
	ball := pool[0]
	pool = pool[1:]
	min_queue(ball)

	if minutes == 0 {
		for !IntArrayEquals(pool,op) { // RUN UNTIL THE INITIAL ORDER IN THE POOL IS REPEATED AND THEN REPORT
			bc_run_time += 1
			ball := pool[0]
			pool = pool[1:]
			min_queue(ball)
		}
		days := bc_run_time / 1440
		fmt.Printf("%d balls cycle after %d days\n",balls,days)
//  END MAIN LOOP
	} else { //RUN TO A CERTAIN AMOUNT OF MINUTES AND REPORT IN JSON FORMAT
		for bc_run_time != minutes {
			bc_run_time += 1
			ball := pool[0]
			pool = pool[1:]
			min_queue(ball)
			
		}

		type myjson struct {
			Min			[]int
			FiveMin []int
			Hour		[]int
			Main		[]int
		}
		
		mj := myjson{min,five_min,hour,pool}
		jj, err := json.Marshal(mj)
		if err != nil {
			fmt.Printf("%s",err.Error())	
		}

		fmt.Printf("%s\n",jj)
		
	}
}

func IntArrayEquals(a []int, b []int) bool {
    if len(a) != len(b) {
        return false
    }
    for i, v := range a {
        if v != b[i] {
            return false
        }
    }
    return true
}

func load(balls int) {
	for i := 1; i < balls+1; i++ {
		pool = append(pool,i)
		pool_orig = append(pool_orig,i)

	}
}

func min_queue(ball int) {
	if len(min) < 4 {
		min = append(min,ball)
	} else {
		pool = append(pool,min[3], min[2], min[1], min[0])
		min = min[0:0]
		five_queue(ball)
	}
}

func five_queue(ball int) {
	if len(five_min) < 11 {
		five_min = append(five_min,ball)
	} else {
		pool = append(pool,five_min[10],five_min[9],five_min[8],five_min[7],five_min[6],five_min[5],five_min[4],five_min[3],five_min[2],five_min[1],five_min[0])
		five_min = five_min[0:0]
		hour_queue(ball)
	}
}


func hour_queue(ball int) {
	if len(hour) < 11 {
		hour = append(hour,ball)
	} else {
		pool = append(pool,hour[10],hour[9],hour[8],hour[7],hour[6],hour[5],hour[4],hour[3],hour[2],hour[1],hour[0],ball)
		hour = hour[0:0]
	}
}
