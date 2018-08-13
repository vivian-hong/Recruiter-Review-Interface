import csv
import xlsxwriter
import subprocess

import sys  

reload(sys)  
sys.setdefaultencoding('utf8')

def format(filename):

	excelname = filename.split('/')[len(filename.split('/')) - 1]

	# if we read f.csv we will write f.xlsx
	wb = xlsxwriter.Workbook(filename.replace(".csv",".xlsx"), {'strings_to_numbers': True})
	ws = wb.add_worksheet(excelname.replace(".csv",""))    # your worksheet title here

	# hide unused
	ws.set_default_row(hide_unused_rows=True)

	with open(filename,'r') as csvfile:
		table = csv.reader(csvfile)

		# write each row from the csv file as text into the excel file
		# this may be adjusted to use 'excel types' explicitly (see xlsxwriter doc)
		#bold = wb.add_format({'bold': True})
		last_line = subprocess.check_output(["tail", "-1", filename])

		head = last_line.split(',')
		head_format = wb.add_format()
		head_format.set_align('center')
		head_format.set_align('vcenter')
		head_format.set_bold()
		head_format.set_bg_color('white')
		head_format.set_font_color('blue')
		head_format.set_text_wrap()
		ws.write_row(0, 0, head, head_format)
		ws.insert_image(0, 3, 'ITA-logo.png',{'x_scale': 0.3, 'y_scale': 0.3})

		categories_format = wb.add_format()
		categories_format.set_align('center')
		categories_format.set_align('vcenter')
		categories_format.set_bold()
		categories_format.set_bg_color('gray')
		categories_format.set_top(5)
		categories_format.set_top_color('blue')

		categories = next(table)

		ws.set_column('A:A',15)
		if len(categories) == 4:
			ws.set_column('E:XFD', None, None, {'hidden': True})
			ws.set_column('B:B',40)
			ws.set_column('C:C',20)
			ws.set_column('D:D',20)
		elif len(categories) == 5:
			ws.set_column('F:XFD', None, None, {'hidden': True})
			ws.set_column('B:B',20)
			ws.set_column('C:C',15)
			ws.set_column('D:D',30)
			ws.set_column('E:E',25)		
		elif len(categories) == 6:
			ws.set_column('G:XFD', None, None, {'hidden': True})
			ws.set_column('B:B',20)
			ws.set_column('C:C',20)
			ws.set_column('D:D',20)
			ws.set_column('E:E',20)	
			ws.set_column('F:F',20)
		else:
			ws.set_column(to_alphabetic(len(categories)) + ':XFD', None, None, {'hidden': True})
			for i in range(0, len(categories)):
				ws.set_column(to_alphabetic(i) + ':' + to_alphabetic(i), 15)
		ws.set_row(0, 50)
		ws.set_row(1, 40)

		ws.write_row(1, 0, categories, categories_format)

		general_format = wb.add_format()
		general_format.set_bg_color('white')
		general_format.set_text_wrap()
		general_format.set_bottom()
		general_format.set_bottom_color('gray')
		general_format.set_align('center')
		i = 2
		for row in table:
			ws.write_row(i, 0, row, general_format)
			i += 1
	# ITA logo as header
	header = '&L&G'
	ws.set_margins(top=2.3)

	ws.set_header(header, {'image_left': 'ITA-logo.png'})

	# last line as footer
	ws.set_footer(last_line)

	wb.close()

def to_alphabetic(i,base=26):
    if base < 0 or 62 < base:
        raise ValueError("Invalid base")

    if i < 0:
        return '-'+to_alphabetic(-i-1)

    quot = int(i)/base
    rem = i%base
    if rem < 26:
        letter = chr( ord("A") + rem)
    elif rem < 36:
        letter = str( rem-26)
    else:
        letter = chr( ord("a") + rem - 36)
    if quot == 0:
        return letter
    else:
        return to_alphabetic(quot-1,base) + letter