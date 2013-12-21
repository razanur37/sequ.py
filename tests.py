#!/usr/bin/python3
# Copyright © 2013 Bart Massey & Geoff Maggi
# Modified by Casey English

# Runs the list of tests below.

import subprocess, sys

from colorama import init, Fore, Style
init(autoreset=True)

headers=19

tests = []
# No Args Test, Maybe print help instead?
tests.append(['Header', 'No Arg Tests'])
tests.append(['','Error'])

# 1 Arg Tests, Should count from 0-arg by 1
tests.append(['Header', '1 Arg Tests'])
tests.append(['3','1 2 3'])
tests.append(['0.8',''])
tests.append(['-2',''])
tests.append(['a','a'])

# 2 arg tests, should count from arg1-arg2 by 1
tests.append(['Header', '2 Arg Tests'])
tests.append(['a 1','Error'])
tests.append(['1 b','Error'])
tests.append(['1 tree','Error'])
tests.append(['2 1',''])
tests.append(['1 1','1'])
tests.append(['1 3','1 2 3'])
tests.append(['-1 1','-1 0 1'])
tests.append(['-1.2 2.22','-1.2 -0.2 0.8 1.8'])
tests.append(['0.000000001 0.1','0.000000001'])

# 3 arg tests, should count from arg1-arg3 by arg2
tests.append(['Header', '3 Arg Tests'])
tests.append(['1 -1 3','']) #infinite loop
tests.append(['-10 10 5','-10 0'])
tests.append(['1 -1 -1','1 0 -1'])
tests.append(['1 -1 0','1 0'])
tests.append(['1 2 3 4 5','Error'])
tests.append(['1 1 3 2 1 2 3 4','Error'])
tests.append(['-0.1 0.1 1','-0.1 0.0 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.0'])

# Float Tests
tests.append(['Header', 'Float Tests'])
tests.append(['.6 .1 .8','0.6 0.7 0.8'])
tests.append(['.6 1.8','0.6 1.6'])
tests.append(['.6 .8','0.6'])
tests.append(['0.6 0.1 0.8','0.6 0.7 0.8'])
tests.append(['0.1 0.99 1.99','0.10 1.09'])
tests.append(['10.8 0.1 10.96','10.8 10.9'])
tests.append(['0.1 -0.1 -0.11','0.1 0.0 -0.1'])
tests.append(['0.8 1e-1 0.9','0.8 0.9'])
tests.append(['0.6 0.1 0.7100000000','0.6 0.7'])
tests.append(['0.6 1e-2 0.62','0.60 0.61 0.62'])
tests.append(['0.69999 1e-7 0.6999901','0.6999900 0.6999901'])

# EQ-Width (-w) Tests
tests.append(['Header', '--equal-width (-w) Tests'])
tests.append(['-w 1 -1 -1','01 00 -1'])
tests.append(['-w -.1 .1 .11','-0.1 00.0 00.1'])
tests.append(['-w 1 3.0','1 2 3'])
tests.append(['-w .8 1e-2 .81','0.80 0.81'])
tests.append(['-w 1 .5 2','1.0 1.5 2.0'])
tests.append(['-w +1 2','1 2'])
tests.append(['-w "    .1"  "    .1"','0.1'])
tests.append(['-w 9 0.5 10','09.0 09.5 10.0'])
tests.append(['-w 999 1e3','0999 1000'])
tests.append(['-w -1 1.0 0','-1 00'])
tests.append(['-w 10 -.1 9.9','10.0 09.9'])

# Pad tests (-p)
tests.append(['Header', '--pad (-p) Tests'])
tests.append(['-p ab 1 -1 -1','Error'])
tests.append(['-p a 1 -1 -1','a1 a0 -1'])
tests.append(['-p a -.1 .1 .11','-0.1 a0.0 a0.1'])
tests.append(['-p a 1 3.0','1 2 3'])
tests.append(['-p a .8 1e-2 .81','0.80 0.81'])
tests.append(['-p a 1 .5 2','1.0 1.5 2.0'])
tests.append(['-p a +1 2','1 2'])
tests.append(['-p a "    .1"  "    .1"','0.1'])
tests.append(['-p a 9 0.5 10','a9.0 a9.5 10.0'])
tests.append(['-p a 999 1e3','a999 1000'])
tests.append(['-p a -1 1.0 0','-1 a0'])
tests.append(['-p a 10 -.1 9.9','10.0 a9.9'])

#tests.append(['-w -1e-3 1','-0.001 00.999'])
#tests.append(['-w -1e-003 1','-0.001 00.999'])
#tests.append(['-w -1.e-3 1','-0.001 00.999'])
#tests.append(['-w -1.0e-4 1','-0.00010 00.99990'])

# Custom format tests (-f)
tests.append(['Header', '--format (-f) Tests'])
tests.append(['-f %2.1f 1.5 .5 2','1.5 2.0'])
tests.append(['-f %0.1f 1.5 .5 2','1.5 2.0'])
tests.append(['-f %.1f  1.5 .5 2','1.5 2.0'])
#tests.append(['-f %3.0f 1 2','/s/s1/s/s2'])
#tests.append(['-f %-3.0f 1 3','1/s/s2/s/s3'])
#tests.append(['-f %+3.0f 1 3','/s+1/s+2/s+3'])
tests.append(['-f %0+3.0f 1 2','+01 +02'])
tests.append(['-f %0+.0f 1 2','+1 +2'])
#tests.append(['-f %%%g%% 1','%1%'])
#tests.append(['-f %%g 1','Error'])
tests.append(['-f % 1','Error'])
#tests.append(['-f %g% 1','Error'])
tests.append(['-f "" 1 3','1 2 3'])
#tests.append(['-f %g%g 1','Error'])

# Test zero trimming
tests.append(['Header', 'Zero Trimming Tests'])
tests.append(['000 2','0 1 2'])
tests.append(['000 02','0 1 2'])
tests.append(['00 02','0 1 2'])
tests.append(['0 02','0 1 2'])

# ROMAN (-F ROMAN) Tests
tests.append(['Header', '--format-word (-F) ROMAN Tests'])
tests.append(['-F ROMAN 10', 'I II III IV V VI VII VIII IX X'])
tests.append(['-F ROMAN 5 15', 'V VI VII VIII IX X XI XII XIII XIV XV'])
tests.append(['-F ROMAN 100 5 150', 'C CV CX CXV CXX CXXV CXXX CXXXV CXL CXLV CL'])
tests.append(['-F ROMAN 10 -1 1', 'X IX VIII VII VI V IV III II I'])
tests.append(['-F ROMAN 4000', 'Error'])
tests.append(['-F ROMAN 1 4000', 'Error'])
tests.append(['-F ROMAN 1 10 4000', 'Error'])
tests.append(['-F ROMAN 10 -1 0', 'Error'])

# roman (-F roman) Tests
tests.append(['Header', '--format-word (-F) roman Tests'])
tests.append(['-F roman 10', 'i ii iii iv v vi vii viii ix x'])
tests.append(['-F roman 5 15', 'v vi vii viii ix x xi xii xiii xiv xv'])
tests.append(['-F roman 100 5 150', 'c cv cx cxv cxx cxxv cxxx cxxxv cxl cxlv cl'])
tests.append(['-F roman 10 -1 1', 'x ix viii vii vi v iv iii ii i'])
tests.append(['-F roman 4000', 'Error'])
tests.append(['-F roman 1 4000', 'Error'])
tests.append(['-F roman 1 10 4000', 'Error'])
tests.append(['-F roman 10 -1 0', 'Error'])

# arabic (-F arabic) Tests
tests.append(['Header', '--format-word (-F) arabic Tests'])
tests.append(['-F arabic -10 10 5','-10 0'])
tests.append(['-F arabic 1 -1 -1','1 0 -1'])
tests.append(['-F arabic 1 -1 0','1 0'])
tests.append(['-F arabic -0.1 0.1 1','Error'])

# alpha (-F alpha) Tests
tests.append(['Header', '--format-word (-F) alpha Tests'])
tests.append(['-F alpha d', 'a b c d'])
tests.append(['-F alpha b f', 'b c d e f'])
tests.append(['-F alpha l a', ''])
tests.append(['-F alpha a 3 z', 'a d g j m p s v y'])
tests.append(['-F alpha d -1 a', 'd c b a'])
tests.append(['-F alpha z -3 a', 'z w t q n k h e b'])
tests.append(['-F alpha a 30 z', 'a'])
tests.append(['-F alpha a .5 z', 'Error'])
tests.append(['-F alpha a 1 aa', 'Error'])

# ALPHA (-F ALPHA) Tests
tests.append(['Header', '--format-word (-F) ALPHA Tests'])
tests.append(['-F ALPHA D', 'A B C D'])
tests.append(['-F ALPHA B F', 'B C D E F'])
tests.append(['-F ALPHA L A', ''])
tests.append(['-F ALPHA A 3 Z', 'A D G J M P S V Y'])
tests.append(['-F ALPHA D -1 A', 'D C B A'])
tests.append(['-F ALPHA Z -3 A', 'Z W T Q N K H E B'])
tests.append(['-F ALPHA A 30 Z', 'A'])
tests.append(['-F ALPHA A .5 Z', 'Error'])
tests.append(['-F ALPHA A 1 AA', 'Error'])

# float (-F float) Tests
tests.append(['Header', '--format-word (-F) float Tests'])
tests.append(['-F float -10 10 5','-10.0 0.0'])
tests.append(['-F float 1 -1 -1','1.0 0.0 -1.0'])
tests.append(['-F float 1 -1 0','1.0 0.0'])
tests.append(['-F float -0.1 0.1 1','-0.1 0.0 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.0'])

for i in range(len(tests)):
	if ("Header"==tests[i][0]):
		continue
	tests[i][1] = tests[i][1].replace(' ', '\n')

# Separator tests (-s)
tests.append(['Header', '--separator (-s) Tests'])
tests.append(['-s "," 1 3','1,2,3'])
tests.append(['-s "," 1 1','1'])
tests.append(['-s ",," 1 3','1,,2,,3'])
tests.append(['-s "\n" 1 3','1\n2\n3'])
tests.append(['-s "\n\t" 1 3','1\n\t2\n\t3'])

# Words tests (-W)
tests.append(['Header', '--words (-W) Tests'])
tests.append(['-W 1 3','1 2 3'])
tests.append(['-W 1 1','1'])

# Pad-spaces tests (-P)
tests.append(['Header', '--pad-spaces (-P) Tests'])
tests.append(['-P 1 -1 -1',' 1\n 0\n-1'])
tests.append(['-P -.1 .1 .11','-0.1\n 0.0\n 0.1'])
tests.append(['-P 1 3.0','1\n2\n3'])
tests.append(['-P .8 1e-2 .81','0.80\n0.81'])
tests.append(['-P 1 .5 2','1.0\n1.5\n2.0'])
tests.append(['-P +1 2','1\n2'])
tests.append(['-P "    .1"  "    .1"','0.1'])
tests.append(['-P 9 0.5 10',' 9.0\n 9.5\n10.0'])
tests.append(['-P 999 1e3',' 999\n1000'])
tests.append(['-P -1 1.0 0','-1\n 0'])
tests.append(['-P 10 -.1 9.9','10.0\n 9.9'])

# Number-lines tests (-n)
tests.append(['Header', '--number-lines (-n) Tests'])
tests.append(['-n test-file.txt 1' , '1 Test 1\n2 Test 2\n3 Test 3\n4 Test 4\n5 Test 5'])
tests.append(['-n test-file.txt 1 5', '1 Test 1\n6 Test 2\n11 Test 3\n16 Test 4\n21 Test 5'])
tests.append(['-n test-file.txt 1 -1', '1 Test 1\n0 Test 2\n-1 Test 3\n-2 Test 4\n-3 Test 5'])
tests.append(['-n test-file.txt 1 1 10', 'Error'])
tests.append(['-n bad-file.txt 1', 'Error'])
tests.append(['-n bad-file.txt 1 5', 'Error'])

passes = 0
xfails = 0
fails = 0

print('Running Test Suite with ' + str(len(tests)-headers) + ' tests!')

for i in range(len(tests)): #run the tests!
	if ("Header"==tests[i][0]):
		tests[i][1] = tests[i][1].center(60)
		print()
		print(tests[i][1])
		continue
	test = repr(tests[i][0])
	test = test.rstrip("'") #remove the ' created by repr
	test = test.lstrip("'") #remove the ' created by repr
	testText = 'sequ.py ' + test
	print(testText.ljust(40) + '===>'.ljust(12),end='')
	
		
	try:
		p = subprocess.check_output('python3 sequ.py '+tests[i][0], universal_newlines=True, shell=True) #Need universal_newlines=True for cross platform
	except Exception:
		if("Error"==tests[i][1]):
			print(Fore.YELLOW + Style.BRIGHT + 'Expected Error'.ljust(20))
			print(Fore.RESET + Style.RESET_ALL + '', end='')
			xfails += 1
		else:
			print(Fore.RED + Style.BRIGHT + 'Unexpected Error'.ljust(20))
			print(Fore.RESET + Style.RESET_ALL + '', end='')
			fails += 1
	else:
		p = p.rstrip(' ');
		if tests[i][1]:
			tests[i][1] += '\n'
		if(p==tests[i][1]):
			print(Fore.GREEN + Style.BRIGHT + 'Pass!'.ljust(20))
			print(Fore.RESET + Style.RESET_ALL + '', end='')
			passes += 1
		else:
			print(Fore.RED + Style.BRIGHT + 'Fail!'.ljust(20))
			print(Fore.RESET + Style.RESET_ALL + '', end='')
			fails += 1

if fails > 0:
	color = Fore.RED
else:
	color = Fore.GREEN

print()
print(color + '-' * 15)
print(color + 'Test Results')
if fails > 0:
	print(color + 'TEST FAILURE - CONSULT LOGS FOR MORE INFO')
else:
	print(color + 'All tests passed!')
print(color + 'Total tests: ' + str(len(tests)-headers))
print(color + 'Pass: ' + str(passes))
print(color + 'XFail: ' + str(xfails))
print(color + 'Fail: ' + str(fails))
print(color + '-' * 15)
print(Fore.RESET + Style.RESET_ALL + '', end='')
		
sys.exit(0)
