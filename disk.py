import sys
import matplotlib.pyplot as plt
import numpy as np




class SSTFobject:
    def __init__(self, processNo=-1, distance=-1, visited=False):
        self.processNo = processNo
        self.distance = distance
        self.visited = False


class disk_comparator:
    def __init__(self, name="\0", seek_ops=-1, Seek_Seq=[]):
        self.name = name
        self.seek_ops = seek_ops
        self.Seek_Seq = Seek_Seq


def PlotGraph(Seq, processID, head_pos, algorithm, seek_ops):
    Seq.insert(0, head_pos)
    seqLength = len(Seq)
    Time = [i for i in range(seqLength)]

    data = np.column_stack((Time, Seq))

    if algorithm == "SCAN" or algorithm == "CSCAN":
        labels = ['process{0}'.format(i) for i in processID]
        labels.insert(0, "Head")
        if 499 in Seq:
            index = Seq.index(499)
            labels.insert(index, "Max")
        if 0 in Seq:
            index = Seq.index(0)
            labels.insert(index, "Min")

    else:
        labels = ['process{0}'.format(i) for i in processID]
        labels.insert(0, "Head")

    plt.subplots_adjust(bottom=0.1)
    plt.scatter(data[:, 0], data[:, 1], marker='o')
    plt.plot(Time, Seq, color='green', linestyle='solid', linewidth=3,
             marker='o', markerfacecolor='blue', markersize=12)

    for label, x, y in zip(labels, data[:, 0], data[:, 1]):
        plt.annotate(
            label,
            xy=(x, y), xytext=(-15, 15),
            textcoords='offset points', ha='right', va='bottom',
            bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5),
            arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))

    plt.xlabel("Time")
    plt.ylabel("Position of head")
    plt.title("Seek operations : {}".format(seek_ops), loc='left')
    plt.title(algorithm, loc='right')

    plt.show()


def SaveGraph(Seq, processID, head_pos, algorithm, seek_ops):
    Seq.insert(0, head_pos)
    seqLength = len(Seq)
    Time = [i for i in range(seqLength)]

    data = np.column_stack((Time, Seq))

    if algorithm == "SCAN" or algorithm == "CSCAN":
        labels = ['process{0}'.format(i) for i in processID]
        labels.insert(0, "Head")
        if 499 in Seq:
            index = Seq.index(499)
            labels.insert(index, "Max")
        if 0 in Seq:
            index = Seq.index(0)
            labels.insert(index, "Min")

    else:
        labels = ['process{0}'.format(i) for i in processID]
        labels.insert(0, "Head")

    plt.subplots_adjust(bottom=0.1)
    plt.scatter(data[:, 0], data[:, 1], marker='o')
    plt.plot(Time, Seq, color='green', linestyle='solid', linewidth=3,
             marker='o', markerfacecolor='blue', markersize=12)

    for label, x, y in zip(labels, data[:, 0], data[:, 1]):
        plt.annotate(
            label,
            xy=(x, y), xytext=(-15, 15),
            textcoords='offset points', ha='right', va='bottom',
            bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5),
            arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))

    plt.xlabel("Time")
    plt.ylabel("Position of head")
    plt.title("Seek operations : {}".format(seek_ops), loc='left')
    plt.title(algorithm, loc='right')
    labels = []
    data = np.empty(shape=[0, 2])
    Seq = []

    plt.savefig('public/'+algorithm+'graph.png')
    plt.clf()


def DISK_comparator(obj):
    return obj.distance


def ReqSeq_To_ObjSeq(RequestSeq):
    Object_seq = []
    count = 1

    for i in RequestSeq:
        obj = SSTFobject(count, i)  # i is the distance
        Object_seq.append(obj)
        count = count + 1

    return Object_seq


def SCAN_diskScheduling(x):
    flag = x
    direction = "right"
    reqSeq = []
    s = sys.argv[1]
    ans = ""

    for i in s:
        if(i == " "):
            num = int(ans)
            reqSeq.append(num)
            ans = ""
        else:
            ans += i
    num = int(ans)
    reqSeq.append(num)

    head_pos = int(sys.argv[2])

    Seq = []
    for i in reqSeq:
        Seq.append(i)

    Seq.append(head_pos)

    RequestSeq = []
    RequestSeq = ReqSeq_To_ObjSeq(Seq)  # ReqSeq is list of objects

    disk_size, seek_ops, temp_head_pos = 500, 0, head_pos
    seek_seq = []
    seek_seq_analysis = []
    processID = []

    RequestSeq.sort(key=DISK_comparator, reverse=False)
    Seq.sort()

    index = Seq.index(head_pos)

    if direction == "right":
        i = index + 1
        while i < len(RequestSeq):
            dis = abs(head_pos - RequestSeq[i].distance)
            seek_ops += dis
            head_pos = RequestSeq[i].distance
            seek_seq.append(RequestSeq[i].distance)
            processID.append(RequestSeq[i].processNo)
            i = i + 1

        seek_ops += abs(head_pos - 499)
        head_pos = 499
        seek_seq.append(499)

        i = index - 1
        while i >= 0:
            dis = abs(head_pos - RequestSeq[i].distance)
            seek_ops += dis
            head_pos = RequestSeq[i].distance
            seek_seq.append(RequestSeq[i].distance)
            processID.append(RequestSeq[i].processNo)
            i = i - 1

    else:
        i = index - 1
        while i >= 0:
            dis = abs(head_pos - RequestSeq[i].distance)
            seek_ops += dis
            head_pos = RequestSeq[i].distance
            seek_seq.append(RequestSeq[i].distance)
            processID.append(RequestSeq[i].processNo)
            i = i - 1

        seek_ops += abs(head_pos - 0)
        head_pos = 0
        seek_seq.append(0)

        i = index + 1
        while i < len(RequestSeq):
            dis = abs(head_pos - RequestSeq[i].distance)
            seek_ops += dis
            head_pos = RequestSeq[i].distance
            seek_seq.append(RequestSeq[i].distance)
            processID.append(RequestSeq[i].processNo)
            i = i + 1

    if (flag == -1):
        PlotGraph(seek_seq, processID, temp_head_pos, "SCAN", seek_ops)

    else:
        SaveGraph(seek_seq, processID, temp_head_pos, "SCAN", seek_ops)


def SSTF_diskScheduling(x):
    flag = x
    reqSeq = []
    s = sys.argv[1]
    ans = ""

    for i in s:
        if(i == " "):
            num = int(ans)
            reqSeq.append(num)
            ans = ""
        else:
            ans += i
    num = int(ans)
    reqSeq.append(num)

    head_pos = int(sys.argv[2])

    RequestSeq = []
    RequestSeq = ReqSeq_To_ObjSeq(reqSeq)
    temp_head_pos, min_dis, seek_ops = head_pos, float('inf'), 0
    SeekSeq = []
    seek_seq_analysis = []

    for i in RequestSeq:
        minRequest = SSTFobject()
        for j in RequestSeq:
            if j.visited == True:
                continue
            dis_from_head = max(j.distance - head_pos, head_pos - j.distance)
            if dis_from_head < min_dis:
                minRequest = j
                min_dis = dis_from_head

        SeekSeq.append(minRequest)
        minRequest.visited = True
        seek_ops += min_dis
        head_pos = minRequest.distance
        min_dis = float('inf')

        Final_Seq = []
        processID = []
        for i in SeekSeq:
            Final_Seq.append(i.distance)
            processID.append(i.processNo)

    if (flag == -1):
        PlotGraph(Final_Seq, processID, temp_head_pos, "SSTF", seek_ops)

    else:
        SaveGraph(Final_Seq, processID, temp_head_pos, "SSTF", seek_ops)


def FCFS_diskScheduling(x):
    flag = x
    reqSeq = []
    s = sys.argv[1]
    ans = ""

    for i in s:
        if(i == " "):
            num = int(ans)
            reqSeq.append(num)
            ans = ""
        else:
            ans += i
    num = int(ans)
    reqSeq.append(num)

    head_pos = int(sys.argv[2])
    RequestSeq = []

    for i in reqSeq:
        RequestSeq.append(i)

    seek_ops = 0
    temp_head_pos = head_pos
    seek_seq = []
    n = len(reqSeq)

    processID = [i for i in range(n)]

    for i in RequestSeq:
        dis = abs(head_pos - i)
        seek_ops += dis
        head_pos = i

    s = ""
    if flag == -1:
        PlotGraph(RequestSeq, processID, temp_head_pos, "FCFS", seek_ops)

    else:
        SaveGraph(RequestSeq, processID, temp_head_pos, "FCFS", seek_ops)


def CSCAN_diskScheduling(x):
    flag = x
    direction = "right"
    reqSeq = []
    s = sys.argv[1]
    ans = ""

    for i in s:
        if(i == " "):
            num = int(ans)
            reqSeq.append(num)
            ans = ""
        else:
            ans += i
    num = int(ans)
    reqSeq.append(num)
    head_pos = int(sys.argv[2])

    Seq = []
    for i in reqSeq:
        Seq.append(i)

    Seq.append(head_pos)

    RequestSeq = []
    RequestSeq = ReqSeq_To_ObjSeq(Seq)  # ReqSeq is list of objects

    disk_size, seek_ops, temp_head_pos = 500, 0, head_pos
    seek_seq = []
    seek_seq_analysis = []
    processID = []

    RequestSeq.sort(key=DISK_comparator, reverse=False)
    Seq.sort()

    index = Seq.index(head_pos)

    if direction == "right":
        i = index + 1
        while i < len(RequestSeq):
            dis = abs(head_pos - RequestSeq[i].distance)
            seek_ops += dis
            head_pos = RequestSeq[i].distance
            seek_seq.append(RequestSeq[i].distance)
            processID.append(RequestSeq[i].processNo)
            i = i + 1

        i, fl1 = 0, 0

        while i < index:
            if fl1 == 0:
                seek_ops += abs(head_pos - 499)
                head_pos = 499
                seek_seq.append(499)
                head_pos = 0
                seek_seq.append(0)
                fl1 = 1

            dis = abs(head_pos - RequestSeq[i].distance)
            seek_ops += dis
            head_pos = RequestSeq[i].distance
            seek_seq.append(RequestSeq[i].distance)
            processID.append(RequestSeq[i].processNo)
            i = i + 1

    else:
        i = index - 1
        while i >= 0:
            dis = abs(head_pos - RequestSeq[i].distance)
            seek_ops += dis
            head_pos = RequestSeq[i].distance
            seek_seq.append(RequestSeq[i].distance)
            processID.append(RequestSeq[i].processNo)
            i = i - 1

        i, fl = len(RequestSeq) - 1, 0

        while i > index:
            if fl == 0:
                seek_ops += abs(head_pos - 0)
                head_pos = 0
                seek_seq.append(0)
                head_pos = 499
                seek_seq.append(499)
                fl = 1

            dis = abs(head_pos - RequestSeq[i].distance)
            seek_ops += dis
            head_pos = RequestSeq[i].distance
            seek_seq.append(RequestSeq[i].distance)
            processID.append(RequestSeq[i].processNo)
            i = i - 1

    if flag == -1:
        PlotGraph(seek_seq, processID, temp_head_pos, "CSCAN", seek_ops)

    else:
        SaveGraph(seek_seq, processID, temp_head_pos, "CSCAN", seek_ops)


def LOOK_diskScheduling(x):
    flag = x
    direction = "right"

    reqSeq = []
    s = sys.argv[1]
    ans = ""

    for i in s:
        if(i == " "):
            num = int(ans)
            reqSeq.append(num)
            ans = ""
        else:
            ans += i
    num = int(ans)
    reqSeq.append(num)
    head_pos = int(sys.argv[2])

    Seq = []
    for i in reqSeq:
        Seq.append(i)

    Seq.append(head_pos)

    RequestSeq = []
    RequestSeq = ReqSeq_To_ObjSeq(Seq)  # ReqSeq is list of objects

    disk_size, seek_ops, temp_head_pos = 500, 0, head_pos
    seek_seq = []
    seek_seq_analysis = []
    processID = []

    RequestSeq.sort(key=DISK_comparator, reverse=False)
    Seq.sort()

    index = Seq.index(head_pos)

    if direction == "right":
        i = index + 1
        while i < len(RequestSeq):
            dis = abs(head_pos - RequestSeq[i].distance)
            seek_ops += dis
            head_pos = RequestSeq[i].distance
            seek_seq.append(RequestSeq[i].distance)
            processID.append(RequestSeq[i].processNo)
            i = i + 1

        i = index - 1
        while i >= 0:
            dis = abs(head_pos - RequestSeq[i].distance)
            seek_ops += dis
            head_pos = RequestSeq[i].distance
            seek_seq.append(RequestSeq[i].distance)
            processID.append(RequestSeq[i].processNo)
            i = i - 1

    else:
        i = index - 1
        while i >= 0:
            dis = abs(head_pos - RequestSeq[i].distance)
            seek_ops += dis
            head_pos = RequestSeq[i].distance
            seek_seq.append(RequestSeq[i].distance)
            processID.append(RequestSeq[i].processNo)
            i = i - 1

        i = index + 1
        while i < len(RequestSeq):
            dis = abs(head_pos - RequestSeq[i].distance)
            seek_ops += dis
            head_pos = RequestSeq[i].distance
            seek_seq.append(RequestSeq[i].distance)
            processID.append(RequestSeq[i].processNo)
            i = i + 1

    if flag == -1:
        PlotGraph(seek_seq, processID, temp_head_pos, "LOOK", seek_ops)

    else:
        SaveGraph(seek_seq, processID, temp_head_pos, "LOOK", seek_ops)


def CLOOK_diskScheduling(x):
    flag = x
    direction = "right"
    reqSeq = []
    s = sys.argv[1]
    ans = ""

    for i in s:
        if(i == " "):
            num = int(ans)
            reqSeq.append(num)
            ans = ""
        else:
            ans += i
    num = int(ans)
    reqSeq.append(num)
    head_pos = int(sys.argv[2])

    Seq = []
    for i in reqSeq:
        Seq.append(i)

    Seq.append(head_pos)

    RequestSeq = []
    RequestSeq = ReqSeq_To_ObjSeq(Seq)  # ReqSeq is list of objects

    disk_size, seek_ops, temp_head_pos = 500, 0, head_pos
    seek_seq = []
    seek_seq_analysis = []
    processID = []

    RequestSeq.sort(key=DISK_comparator, reverse=False)
    Seq.sort()

    index = Seq.index(head_pos)

    if direction == "right":
        i = index + 1
        while i < len(RequestSeq):
            dis = abs(head_pos - RequestSeq[i].distance)
            seek_ops += dis
            head_pos = RequestSeq[i].distance
            seek_seq.append(RequestSeq[i].distance)
            processID.append(RequestSeq[i].processNo)
            i = i + 1

        i = 0

        while i < index:
            dis = abs(head_pos - RequestSeq[i].distance)
            seek_ops += dis
            head_pos = RequestSeq[i].distance
            seek_seq.append(RequestSeq[i].distance)
            processID.append(RequestSeq[i].processNo)
            i = i + 1

    else:
        i = index - 1
        while i >= 0:
            dis = abs(head_pos - RequestSeq[i].distance)
            seek_ops += dis
            head_pos = RequestSeq[i].distance
            seek_seq.append(RequestSeq[i].distance)
            processID.append(RequestSeq[i].processNo)
            i = i - 1

        i = len(RequestSeq) - 1

        while i > index:
            dis = abs(head_pos - RequestSeq[i].distance)
            seek_ops += dis
            head_pos = RequestSeq[i].distance
            seek_seq.append(RequestSeq[i].distance)
            processID.append(RequestSeq[i].processNo)
            i = i - 1

    if flag == -1:
        PlotGraph(seek_seq, processID, temp_head_pos, "CLOOK", seek_ops)

    else:
        SaveGraph(seek_seq, processID, temp_head_pos, "CLOOK", seek_ops)


def DISK_ComparativeAnalysis():
    FCFS_diskScheduling(0)
    SSTF_diskScheduling(1)
    SCAN_diskScheduling(2)
    CSCAN_diskScheduling(3)
    LOOK_diskScheduling(4)
    CLOOK_diskScheduling(5)


check = sys.argv[3]

if (check == "scan"):
    SCAN_diskScheduling(-1)


if(check == "sstf"):
    Seq = sys.argv[1]
    head_pos = sys.argv[2]
    SSTF_diskScheduling(-1)


if(check == "fcfs"):
    FCFS_diskScheduling(-1)

if(check == "cscan"):
    CSCAN_diskScheduling(-1)

if(check == "look"):
    LOOK_diskScheduling(-1)

if(check == "clook"):
    CLOOK_diskScheduling(-1)


if(check == "disk_comp"):
    DISK_ComparativeAnalysis()


print("Harshit")