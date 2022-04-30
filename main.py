import matplotlib.pyplot as plt
import numpy as np


class memory_comparator:
    def __init__(self, name="\0", TU=-1, IF=-1, EF=-1):
        self.name = name
        self.TU = TU
        self.IF = IF
        self.EF = EF


class disk_comparator:
    def __init__(self, name="\0", seek_ops=-1, Seek_Seq=[]):
        self.name = name
        self.seek_ops = seek_ops
        self.Seek_Seq = Seek_Seq


class SSTFobject:
    def __init__(self, processNo=-1, distance=-1, visited=False):
        self.processNo = processNo
        self.distance = distance
        self.visited = False


class process_memory:
    def __init__(self, num=-1, size=-1, block=-1):
        self.num = num
        self.size = size
        self.block = block


class block:
    def __init__(self, num=-1, size=-1):
        self.num = num
        self.size = size


def FCFS_diskScheduling(reqSeq, head_pos, comparison=[], flag=-1):
    RequestSeq = []
    for i in reqSeq:
        RequestSeq.append(i)

    seek_ops, temp_head_pos = 0, head_pos
    seek_seq = []

    n = len(reqSeq)
    processID = [i for i in range(n)]

    for i in RequestSeq:
        dis = max(head_pos - i, i - head_pos)
        seek_ops += dis
        head_pos = i

    if flag == -1:
        print("Total number of Seek operation : ", seek_ops)
        print("Seek Sequence : ", end="")
        print(temp_head_pos, end="")
        for i in RequestSeq:
            print("->", i, " ", end="")

        return RequestSeq, processID, seek_ops

    else:
        seek_seq.append(temp_head_pos)
        for i in RequestSeq:
            seek_seq.append(i)

        d = disk_comparator("FCFS", seek_ops, seek_seq)
        comparison.append(d)


def ReqSeq_To_ObjSeq(RequestSeq):
    Object_seq = []
    count = 1

    for i in RequestSeq:
        obj = SSTFobject(count, i)  # i is the distance
        Object_seq.append(obj)
        count = count + 1

    return Object_seq


def SSTF_diskScheduling(Seq, head_pos, comparison=[], flag=-1):
    RequestSeq = ReqSeq_To_ObjSeq(Seq)
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

    if flag == -1:
        print("Total number of Seek operation : ", seek_ops)
        print("Seek Sequence : ", end="")
        print(temp_head_pos, end="")
        for i in SeekSeq:
            print("->", i.distance, " ", end="")

        return Final_Seq, processID, seek_ops

    else:
        seek_seq_analysis.append(temp_head_pos)
        for i in SeekSeq:
            seek_seq_analysis.append(i.distance)

        d = disk_comparator("SSTF", seek_ops, seek_seq_analysis)
        comparison.append(d)


def DISK_comparator(obj):
    return obj.distance


def SCAN_diskScheduling(reqSeq, head_pos, comparison=[], flag=-1, direction="right"):
    Seq = []
    for i in reqSeq:
        Seq.append(i)

    Seq.append(head_pos)
    RequestSeq = ReqSeq_To_ObjSeq(Seq)  # ReqSeq is list of objects

    disk_size, seek_ops, temp_head_pos = 500, 0, head_pos
    seek_seq = []
    seek_seq_analysis = []
    processID = []
    # RequestSeq.append(head_pos)
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

    if flag == -1:
        print("Total number of Seek operation : ", seek_ops)
        print("Seek Sequence : ", end="")
        # print(temp_head_pos, end="")
        for i in seek_seq:
            print("->", i, " ", end="")

        return seek_seq, processID, seek_ops

    else:
        seek_seq_analysis.append(temp_head_pos)
        for i in seek_seq:
            seek_seq_analysis.append(i)

        d = disk_comparator("SCAN", seek_ops, seek_seq_analysis)
        comparison.append(d)


def CSCAN_diskScheduling(reqSeq, head_pos, comparison=[], flag=-1, direction="right"):
    Seq = []
    for i in reqSeq:
        Seq.append(i)

    Seq.append(head_pos)
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
        print("Total number of Seek operation : ", seek_ops)
        print("Seek Sequence : ", end="")
        # print(temp_head_pos, end="")
        for i in seek_seq:
            print("->", i, " ", end="")

        return seek_seq, processID, seek_ops

    else:
        seek_seq_analysis.append(temp_head_pos)
        for i in seek_seq:
            seek_seq_analysis.append(i)

        d = disk_comparator("CSCAN", seek_ops, seek_seq_analysis)
        comparison.append(d)


def LOOK_diskScheduling(reqSeq, head_pos, comparison=[], flag=-1, direction="right"):
    Seq = []
    for i in reqSeq:
        Seq.append(i)

    Seq.append(head_pos)
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
        print("Total number of Seek operation : ", seek_ops)
        print("Seek Sequence : ", end="")
        # print(temp_head_pos, end="")
        for i in seek_seq:
            print("->", i, " ", end="")

        return seek_seq, processID, seek_ops

    else:
        seek_seq_analysis.append(temp_head_pos)
        for i in seek_seq:
            seek_seq_analysis.append(i)

        d = disk_comparator("LOOK", seek_ops, seek_seq_analysis)
        comparison.append(d)


def CLOOK_diskScheduling(reqSeq, head_pos, comparison=[], flag=-1, direction="right"):
    Seq = []
    for i in reqSeq:
        Seq.append(i)

    Seq.append(head_pos)
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
        print("Total number of Seek operation : ", seek_ops)
        print("Seek Sequence : ", end="")
        # print(temp_head_pos, end="")
        for i in seek_seq:
            print("->", i, " ", end="")

        return seek_seq, processID, seek_ops

    else:
        seek_seq_analysis.append(temp_head_pos)
        for i in seek_seq:
            seek_seq_analysis.append(i)

        d = disk_comparator("CLOOK", seek_ops, seek_seq_analysis)
        comparison.append(d)


def DiskComp(obj):
    return obj.seek_ops


def DISK_ComparativeAnalysis(Seq, head_pos):
    comparison = []
    FCFS_diskScheduling(Seq, head_pos, comparison, 0)
    SSTF_diskScheduling(Seq, head_pos, comparison, 1)
    SCAN_diskScheduling(Seq, head_pos, comparison, 2)
    CSCAN_diskScheduling(Seq, head_pos, comparison, 3)
    LOOK_diskScheduling(Seq, head_pos, comparison, 4)
    CLOOK_diskScheduling(Seq, head_pos, comparison, 5)

    comparison.sort(key=DiskComp, reverse=False)

    for i in comparison:
        print(i.name, "  ", i.seek_ops, "   ", i.Seek_Seq)


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


def DISK_TakeInput():
    list = []
    list = [int(item)
            for item in input("Enter the request sequence : ").split()]
    head_pos = int(input("Enter the head position : "))
    algo = input("Enter the desired algo : ")

    return list, head_pos, algo


def MEMORY_TakeInput():
    block_size = [int(item) for item in input(
        "Enter the size of each block : ").split()]
    mem_req = [int(item) for item in input(
        "Enter the memory requirement of each process : ").split()]

    count = 1
    processes = []
    blocks = []

    for i in mem_req:
        p = process_memory(count, i)
        processes.append(p)
        count = count + 1

    count1 = 1
    for i in block_size:
        b1 = block(count1, i)
        blocks.append(b1)
        count1 = count1 + 1

    return blocks, processes


def FF(blocks=[], processes=[], comparison=[], flag=-1):
    block_size_temp = []
    for i in blocks:
        b = block(i.num, i.size)
        block_size_temp.append(b)

    for i in processes:
        for j in block_size_temp:
            if i.size <= j.size:
                j.size -= i.size
                i.block = j.num
                break

    print("First Fit")
    print("ProcessID", "  ", "Memory Requirement", "  ", "Block Allocated")
    for i in processes:
        print("P", i.num, "              ", i.size, "              ", end="")
        if i.block == -1:
            print("No Block Allocated")
        else:
            print(i.block)

    if flag != 1:

        TU, IF, EF, total_memory = 0, 0, 0, 0

        for i, j in zip(blocks, block_size_temp):

            total_memory += i.size
            difference = i.size - j.size
            TU += difference

            if difference == 0:
                EF += i.size
            else:
                IF += j.size

        TU = ((TU) / total_memory) * 100
        IF = ((IF) / total_memory) * 100
        EF = ((EF) / total_memory) * 100
        m = memory_comparator("First Fit", TU, IF, EF)
        comparison.append(m)
        MEMORY_ANALYSIS_graph(comparison)


def compare_blocks(obj):
    return obj.size


def BF_WF(BLOCK=[], processes=[], comparison=[], flag=-1, algo="BF"):
    blocks = []
    for i in BLOCK:
        b = block(i.num, i.size)
        blocks.append(b)

    block_size_temp = []
    for i in BLOCK:
        b = block(i.num, i.size)
        block_size_temp.append(b)

    for i in processes:
        if algo == "BF":
            blocks.sort(key=compare_blocks, reverse=False)
            block_size_temp.sort(key=compare_blocks, reverse=False)

        else:
            blocks.sort(key=compare_blocks, reverse=True)
            block_size_temp.sort(key=compare_blocks, reverse=True)

        for j in block_size_temp:
            if i.size <= j.size:
                j.size -= i.size
                i.block = j.num
                break

    if flag == 1:
        print("Best Fit")
    else:
        print("Worst Fit")

    print("ProcessID", "  ", "Memory Requirement", "  ", "Block Allocated")
    for i in processes:
        print("P", i.num, "              ", i.size, "              ", end="")
        if i.block == -1:
            print("No Block Allocated")
        else:
            print(i.block)

    if flag != -1:
        TU, IF, EF, total_memory = 0, 0, 0, 0

        for i, j in zip(blocks, block_size_temp):
            total_memory += i.size
            difference = i.size - j.size
            TU += difference

            if difference == 0:
                EF += i.size
            else:
                IF += j.size

        TU = ((TU * 1.0) / total_memory) * 100
        IF = ((IF * 1.0) / total_memory) * 100
        EF = ((EF * 1.0) / total_memory) * 100

        if flag == 1:
            m = memory_comparator("Best Fit", TU, IF, EF)
            comparison.append(m)

        else:
            m = memory_comparator("Worst Fit", TU, IF, EF)
            comparison.append(m)


def NF(blocks=[], processes=[], comparison=[], flag=-1):
    block_size_temp = []
    for i in blocks:
        b = block(i.num, i.size)
        block_size_temp.append(b)

    last_allocated = -1

    for i in processes:
        num_of_iterations = 0
        j = last_allocated + 1
        while num_of_iterations < len(blocks):
            num_of_iterations += 1
            if i.size <= block_size_temp[j].size:
                block_size_temp[j].size -= i.size
                i.block = j + 1
                last_allocated = ((j + 1) % len(blocks)) - 1
                break

            j = (j + 1) % len(blocks)

    print("Next Fit")
    print("ProcessID", "  ", "Memory Requirement", "  ", "Block Allocated")
    for i in processes:
        print("P", i.num, "              ", i.size, "              ", end="")
        if i.block == -1:
            print("No Block Allocated")
        else:
            print(i.block)

    if flag != -1:
        TU, IF, EF, total_memory = 0, 0, 0, 0

        for i, j in zip(blocks, block_size_temp):
            total_memory += i.size
            difference = i.size - j.size
            TU += difference

            if difference == 0:
                EF += i.size
            else:
                IF += j.size

        TU = ((TU * 1.0) / total_memory) * 100
        IF = ((IF * 1.0) / total_memory) * 100
        EF = ((EF * 1.0) / total_memory) * 100
        m = memory_comparator("Next Fit", TU, IF, EF)
        comparison.append(m)


def MEMORY_ANALYSIS_graph(comparison=[]):
    length = len(comparison)

    tu_list = []
    ef_list = []
    if_list = []

    for i in comparison:
        tu_list.append(i.TU)
        ef_list.append(i.EF)
        if_list.append(i.IF)

    # set width of bar
    barWidth = 0.25
    # if(length == 1):
    #     barWidth = 0.1
    #fig = plt.subplots(figsize=(12, 8))

    # set height of bar
    # IT = [12, 30, 1, 8, 22]
    # ECE = [28, 6, 16, 5, 10]
    # CSE = [29, 3, 24, 25, 17]

    # Set position of bar on X axis
    br1 = np.arange(len(tu_list))
    br2 = [x + barWidth for x in br1]
    br3 = [x + barWidth for x in br2]

    # Make the plot
    plt.bar(br1, tu_list, color='r', width=barWidth,
            edgecolor='grey', label='TU')
    plt.bar(br2, ef_list, color='g', width=barWidth,
            edgecolor='grey', label='EF')
    plt.bar(br3, if_list, color='b', width=barWidth,
            edgecolor='grey', label='IF')

    # Adding Xticks
    plt.xlabel('Memory management Algorithms', fontweight='bold', fontsize=15)
    plt.ylabel('Percentage of Utilization', fontweight='bold', fontsize=15)
    if(length == 1):
        plt.xticks([r + barWidth for r in range(len(tu_list))],
                   [comparison[0].name])
    else:
        plt.xticks([r + barWidth for r in range(len(tu_list))],
                   ['First Fit', 'Best Fit', 'Worst Fit', 'Next Fit'])

    plt.legend()
    plt.show()


def MEMORY_ComparativeAnalysis():

    comparison = []
    blocks, processes = MEMORY_TakeInput()

    FF(blocks, processes, comparison, 0)
    BF_WF(blocks, processes, comparison, 1)
    BF_WF(blocks, processes, comparison, 2, "WF")
    NF(blocks, processes, comparison, 3)

    print("Algorithm", "      ", "TU(%)", "      ",
          "IF(%)", "      ", "EF", "      ")
    for i in comparison:
        print(i.name, "         ", i.TU, "        ", i.IF, "       ", i.EF)

    MEMORY_ANALYSIS_graph(comparison)


# blocks, processes = MEMORY_TakeInput()
# NF(blocks,processes)
MEMORY_ComparativeAnalysis()
# blocks, processes = MEMORY_TakeInput()
# FF(blocks, processes)
'''
ReqSeq , head_pos , algo = TakeInput()

DISK_ComparativeAnalysis(ReqSeq , head_pos)
#Object_seq = ReqSeq_To_ObjSeq(ReqSeq)
#Seq , processID ,seek_ops = CLOOK_diskScheduling(ReqSeq , head_pos)
#Seq, processID ,seek_ops = FCFS_diskScheduling(ReqSeq , head_pos )


#PlotGraph(Seq , processID , head_pos , algo , seek_ops)

#Seq , processID ,seek_ops = LOOK_diskScheduling(ReqSeq , head_pos)
#PlotGraph(Seq , processID , head_pos , algo , seek_ops)

'''
