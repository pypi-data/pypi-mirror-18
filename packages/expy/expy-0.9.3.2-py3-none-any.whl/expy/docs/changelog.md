# todo
- todo: format text draw function

# 0.9.3.2
- Fix the error when running `sendTrigger` without available port.
- Fix the error when setting.txt doesn't exist.
- Fix the error of `import pyglet`

# 0.9.3.1
- Add the parameter "winsize" to `start`
- fix the remained time after run `suspend` 

# 0.9.3
- Press F12 to suspend the program, and press anykey to continue.
- `recordSound_tofile` and `recordSound` allowed press F12 to suspend and ESC to quit.
- Add the parameter "block" to `playSound`
- Now the `getPos` function can use more position's benchmarks: center(default), upper_left, upper_right, lower_left, lower_right, upper_center, left_center, lower_center, right_center
- All the `drawXXX` functions support the "benchmark" parameter 
- Custom fonts size in setting.txt
- Remove `drawFix`,`drawWord`
- 'sendTrigger' function
- Add the parameter "feedback" to `recordSound`

---
# 0.9.1
First released version