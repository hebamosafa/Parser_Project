# cv2.line(tree, (px1+30, py2), (int(x1+30), int(y1)), (0,255,0),2)
# cv2.line(tree, (px1+30, py2), (x1+30, y1), (0,255,0),3)
import cv2
import random
from pythonds.basic import Stack
from pythonds.trees import BinaryTree
def buildParseTree(fpexp):
    fplist = fpexp.split()
    pStack = Stack()
    eTree = BinaryTree('')
    pStack.push(eTree)
    currentTree = eTree

    for i in fplist:
        if i == '(':
            currentTree.insertLeft('')
            pStack.push(currentTree)
            currentTree = currentTree.getLeftChild()

        elif i in ['+', '-', '*', '/']:
            currentTree.setRootVal(i)
            currentTree.insertRight('')
            pStack.push(currentTree)
            currentTree = currentTree.getRightChild()

        elif i == ')':
            currentTree = pStack.pop()

        elif i not in ['+', '-', '*', '/', ')']:
            try:
                currentTree.setRootVal(i)
                parent = pStack.pop()
                currentTree = parent

            except ValueError:
                raise ValueError("token '{}' is not a valid integer".format(i))

    return eTree

tree = cv2.imread('images/tree.png')
scale_percent = 220 # percent of original size
width = int(tree.shape[1] * scale_percent / 100)
height = int(tree.shape[0] * scale_percent / 100)
dim = (width, height)

    # resize image
tree = cv2.resize(tree, dim, interpolation = cv2.INTER_AREA)
length=0
########################################################################################
class node:
    text = ''
    xcc = 0
    ycc = 0
    x22 = 0
    y22 = 0
    textx = 0
    texty = 0
    font = cv2.FONT_HERSHEY_SIMPLEX
    type = 0

    def __init__(self, type, xc, yc, x2, y2, tex):
        self.xcc = xc
        self.ycc = yc
        self.x22 = x2
        self.y22 = y2
        self.text = tex
        self.textx = int(self.xcc) + 5
        self.texty = ((int(self.y22) - int(self.ycc)) / 2) + self.ycc
        self.type = type
        self.set_para()

    def set_para(self):
        if (self.type == 0):
            start = (int(self.xcc), int(self.ycc))
            end = (int(self.x22), int(self.y22))
            cv2.rectangle(tree, start, end, (255, 0, 0), 2)

        else:
            cv2.circle(img=tree, center=(int(self.xcc)+20, int(self.ycc)+20), radius=25, color=(255, 0, 0), thickness=2)

        cv2.putText(tree, text=self.text, org=(int(self.textx), int(self.texty)), fontFace=self.font, fontScale=0.5,
                    color=(255, 0, 255), thickness=1, lineType=cv2.LINE_AA)

    def left_child(self, type, text):

        x2 = (((self.x22 - self.xcc) / 2) - 5) + self.xcc-50
        x1 = self.xcc - 80
        y1 = self.y22 + 30
        y2 = y1 + 40
        left = node(type, x1, y1, x2, y2, text)
        self.drawline(self.xcc,self.y22,x1+30,y1)
        return left
    def samelevel(self,type,text):
        print('k')
        x1 = self.x22+190
        x2 = x1 +60
        y1 = self.ycc
        y2 = self.y22
        same = node(type, x1, y1, x2, y2, text)
        self.drawline(self.xcc+60, self.y22-20, x1, y1+20)
        return  same
    def onlyone(self,type,text):

        y1 = self.y22+90
        y2 = y1+40
        same = node(type, self.xcc, y1, self.x22, y2, text)
        self.drawline(self.xcc+30, self.y22, self.xcc+30, y1-5)
        return same
    def drawline(self,x1,y1,x2,y2):
        cv2.line(tree, (int(x1), int(y1)), (int(x2),int(y2)), (0,255,0),2)



    def right_child(self, type, text):
        x1 = (((self.x22 - self.xcc) / 2) + 5) + self.xcc+50
        x2 = x1 + 60
        y1 = self.y22 + 30
        y2 = y1 + 40

        right = node(type, x1, y1, x2, y2, text)
        self.drawline(self.x22-10, self.y22-10, x1, y1)
        return right

    def addextra(self, text):
        cv2.putText(tree, text='('+text+')', org=(int(self.textx), int(self.texty) + 13), fontFace=self.font,
                    fontScale=0.4,
                    color=(255, 0, 255), thickness=1, lineType=cv2.LINE_AA)

                            #################################
def term(text):
 termenals=['op','const','id']
 s=termenals.count(text)
 if(s>0):
     return 1
 return 0
def del_brackets(i,limit,tokens):
    while (tokens[i] != limit):
        if (tokens[i] == ')' or tokens[i] == '('):
            del tokens[i]
        else:
            i+=1
    return tokens
#############################################
def if_stat(i,parent,tokens):

    tokens=del_brackets(i,'then',tokens)
    print(tokens)
    global length
    length=len(tokens)
    if(parent.text!='if'):
        IF = parent.left_child(0, 'if')
    else:IF=parent
    OP = IF.left_child(1, 'op')
    i = op_op(i, OP,tokens)
    i, IFR = check(i, IF, 1,tokens)
    LEVEL1 = IFR
    while (tokens[i] != 'end' and tokens[i] != 'else'  ):
        # create node that in the same leve
        i, LEVEL2 = check(i, LEVEL1, 0,tokens)
        LEVEL1 = LEVEL2
    if(tokens[i] == 'else'):
        if(tokens[i+1]=='else'):
            else_part=IF.onlyone(1,'else')
            i, IFS=check(i+2,else_part,1,tokens)
            print('heba')
            LEVELELSE1=IFS
            while (tokens[i] != 'end'):
                # create node that in the same leve
                i, LEVELELSE2 = check(i, LEVELELSE1, 0, tokens)
                LEVELELSE1 = LEVELELSE2
    return i,IF
####################
def constant(root1,x):
    m = 1
    while m in range(len(x) - 1):
        if (is_number(x[m+1])):
            u = root1.left_child(1, 'const')
        elif(str(x[m + 1]).isalpha()):
            u = root1.left_child(1, 'id')
        else:
            u = root1.left_child(1, 'op')
        u.addextra(x[m + 1])
        if (is_number(x[m])):
            p = root1.right_child(1, 'const')

        elif (str(x[m]).isalpha()):
            p = root1.right_child(1, 'id')

        else:
            p = root1.right_child(1, 'OP')
        p.addextra(x[m])


        root1=u
        m += 2


###########################
def expt(i,OP,tokens):
    var='('
    while(i!=len(tokens) and tokens[i]!=';'and tokens[i]!='end'and tokens[i]!='else' and not(comparson(tokens[i])) and  tokens[i]!='then'and tokens[i]!='until'):
        var+=tokens[i]+' '
        i+=1
    var=var[1:]
    print(var)
    pt = buildParseTree(var)
    x = pt.postorder()
    x.reverse()
    if('' in x):
        x.remove('')
    print(len(x))
    print(x)
    if(len(x)==1):
        root1 = OP.onlyone(1, 'const')
        root1.addextra(x[0])
    else:
        root1 = OP.onlyone(1, 'op')
        root1.addextra(x[0])
        constant(root1,x)
    x.clear()
    return i
##################################
def assignt(i,ASSIGN,tokens):
    i=expt(i+1,ASSIGN,tokens)
    return i
##########################################
def repeatt(i,IFR,tokens):
    OP_REP = IFR.right_child(1, 'op')
    i, W = check(i + 1, IFR, 1,tokens)
    while(tokens[i]!='until'):
        i, W = check(i , W, 0,tokens)

    i = op_op(i, OP_REP,tokens)
    return  i
######################################################
def check(i,IF,Y,tokens):

    while (tokens[i] != ':=' and tokens[i] != 'read' and tokens[i] != 'write' and tokens[i] != 'repeat'and tokens[i] != 'if'):
        i += 1
    if(tokens[i] == ':=') :
        tokens[i] = 'assign'
    if (Y):
        if(IF.text=='if'):

            IFR = IF.right_child(0, tokens[i])
        else:
            IFR = IF.left_child(0, tokens[i])
    else:
        IFR = IF.samelevel(0, tokens[i])


    if (tokens[i] == 'assign'):
        IFR.addextra(tokens[i - 1])
        i = assignt(i, IFR,tokens)
    elif (tokens[i] == 'read'):
        IFR.addextra(tokens[i + 1])
        #to skip x;

        i += 3
    elif (tokens[i] == 'write'):
        e = IFR.onlyone(1, 'id')
        e.addextra(tokens[i + 2])

        #to skip x;
        i += 4
    elif (tokens[i] == 'repeat'):
       i= repeatt(i,IFR,tokens)
    elif (tokens[i] == 'if'):
        i,_ = if_stat(i,IFR ,tokens)
    return i,IFR


##################################################################
def comparson (text):
    if(text=='=' or text=='<' or  text=='>'):
        return 1
    return 0
################################################################################
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
def op_op(i,OP,tokens):

    if (comparson(tokens[i+2])):
        OP.addextra(tokens[i+2])
        if(is_number(tokens[i + 1])):
            OPL = OP.left_child(1, 'const')
            OPL.addextra(tokens[i + 1])
        elif(str(tokens[i]).isalpha()):
            OPL = OP.left_child(1, 'id')
            OPL.addextra(tokens[i + 1])
        else:
            pass
            #OPL = OP.left_child(1, tokens[i+1])

        i += 1
    else:
        i = expt(i + 1, OP,tokens)

     #pos of expected then left <= rirght then
    i+=3
    if (i !=len(tokens) and tokens[i] != 'then' and tokens[i] != ';' ):
        i = expt(i-1,OP,tokens)
        #true = i + 1
    else:
        if (is_number(tokens[i - 1])):
            OPR = OP.right_child(1, 'const')
            OPR.addextra(tokens[i - 1])
        elif(str(tokens[i-1]).isalpha()):
            OPR = OP.right_child(1, 'id')
            OPR.addextra(tokens[i-1])
        else:
            pass
            #OPR=OP.right_child(1,tokens[i - 1])
        i+=1
    # return pos of last exp
    return i
##############################################################################
def syntax_tree(tokens):

    #tokens = ['read','x',';','if', '0', '<', 'x','then','fact', ':=','x','*','1', ';','repeat','fact',':=','(','x','-','5',')','*','6',';','x',':=','x','-','1',
     #'until','x','=','0',';','write','fact','end','else','fact', ':=','x','*','1',';','x',':=','0','end']
    #tokens=['fact',':=','(','x','-','5',')','*','6',';','x',':=','x','-','1']
    #tokens=['read', 'x', ';', 'if', '(', '0', '<', 'x', ')', 'then', 'fact', ':=','(', '1',')', 'end']
    #tokens=['read', 'x', ';', 'if', '(', '0', '<', 'x', ')', 'then', 'fact', ':=', '(', '1', ')', ';', 'write', '(', 'fact', ')', 'end']
    #tokens=['if', '(', '0', '<', 'x', ')', 'then', 'fact', ':=', '(', '1', ')', ';', 'write', '(', 'fact', ')', 'end']
    #tokens=['read', 'x', ';', 'if', 'choice', '=', '0', 'then', 'result', ':=', '(', '0', ')', 'else', 'result', ':=', '(', '1', ')',
    #tokens= ['read', 'x', ';', 'if', 'x', '<', '0', 'then', 'repeat', 'y', ':=', '(', '(', 'z', '+', '1', ')', ')', ';', 'z', ':=', '(', '(', 'z', '*', '2', ')', ')', 'until', 'z', '=', '20', ';', 'write', '(', 'y', ')', 'end']
    #tokens=['fact', ':=', '(', 'x', '+', '3',')']
    #        'end', ';', 'repeat', 'if', '(', '(', '(', 'choice', '=', '0', ')', ')', ')', 'then', 'result', ':=', '(', '(', 'result', '+', 'x', ')', ')', 'else', 'result', ':=', '(', '(', 'result', '*', 'x', ')', ')', 'end', ';', 'x', ':=', '(', '(', 'x', '-', '1', ')', ')', 'until', '(', 'x', '=', '0', ')']
    global length
    length = len(tokens)
    i = 0

    global tree
    cv2.rectangle(tree, (0, 0), (width, height), (255, 255, 255), -1)


    if tokens[0] == 'if':
        parent = node(0, 160, 20, 220, 60, tokens[0])
        i,IF=if_stat(0,parent,tokens)
        IF_LEVEL2=IF
        while(i+1<length):
            i,IF_LEVEL2=check(i+1,IF_LEVEL2,0,tokens)
    elif (tokens[0]=='repeat'):
        parent = node(0, 100, 20, 160, 60, tokens[0])
        i=repeatt(0,parent,tokens)
        REPEAT_2= parent
        while (i+2  < length):
            i, REPEAT_2 = check(i + 1, REPEAT_2, 0,tokens)

    elif(tokens[0]=='write'):
        parent = node(0, 100, 20, 160, 60, tokens[0])
        e=parent.onlyone(1,'id')
        e.addextra(tokens[i + 2])
        # to skip x;
        i += 3
        WRITE_2 = parent
        while (i + 2 < length):
            i, WRITE_2 = check(i + 1, WRITE_2, 0,tokens)
    elif (tokens[0] == 'read'):
        parent = node(0, 20, 20, 80, 60, tokens[0])
        parent.addextra(tokens[i + 1])
        # to skip x;
        i += 2
        READ_2 = parent
        while (i + 2 < length):
            i, READ_2 = check(i + 1, READ_2, 0,tokens)
    else:
        parent = node(0,300, 20, 360, 60, 'assign')
        parent.addextra(tokens[0])
        i=assignt(1,parent,tokens)
        REPEAT_2 = parent
        while (i + 1 < length):
            i, REPEAT_2 = check(i + 1, REPEAT_2, 0, tokens)


    cv2.imshow('heba', tree)
    cv2.waitKey()


    #######################################################################################################################
#syntax_tree('')