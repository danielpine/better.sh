import sys
sys.path.append("..")
sys.path.append(".")

if __name__ == '__main__':
    from tools.common import extract
    from tools.PySqlTemplate import PySqlTemplate
    from tools import setupDataSource

    setupDataSource()
    state = '芳华 @区县: 浦东 @地址: 白杨'
    current = 1
    pageSize = 10
    dd = '0328'
    fields = extract(state)
    vals = []
    statements = []
    if '小区' in fields:
        s = ['%'+'%'.join(st)+'%' for st in fields['小区']]
        t = [' name like ? ' for st in fields['小区']]
        vals += s
        statements += t

    if '地址' in fields:
        s = ['%'+'%'.join(st)+'%' for st in fields['地址']]
        t = [' lane like ? ' for st in fields['地址']]
        vals += s
        statements += t
    vals = tuple(v for v in vals)
    sql = 'or'.join(statements)
    if sql:
        sql = ' WHERE '+sql

    countSql = '''SELECT count(name) FROM  estate %s''' % sql

    total = PySqlTemplate.count(countSql, *vals)
    # print(total)
    page = PySqlTemplate.findList(
        ''' SELECT e.*, r.mark_date, r.`name` AS pubname FROM 
        ( SELECT * FROM estate %s ORDER BY NAME LIMIT ?,? ) e 
        LEFT JOIN record r ON LOCATE(r.`name`, e.lane) > 0 and r.district=e.district where r.mark_date>=? ORDER BY e.NAME''' % sql,
        *vals,
        (int(current)-1)*int(pageSize), int(pageSize), dd
    )
    # print(page)
