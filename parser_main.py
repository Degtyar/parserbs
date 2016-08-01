import sys
import argparse
import name

# Список файлов для работы
try:
    f = open('cdr_1.csv', 'r', encoding='UTF8')             # - файл выгрузки Барсум
    fw = open('otchet_vigruzki.html', 'w', encoding='UTF8')  # - файл выгрузки итогов
    viborka = open('viborka2.txt', 'w', encoding='UTF8')     # - файл со строками совпадений
except Exception as e:
    print("OS error: {0}".format(e))
    sys.exit()

# Обработчик входных параметров
def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-yy', '--year', type=int, default=0)
    parser.add_argument('-mm', '--month', type=int, default=0)
    parser.add_argument('-max', '--max', type=int, default=0)   # вывечти топ из max строк
    parser.add_argument('-ts', '--t_sum', type=int, default=0)  # продолжительность вызовов
    parser.add_argument('-tc', '--t_col', type=int, default=0)  # количество вызовов
    parser.add_argument('-s', '--t_sort', type=int, default=0)  # сортировка 1 - времени 0 - количество
    parser.add_argument('-w', '--t_work', type=int, default=0)  # сортировка 1 - времени 0 - количество
    return parser

# Заполнение параметров
if __name__ == '__main__':
    parser = createParser()
    namespace = parser.parse_args(sys.argv[1:])
    yy = namespace.year
    mm = namespace.month
    #max = namespace.max
    max = 10
    t_sum = namespace.t_sum
    t_col = namespace.t_col
    t_sum = 300
    t_sort = namespace.t_sort
    t_sort = 0

# Инициализация служебных переменных
month = ['январь', 'февраль', 'март', 'апрель', 'май', 'июнь', 'июль', 'август', 'сентябрь', 'октябрь', 'ноябрь',
         'декабрь']
work_hour = [7,8,9,10,11,12,13,14,15,16,17,18,19]
not_work_hour = [20,21,22,23,0,1,2,3,4,5,6]
# исключить из выборки номера короче L
L = 5
# временной интервал
tt_n = 8
tt_e = 20
if t_sort:
    l = lambda x: x[1][1]
else:
    l = lambda x: x[1]

print('----Начало выполенения задания----')
print(' yy = %d mm = %d max = %d t_sum = %d t_col = %d' % (yy, mm, max, t_sum, t_col))


def namber_search(f,work_hour):
    count_sovp = 0
    count_coll = 0
    namber = {}
    namber_total = {}
    err = 0
    err_t = ''
    for s in f:
        f_str = s.split(';')
        try:
            day_f = f_str[0].split('.')
            w_time = f_str[1].split(':')
            if int(day_f[1]) >= mm and int(day_f[2]) >= yy and (int(w_time[0]) in work_hour):
                in_namber = f_str[3]
                out_namber = f_str[4]
                len_out = len(out_namber)
                name_t = f_str[2]
                to_time = f_str[6].split(':')
                if len(to_time) > 0 and len(to_time) > 2:
                    t_min = int(to_time[0]) * 60 + int(to_time[1])
                elif len(to_time) > 0:
                    t_min = int(to_time[0])
                if t_min < 200:
                    count_sovp += 1
                    viborka.write(s)
                    if in_namber in namber and len_out > L:
                        if out_namber in namber[in_namber] and t_min != 0:
                            namber[in_namber][out_namber][0] += 1
                            namber[in_namber][out_namber][1] += t_min
                            namber_total[in_namber][1] += t_min
                            namber_total[in_namber][0] += 1
                        elif t_min != 0 and len_out > L:
                            namber[in_namber][out_namber] = [1, t_min]
                            namber_total[in_namber][1] += t_min
                            namber_total[in_namber][0] += 1
                    elif t_min != 0 and len_out > L:
                        namber[in_namber] = {out_namber: [1, t_min]}
                        namber_total[in_namber] = [1, t_min, name_t]
        except Exception:
            err += 1
            err_t += "Ошибка обработки строки  №%d : %s \n" % (count_coll, s)
        count_coll += 1
    return {'namber':namber, 'namber_total':namber_total, 'count_coll':count_coll, 'count_sovp':count_sovp, 'err':err, 'err_t':err_t}

result_namber = namber_search(f,not_work_hour)
namber = result_namber['namber']
namber_total = result_namber['namber_total']
count_coll = result_namber['count_coll']
err = result_namber['err']
err_t = result_namber['err_t']
count_sovp = result_namber['count_sovp']


html_wr = 0


print('----Обработано %d строк / в выборку попало %d ошибок при обработке %d ----' % (count_coll, count_sovp, err))
sorted_total_count = (sorted(namber_total.items(), key=l, reverse=True))

for tel in sorted_total_count:
    rez = namber[tel[0]]
    if int(tel[0]) in name.name_mas:
        name_tel = '/--%s--/' % name.name_mas[int(tel[0])]
    else:
        name_tel = '/--отсутствует в справочнике портала--/'
    if int(tel[0]) in name.name_mas_av:
        name_tel_av = '/**%s**/' % name.name_mas_av[int(tel[0])]
    else:
        name_tel_av = '/**отсутствует описание**/'
    total = namber_total[tel[0]]
    middle_t = round(total[1] / total[0], 1)
    z = (sorted(rez.items(), key=l, reverse=True))
    wr = '\n \n \t %s внутренний номер = %s %s %s \n \t всего вызовов = %d  на мин = %d средняя продолжительность вызова = %s мин \n ' % (
    tel[0], total[2], name_tel, name_tel_av, total[0], total[1], middle_t)
    if mm: wr += '\t за месяц %s \n' % month[mm - 1]
    if t_col: wr += '\t фильтр - номера телефонов на которые взонили %d раз и более \n' % t_col
    if t_sum: wr += '\t фильтр - номера телефонов с котормыми говорили %d мин и более\n' % t_sum
    if max: wr += '\t фильтр - ТОП %d вызовов \n' % max
    count_loop = 1
    for y in z:
        if max and count_loop > max: break
        if y[1][0] > t_col and y[1][1] > t_sum:
            fw.write(wr)
            wr = ''
            wr = 'звонки с номера = %s \t' % tel[0]
            wr += 'на номер = %s \t' % y[0]
            wr += 'вызовов = %d \t \t мин = %d\n' % (y[1][0], y[1][1])
            fw.write(wr)
            wr = ''
            count_loop += 1

viborka.write(err_t)

f.close()
fw.close()
viborka.close()
