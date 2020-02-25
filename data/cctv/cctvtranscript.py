with open("juli.txt", 'r') as f:
    lst = []
    count = 0
    with open("cctv_transcript.txt", 'w+') as f1:
        for line in f.readlines():
            lst.append(line)
            count += 1
        for num in range(count):
            print('temp'+str(num+101)+' '+lst[num][16:].strip())
            a = 'temp'+str(num+101)+' '+lst[num][16:].strip()
            f1.write('{}\n'.format(a))