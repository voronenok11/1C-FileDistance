import os


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

    lcs = [[0 for i in range(length2 + 1)] for j in range(length1 + 1)]
    
    for i in range(1, length1 + 1):
        for j in range(1, length2 + 1):
            c1 = content1[i - 1]
            c2 = content2[j - 1]
            if c1 == c2:
                lcs[i][j] = max(lcs[i][j], lcs[i - 1][j - 1] + 1)
            lcs[i][j] = max(lcs[i][j], lcs[i - 1][j], lcs[i][j - 1])

    return lcs[length1][length2] * 100.0 / max(length1, length2) 
            
    
    






first_path_directory = input('Введите путь до первой директории: ')
second_path_directory = input('Введите путь до второй директории: ')
similarity = float(input('Введите параметр сходство: '))

first_directory_files = os.listdir(first_path_directory)
second_directory_files = os.listdir(second_path_directory)

for file1 in first_directory_files:
    for file2 in second_directory_files:
        path1 = first_path_directory + '/' + file1
        path2 = second_path_directory + '/' + file2
        cur_similarity = is_similarity(path1, path2)
        if cur_similarity >= similarity:
            print(f"Файлы {path1} и {path2} похожи с коэффициентом сходства {cur_similarity:.1f}%")




