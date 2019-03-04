Sub stockvolume():

    'goes through each tab in the workbook
    Dim Tabs As Worksheet
        For Each Tabs In ActiveWorkbook.Worksheets
    Tabs.Activate
        LastRow = Tabs.Cells(Rows.Count, 1).End(xlUp).Row

    'set variables
    Dim ticker As String
    Dim volume As Double
    volume = 0
    
    Dim i As Long
    
    'generate the header name for the ticker and total volume
    Cells(1, 9).Value = "Ticker Symbol"
    Cells(1, 10).Value = "Total Stock Volume"

    'set a table to keep track of ticker symbol
    Dim summary_table_row As Integer
    summary_table_row = 2

    'loops through all ticker symbols
        For i = 2 To LastRow
        
        'Check if we are still within the same credit card brand, if it is not...
            If Cells(i + 1, 1).Value <> Cells(i, 1).Value Then
            
            'to set the ticker symbol
            ticker = Cells(i, 1).Value
            'add the volume
            volume = volume + Cells(i, 7).Value
            
            'show the ticker and the volume in the summary table
            range("I" & summary_table_row).Value = ticker
            range("J" & summary_table_row).Value = volume
            
            'add one to the summary table row
            summary_table_row = summary_table_row + 1
            
            'resets the volume total
            volume = 0
    
            Else
            
            'add to the volume
            volume = volume + Cells(i, 7).Value
            
            'close if
            End If
            
        'close loops
        Next i
    Next Tabs



End Sub
