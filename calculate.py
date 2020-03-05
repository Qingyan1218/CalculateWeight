import re

def replacek(initexpr):
    """to replace chinese parenthesis with english parenthesis"""
    a=initexpr.replace('（', '(')
    b=a.replace('）', ')')
    return b

def readexpr(initexpr):
    """to find the math expression between two equal sign, flag is the symbol of the start of the unit"""
    indexlist = [i.start() for i in re.finditer('=', initexpr)]  #find the equal sign place
    if len(indexlist)>1:
        ename=initexpr[0:indexlist[0]]
        expr=initexpr[(indexlist[0]+1):indexlist[1]]
        rest=initexpr[indexlist[1]+1: ]
        unit=''
        flag=0
        for i in rest:
            if flag==0:
                if i.isalpha():
                    unit+=i
                    flag=1
            else:
                if i.isalpha() or i=='/' or i=='.':
                    unit +=i
        if unit=='':
            unit="kN"
    elif len(indexlist)==1:
        ename=initexpr[0:indexlist[0]]
        rest=initexpr[(indexlist[0]+1):]
        unit=''
        expr=''
        flag=0
        for i in rest:
            if flag==0:
                if i.isalpha() and i !='x':
                    unit+=i
                    flag=1
                else:
                    expr+=i
            else:
                if i.isalpha() or i=='/' or i=='.':
                    unit +=i
        if unit=='':
            unit='kN'
        else:
            ename=initexpr
            expr=None
    else:
        ename=None
        expr=None
        unit=None
    return (ename,expr,unit)

def calculate(ename,expr,unit='kN',valuedict=None):
    """to calculate the math expression, ename and unit are used to create the final expression"""
    if valuedict:
        for item in valuedict:
            exec(item + '=' + valuedict[item])
    newexpr = expr.replace('x', '*')
    value = eval(newexpr)
    result = '%s=%s=%.2f%s' % (ename, expr, value, unit)
    return result

def splitexpr(initexpr,valuedict=None):
    """this function uses the other function in this module to get the result of the expression"""
    newexpr1=initexpr.replace('，',',')
    newexpr=newexpr1.replace(' ','')
    exprlist=(newexpr.strip()).split(',')
    resultstr=''
    for sexpr in exprlist:
        newsexpr=replacek(sexpr.strip())
        ename,expr,unit=readexpr(newsexpr)
        if expr:
            result=calculate(ename,expr,unit,valuedict)
        else:
            result=newsexpr
        resultstr +=(result+'，')
    if resultstr[-2]=="，" :
        resultstr=resultstr[0:-1]
    return resultstr

def getparam(sententce):
    """to get the name and value"""
    single = sententce.split('，')
    result=[]
    for item in single:
        if item=='':
            pass
        else:
            part = item.split('=')
            if len(part)==1:
                pass
            else:
                reversepart=part[0][::-1]
                for i, alpha in enumerate(reversepart):
                    if alpha.encode('utf-8').isalpha() or alpha.isdigit():   #chinese is alpha.
                        i+=1
                    else:
                        break
                    i=-i
                    name = part[0][i:]
                for i, number in enumerate(part[-1]):
                    if number.isalpha():
                        value = part[-1][0:i]
                        break
                expression=(name,value)
                result.append(expression)
    return result

if __name__=='__main__':
    # initexpr='侧壁及纵隔墙重G1=(19.5x14.4-17.9x6x2)x8.8x25=37280kN'
    # aname,expr,unit=readexpr(initexpr)
    # print(aname,expr,unit)
    # print(calculate(aname,expr,unit))
    # a = 'L2尺寸为400*300（h），跨度为L=1.6x3.1416x100/360=1.4m，但是还有kN和kN/m'
    # ename, expr,unit = readexpr(a)
    # print(ename, expr,unit)
    # print(calculate(ename,expr,unit))
    # a="因此活载为Q=70+30=100kN/m，恒载为P=8.3+8.5=16.8kN/m"
    # print(splitexpr(a))
    # b="L2尺寸为400*300（h），跨度为L=1.6x3.1416x100/360=1.4m"
    # print(splitexpr(b))
    # c="牛腿G5=（1.5+3.0）/2x4.25x0.8x25"
    # print(splitexpr(c))
    result = getparam('检修活载G13=5x(19.5-3.2-2.665)x14.4=981.72kN，')
    print(result)
    result = getparam('板重按0.6m宽作用于L2及0.4m高的梁重P2=0.6x0.3x25+0.4x0.4x25=25kN/m')
    print(result)
    result=getparam('L2=200mm，跨度为L=1.6x3.1416x100/360=50m')
    print(result)
    for item in result:
        print(item)
        exec(item[0]+'='+item[1])
    newresult=eval('L2-L/(L2+L)')
    print(newresult)




    
