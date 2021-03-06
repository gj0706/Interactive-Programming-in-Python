# template for "Stopwatch: The Game"
import simplegui
# define global variables
WIDTH = 400
LENGTH = 400
tick_times = 0
INTERVAL = 100
total_stops = 0
success_stops = 0
timer_running = False
tenth_sec = 0

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    global tenth_sec
    min = (t // 100) // 6
    ten_sec = (t // 100) % 6     
    sec = (t // 10) % 10
    tenth_sec = t % 10
    return (str(min) + ":" + str(ten_sec) + str(sec) + "." + str(tenth_sec) )
       
# define event handlers for buttons; "Start", "Stop", "Reset"
def start():
    global timer_running   
    timer_running = True
    timer.start()
    
def stop():
    timer.stop()
    global total_stops, success_stops, d, timer_running
    if timer_running:
        timer_running = False
        total_stops += 1
        if tenth_sec == 0:
            success_stops += 1
def reset():
    timer.stop()
    global tick_times, total_stops, success_stops, timer_running
    total_stops = 0
    tick_times = 0
    success_stops = 0
    
# define event handler for timer with 0.1 sec interval
def tick():
    global tick_times
    tick_times += 1
      
# define draw handler
def draw_time(canvas):
    canvas.draw_text(str(format(tick_times)), [WIDTH / 3, LENGTH / 2], 50, "White")
    canvas.draw_text(str(success_stops) + "/" + str(total_stops), [300, 50], 50, "Red")
# create frame
frame = simplegui.create_frame("Timer", WIDTH, LENGTH)

# register event handlers
timer = simplegui.create_timer(INTERVAL, tick)
frame.set_draw_handler(draw_time)
frame.add_button("Start", start)
frame.add_button("Stop", stop)
frame.add_button("Reset", reset)
# start frame
frame.start()
