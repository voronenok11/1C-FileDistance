import os
from multiprocessing import Pool


def is_similarity(file1, file2):
    reader1 = open(file1, "rb")
    reader2 = open(file2, "rb")
    content1 = reader1.read()
    content2 = reader2.read()

    length1 = len(content1)
    length2 = len(content2)

    if length1 == 0 or length2 == 0:
        if length1 == length2:
            return 100.0
        return 0.0
    
    if length1 < length2:
        length1, length2 = length2, length1
        content1, content2 = content2, content1

    lcs = [[0 for i in range(length2 + 1)] for j in range(2)]
    
    for i in range(1, length1 + 1):
        for j in range(1, length2 + 1):
            c1 = content1[i - 1]
            c2 = content2[j - 1]
            if c1 == c2:
                lcs[1][j] = max(lcs[1][j], lcs[0][j - 1] + 1)
            lcs[1][j] = max(lcs[1][j], lcs[0][j], lcs[1][j - 1])

        for j in range(length2 + 1):
            lcs[0][j] = lcs[1][j]
            lcs[1][j] = 0

    reader1.close()
    reader2.close()

    return lcs[0][length2] * 100.0 / max(length1, length2) 


def solve(first_path_directory, second_path_directory, similarity):
    first_directory_files = [first_path_directory + '/' + file for file in os.listdir(first_path_directory)]
    second_directory_files = [second_path_directory + '/' + file for file in os.listdir(second_path_directory)]


    answer_file = open("answer.txt", "w")


    with Pool(20) as pool:
        res = pool.starmap(is_similarity, [
            (file1, file2)
            for file1 in first_directory_files
            for file2 in second_directory_files
        ]) 

    for ind1, file1 in enumerate(first_directory_files):
        for ind2, file2 in enumerate(second_directory_files):
            cur_similarity = res[ind1 * len(second_directory_files) + ind2]
            if cur_similarity == 100.0:
                answer_file.write(f"Файлы {file1} и {file2} идентичны\n")
    
    for ind1, file1 in enumerate(first_directory_files):
        for ind2, file2 in enumerate(second_directory_files):
            cur_similarity = res[ind1 * len(second_directory_files) + ind2]
            if cur_similarity >= similarity:
                answer_file.write(f"Файлы {file1} и {file2} похожи с коэффициентом сходства {cur_similarity:.1f}%\n")

    for ind1, file1 in enumerate(first_directory_files):
        in_another_directory = False
        for ind2, file2 in enumerate(second_directory_files):
            cur_similarity = res[ind1 * len(second_directory_files) + ind2]
            if cur_similarity >= similarity:
                in_another_directory = True

        if not in_another_directory:
            answer_file.write(f"Файл {file1} есть в первой директории, но нет во второй\n")
        
    for ind2, file2 in enumerate(second_directory_files):
        in_another_directory = False
        for ind1, file1 in enumerate(first_directory_files):
            cur_similarity = res[ind1 * len(second_directory_files) + ind2]
            if cur_similarity >= similarity:
                in_another_directory = True

        if not in_another_directory:
            answer_file.write(f"Файл {file2} есть во второй директории, но нет в первой\n")


    answer_file.close()




first_path_directory = input('Введите путь до первой директории: ')
second_path_directory = input('Введите путь до второй директории: ')
similarity = float(input('Введите параметр сходство: '))

solve(first_path_directory, second_path_directory, similarity)





