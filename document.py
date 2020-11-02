
import os 

if(not os.path.exists('hiscore.txt')):
        with open('hiscore.txt','w') as file:
            file.write('0')

a = '1'
    
#Check hiscore text from file

with open('emotion.txt', 'w') as file :
    file.write('123')

file = open('emotion.txt','w')

file.write(a)