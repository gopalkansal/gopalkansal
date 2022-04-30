import sys
import matplotlib.pyplot as plt
import numpy as np


class memory_comparator:
    def __init__(self, name="\0", TU=-1, IF=-1, EF=-1):
        self.name = name
        self.TU = TU
        self.IF = IF
        self.EF = EF


class process_memory:
    def __init__(self, num=-1, size=-1, block=-1):
        self.num = num
        self.size = size
        self.block = block


class block:
    def __init__(self, num=-1, size=-1):
        self.num = num
        self.size = size


def compare_blocks(obj):
    return obj.size


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
        plt.legend()
        plt.show()
    else:
        plt.xticks([r + barWidth for r in range(len(tu_list))],
                   ['First Fit', 'Best Fit', 'Worst Fit', 'Next Fit'])
        plt.legend()
        plt.savefig('public/memoryCompGraph.png')


def BlocksAllocated_graph(processes, algorithm):
    block = []
    processID = []
    notAllocatedBlock = []
    notAllocatedProcess = []
    for i in processes:
        if(i.block == -1):
            notAllocatedBlock.append((i.block))
            notAllocatedProcess.append((i.num))
        block.append((i.block))
        processID.append(i.num)

    plt.xlabel('Process ID', fontweight='bold', fontsize=15)
    plt.ylabel('Block Number', fontweight='bold', fontsize=15)

    plt.title(algorithm, loc='right')
    # plt.scatter(processID, block)
    plt.plot(processID, block, color='green', linestyle='none', linewidth=0,
             marker='o', markerfacecolor='blue', markersize=8)

    plt.plot(notAllocatedProcess, notAllocatedBlock, color='green', linestyle='none', linewidth=0,
             marker='o', markerfacecolor='red', markersize=8)
    plt.show()
    plt.clf()


def BlocksAllocated_Savegraph(processes, algorithm):
    block = []
    processID = []
    notAllocatedBlock = []
    notAllocatedProcess = []
    for i in processes:
        if(i.block == -1):
            notAllocatedBlock.append((i.block))
            notAllocatedProcess.append((i.num))
        block.append((i.block))
        processID.append(i.num)

    plt.xlabel('Process ID', fontweight='bold', fontsize=15)
    plt.ylabel('Block Number', fontweight='bold', fontsize=15)

    plt.title(algorithm, loc='right')
    # plt.scatter(processID, block)
    plt.plot(processID, block, color='green', linestyle='none', linewidth=0,
             marker='o', markerfacecolor='blue', markersize=8)

    plt.plot(notAllocatedProcess, notAllocatedBlock, color='green', linestyle='none', linewidth=0,
             marker='o', markerfacecolor='red', markersize=8)
    plt.savefig('public/'+algorithm+'graph.png')

    plt.clf()


def MEMORY_TakeInput(block_size, mem_req):
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


def FF(flag=-1, compareAll4=[]):
    # blocks
    blocks_ff = []

    s = sys.argv[1]
    ans = ""

    for i in s:
        if(i == " "):
            num = int(ans)
            blocks_ff.append(num)
            ans = ""
        else:
            ans += i
    num = int(ans)
    blocks_ff.append(num)

    # processes
    processes_ff = []
    t = sys.argv[2]
    ans1 = ""

    for i in t:
        if(i == " "):
            num = int(ans1)
            processes_ff.append(num)
            ans1 = ""
        else:
            ans1 += i
    num = int(ans1)
    processes_ff.append(num)

    blocks, processes = MEMORY_TakeInput(blocks_ff, processes_ff)

    comparison = []
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

    if (flag == -1):
        MEMORY_ANALYSIS_graph(comparison)
        BlocksAllocated_graph(processes, "First Fit")
    else:
        compareAll4.append(m)
        BlocksAllocated_Savegraph(processes, "First Fit")


def BF_WF(algo="Best Fit", flag=-1, compareAll4=[]):
    # blocks
    blocks_ff = []

    s = sys.argv[1]
    ans = ""

    for i in s:
        if(i == " "):
            num = int(ans)
            blocks_ff.append(num)
            ans = ""
        else:
            ans += i
    num = int(ans)
    blocks_ff.append(num)

    # processes
    processes_ff = []
    t = sys.argv[2]
    ans1 = ""

    for i in t:
        if(i == " "):
            num = int(ans1)
            processes_ff.append(num)
            ans1 = ""
        else:
            ans1 += i
    num = int(ans1)
    processes_ff.append(num)

    BLOCK, processes = MEMORY_TakeInput(blocks_ff, processes_ff)

    comparison = []

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

    m = memory_comparator(algo, TU, IF, EF)
    comparison.append(m)

    if(flag == -1):
        MEMORY_ANALYSIS_graph(comparison)
        BlocksAllocated_graph(processes, algo)
    else:
        compareAll4.append(m)
        BlocksAllocated_Savegraph(processes, algo)


def NF(flag=-1, compareAll4=[]):
    # blocks
    blocks_ff = []

    s = sys.argv[1]
    ans = ""

    for i in s:
        if(i == " "):
            num = int(ans)
            blocks_ff.append(num)
            ans = ""
        else:
            ans += i
    num = int(ans)
    blocks_ff.append(num)

    # processes
    processes_ff = []
    t = sys.argv[2]
    ans1 = ""

    for i in t:
        if(i == " "):
            num = int(ans1)
            processes_ff.append(num)
            ans1 = ""
        else:
            ans1 += i
    num = int(ans1)
    processes_ff.append(num)

    blocks, processes = MEMORY_TakeInput(blocks_ff, processes_ff)

    comparison = []
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

    if (flag == -1):
        MEMORY_ANALYSIS_graph(comparison)
        BlocksAllocated_graph(processes, "Next Fit")
    else:
        compareAll4.append(m)
        BlocksAllocated_Savegraph(processes, "Next Fit")


def MEMORY_ComparativeAnalysis():
    compareAll4 = []
    print("Above FF call")
    FF(0, compareAll4)
    print("Above BF call")
    BF_WF("Best Fit", 1, compareAll4)
    print("Above WF call")
    BF_WF("Worst Fit", 2, compareAll4)
    print("Above NF call")
    NF(3, compareAll4)
    print("Done with all calls")
    MEMORY_ANALYSIS_graph(compareAll4)


check = sys.argv[3]
if(check == "first_fit"):
    FF()

if(check == "best_fit"):
    BF_WF()

if(check == "worst_fit"):
    BF_WF("Worst Fit")

if(check == "next_fit"):
    NF()

if(check == "memory_comp"):
    print("Inside check")
    MEMORY_ComparativeAnalysis()
