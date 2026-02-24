; This code automatically fills solution on website https://sudoku.com/
Func solve()
	; --- Sudoku Solution Data ---
	Local $solution[9][9] = [[7, 4, 9, 3, 1, 2, 8, 6, 5], [6, 1, 2, 9, 5, 8, 3, 7, 4], [3, 5, 8, 6, 7, 4, 1, 2, 9], [4, 3, 5, 7, 8, 1, 2, 9, 6], [2, 7, 6, 4, 3, 9, 5, 8, 1], [9, 8, 1, 5, 2, 6, 7, 4, 3], [1, 9, 3, 2, 4, 7, 6, 5, 8], [8, 6, 7, 1, 9, 5, 4, 3, 2], [5, 2, 4, 8, 6, 3, 9, 1, 7]]

	; Give yourself 3 seconds to switch to the browser window after running
	WinActivate("Daily Sudoku - Fresh free puzzles 24/7 — Mozilla Firefox")
	Sleep(800)
	Send("^{HOME}")
	Sleep(200)
	MouseMove(1021, 122, 5)
	MouseClick("left")
	Sleep(900)
	MouseMove(767, 372, 5)
	MouseClick("left")
	Sleep(800)
	MouseMove(772, 563, 5)
	MouseClick("left")
	Sleep(2000)
	; --- Execution Loop ---
	For $r = 0 To 8
		For $c = 0 To 8
			; Send the number from the array
			Send($solution[$r][$c])
			
			; Short delay to ensure the canvas registers the input
			Sleep(50) 

			; Navigation Logic
			If $c < 8 Then
				; Move right to the next cell
				Send("{RIGHT}")
			ElseIf $r < 8 Then
				; End of row reached: Move down and back to the start of the next row
				Send("{DOWN}")
				For $i = 1 To 8
					Send("{LEFT}")
				Next
			EndIf
			
			; Small delay between movements
			Sleep(50)
		Next
	Next
	Sleep(2000)
	;
	return 1;

EndFunc
For $i = 0 To 8
	Local $sum = solve()
Next
MsgBox(0, "Done", "Done")