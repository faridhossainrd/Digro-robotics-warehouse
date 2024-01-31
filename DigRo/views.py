from django.shortcuts import render , redirect ,HttpResponseRedirect
from .forms import ProductsForm
from .models import Allroducts ,orders_storage ,Total , robot_map ,productdata ,productupdate
from django.db.models import Q
from django.http import HttpResponse 
from django.views.decorators.csrf import csrf_protect
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.core.files.storage import FileSystemStorage
from django.core.files import File
from django.http import FileResponse
import sys, pyqrcode
import numpy as np 
# Create your views here. ImageForm
import time
from django import template
register = template.Library()
@register.filter(is_safe=True)
def is_numberic(value):
    return "{}".format(value).isdigit()


map_box_con = {
      1: [1, 2, 0, 0],
      2: [1, 2, 0, 0],
      3: [1, 2, 0, 0],
      4: [1, 2, 0, 0],
      5: [0, 0, 0, 0],
      6: [1, 2, 0, 0],

    }

feedback=False

def order_compilations(ide): 
        orders_storage.objects.filter(id=ide).delete()

def mainupdate():
    item = 0
    product_ = 0
    amount = 0
    sells=0
    order_pending_=0
    all_products = productdata.objects.all()
    for product in all_products:
        item += 1
        product_ += int(product.product_data['Quantity'])
        amount += int(product.product_data['Price'])
    for product in orders_storage.objects.all():
        order_pending_ += 1
        for ord in product.order:
           sells += ord['value'][0] * ord['value'][1]
    
    Total.objects.filter(id=1).update(Items=item, Products=product_ , Amount=amount,order_pending=order_pending_,Sells_amount=sells)
    
def orders(request):
    if request.method == "POST":
           
            ordersa = json.loads(request.POST['result'])
            try:
                if ordersa[0] !="":
                   ordersdata = orders_storage.objects.create(order=ordersa)
                   ordersdata.save()
                   feedback=True
                   #mainupdate()  
            except:
                 print("0 order placement")

    return HttpResponse({'foo':'bar'})

def order_res1(request):
    order_id = ''
    order_p=''
    if request.method == "POST":
        ordersa = request.POST['text']
        for product in orders_storage.objects.all():
            order_id = product.id
            order_p = product.order

    return HttpResponse({'orderid': '5'})

@api_view(['GET',])
def order_res(request):
    order_id = 0
    try:
        for product in orders_storage.objects.all():
                order_id = product.id
                break
    except:
         order_id = 0
    Total.objects.filter(id=1).update(order_processing=order_id)

    return Response({'orderid': order_id})

@api_view(['POST',])
def con_n(request):
    order_id='0'
    if request.method == "POST":
        if request.POST['read_con'] == '0':
            if (Total.objects.get(pk=1).containter!='0'):
                order_id = Total.objects.get(pk=1).containter
        else:
            Total.objects.filter(id=1).update(containter=request.POST['read_con'])
            
    return Response({'con_n': order_id})

@api_view(['POST',])
def request_from_robot(request):
    if request.method == "POST":
        print( request.data['read_con'])
    
    return Response({"farid":345,"rony":54})

@api_view(['POST',])
def con_n1(request):
    order_id='0'
    if request.method == "POST":
        if request.POST['read_con'] == '0':
            if (Total.objects.get(pk=1).containter!='0'):
                order_id = Total.objects.get(pk=1).containter

        else:
            Total.objects.filter(id=1).update(containter=request.POST['read_con'])
            print(Total.objects.get(pk=1).containter)
            
    return Response({'con_n': order_id})

def order_resq(request):

    return render(request, "rest.html")
    
@api_view(['POST',])
def order_com(request):
    if request.method == "POST":
        order_compilations(request.POST['orderid'])
        Total.objects.filter(id=1).update(order_complete=Total.objects.get(pk=1).order_complete + 1)
        Total.objects.filter(id=1).update(order_processing=0)

    return HttpResponse({'orderid': '5'})

def index(request):
    dests = productdata.objects.all()
    return render(request, "index.html", {"dests": dests})
    
def fulfillment(request):
    if request.method == "POST":
        orders(request)
        
    mainupdate()
    dests =  productdata.objects.all() #Allroducts.objects.all()

    return render(request, "fulfillment.html", {"dests": dests, 'totalp': Total.objects.get(pk=1)})
 
def robot_map_pos(id, action):
    
    if action == 'run':
        
        row =  productdata.objects.get(pk=id).product_data["Row"]
        column = productdata.objects.get(pk=id).product_data["cloumn"]
        continar = productdata.objects.get(pk=id).product_data["continar"]
        bin = robot_map.objects.get(pk=1).map[0][continar][2]

        robot_golr_pos = productupdate.objects.get(id=1).product_data["digro1"]
        if (len(robot_golr_pos) > 2) and (robot_golr_pos[0][1]!=2) :

            pos = {
                        
                            "digro1": [ [2,1,1,2,1] , [robot_golr_pos[0][0], robot_golr_pos[0][1] , 2,2,1],[2,2,1,1,1] , [robot_golr_pos[0][0], robot_golr_pos[0][1] , 2,1,1] ] 
                    }
            productupdate.objects.filter(id=1).update(product_data=pos)
        
        else:
            pos = {
                        
                            "digro1": [[2, 1,1,2,1],[robot_golr_pos[0][0], robot_golr_pos[0][1] , 2,2,1]] 
                    }
            productupdate.objects.filter(id=1).update(product_data=pos)
         


    elif action == 'start':

            orders = orders_storage.objects.get(pk=int(id))               
            id = int(orders.order[0]['key'])
            print(id)
            row =  productdata.objects.get(pk=id).product_data["Row"]
            column = productdata.objects.get(pk=id).product_data["cloumn"]
            continar = productdata.objects.get(pk=id).product_data["continar"]
            bin = robot_map.objects.get(pk=1).map[0][continar][2]
            robot_golr_pos = productupdate.objects.get(id=1).product_data["digro1"]
        
            if (bin == 2 ) and (column!=2) :
                 
                pos = {
                            
                                "digro1": [[row, column,1,1,1],[2,2,2,1,1],[row, column,1,2,1],[2, 1,2,2,1]] 
                        }
                productupdate.objects.filter(id=1).update(product_data=pos)
            elif (column == 2):

                 
                pos = {
                            
                                "digro1": [[row, column,1,2,1],[2,1,2,2,1]] 
                        }
                productupdate.objects.filter(id=1).update(product_data=pos)
            else:
                 
                pos = {
                            
                                "digro1": [[row, column,1,1,1],[2,1,2,2,1]] 
                        }
                productupdate.objects.filter(id=1).update(product_data=pos)
    
    elif action == 'load':

            row =  productdata.objects.get(pk=id).product_data["Row"]
            column = productdata.objects.get(pk=id).product_data["cloumn"]
            continar = productdata.objects.get(pk=id).product_data["continar"]
            bin = robot_map.objects.get(pk=1).map[0][continar][2]
            robot_golr_pos = productupdate.objects.get(id=1).product_data["digro1"]
        
            if (bin == 2 ) and (column!=2) :
                 
                pos = {
                            
                                "digro1": [[row, column,1,1,1],[2,2,2,1,1],[row, column,1,2,1],[2, 1,2,2,1]] 
                        }
                productupdate.objects.filter(id=1).update(product_data=pos)
            elif (column == 2):

                 
                pos = {
                            
                                "digro1": [[row, column,1,2,1],[2,1,2,2,1]] 
                        }
                productupdate.objects.filter(id=1).update(product_data=pos)
            else:
                 
                pos = {
                            
                                "digro1": [[row, column,1,1,1],[2,1,2,2,1]] 
                        }
                productupdate.objects.filter(id=1).update(product_data=pos)

    elif action=='stop':
         robot_golr_pos = productupdate.objects.get(id=1).product_data["digro1"]
         print(len(robot_golr_pos))
         robot_golr_pos[0][4] = 0
         robot_golr_pos={
               "digro1": [[robot_golr_pos[0][0] , robot_golr_pos[0][1] ,1,1,0]] 
                 }
         productupdate.objects.filter(id=1).update(product_data=robot_golr_pos)
    

@api_view(['POST',])
def robot_update(request):
    
    robot_golr_pos={}
    if request.method == "POST":
        try:
           
            update = request.data['digro1']
            print(update)
            if (update == "hi"):
                robot_golr_pos = productupdate.objects.get(id=1).product_data["digro1"]

            else:
                robot_golr_pos={
               "digro1": update
                 }
                productupdate.objects.filter(id=1).update(product_data=robot_golr_pos)
                
        except:
            robot_golr_pos={
               "digro1": [1]
                 }
   
    return Response({"digro1":robot_golr_pos})

@api_view(['GET',])
def robot_maps(request):

    return Response({'data': "order_com"})

def get_orderitem(key, value):
    #product_data[value]
    return productdata.objects.get(pk=key).product_data[value]

@api_view(['POST',])
def remove_p(request):
    order_com="Scan the QR code of the product on the screen"
    if request.method == "POST":

            productid = request.POST.get('qrcode')
            productname = request.POST.get('pn')
            orderid = request.POST.get('pr')
            start = request.POST.get('start')
            stop = request.POST.get('stop')
             
            if start == "start":
                 robot_map_pos(int(orderid),"start")
                 #print(orderid)
            elif stop == "stop":
                robot_map_pos(0,stop)
            else:
                    try:
                            alldata = []
                            y={}
                            emtyorder = True
                
                            orders = orders_storage.objects.get(pk=int(orderid))
                            
                            for item in orders.order:
                                if get_orderitem(item['key'], "name") != productname:
                                    y = {
                                                    
                                        'key':  item['key'],
                                        'value': [ item['value'][0],item['value'][1] ]
                                        }
                                    alldata.append(y)
                            orders_storage.objects.filter(id=int(orderid)).update(order=alldata)

                            orders = orders_storage.objects.get(pk=int(orderid))
                            for item in orders.order:
                                emtyorder = False
                            if (emtyorder):
                                orders_storage.objects.filter(id=int(orderid)).delete()

                            robot_map_pos(int(productid),"run")
                    except:
                        order_com = "This is not QR code"
                        print("error to remove")
                        
                    
    
    return Response({'data': order_com})

@api_view(['POST',])
def loadporo(request):
    order_com="Scan again"
    if request.method == "POST":
        try:
            productid = request.POST.get('qrcode')
            product = productdata.objects.get(pk=int(productid)).product_data["name"]

            grade_maping = robot_map.objects.get(pk=2).map
            status = int(grade_maping[0]['status'])
            if status == 1:
                robot_map_pos(int(productid),"load")
                pos = [{
                                
                                    "status": 2
                        }]
                robot_map.objects.filter(pk=2).update(map=pos)
            if status == 2:
                robot_map_pos(int(productid),"run")
                pos = [{
                                
                                    "status": 1
                            }]
                robot_map.objects.filter(pk=2).update(map=pos)

            print(status)
            order_com=productid
        except:
            order_com = "Product not found"
            
    return Response({'data': order_com})

def order_process(request):
    
    alldata = []
    y={}
    emtyorder = True
    emtyorder1=True
    orders = orders_storage.objects.all()
    for items in orders:
        emtyorder1=False
        for item in items.order:
            emtyorder=False
            y = {
                        
                        'name':  get_orderitem(item['key'], "name"),
                        'img': productdata.objects.get(pk=item['key']).Image,
                        'orderQ': item['value'][1],
                        'orderno':items.id,
                }
             
            break
        break
    alldata.append(y)
    if emtyorder1:
        print("no order")
        alldata = []
        y = {
                        
                        'name': "",
                        'img': Allroducts.objects.get(id=1).Image,
                        'orderQ': "",
                        'orderno':"",
    
                }
        alldata.append(y)
   
   
    return render(request, "order_process.html",{"dests": alldata,'totalp': Total.objects.get(pk=1)})

@api_view(['POST',])
def order_fin(request):
    try:
        alldata =[]
        if request.method == "POST":
            pro_name = request.POST.get('pro_name')
            if (pro_name != "No Order found"):
                single_order = orders_storage.objects.get(pk=Total.objects.get(pk=1).order_processing).order
                for product_pro in single_order:
                    if pro_name!= product_pro['key']:
                        y = {
                                
                                'key': product_pro['key'],
                                'value':product_pro['value']
                            
                        }
                        alldata.append(y)
                orders_storage.objects.filter(id=Total.objects.get(pk=1).order_processing).update(order=alldata)
        print("order finish")
        
    except:
        print("exepotion")
    #order_process(request)
    return Response({'con_n': "order_id"})

def registrar(request):
    reg_ck=False
    if request.method == "POST":
        chk = request.POST.get('Container')
        if (chk == "add"):
            reg_ck=False
        else:
            print(chk)
            form = ProductsForm(request.POST, request.FILES)
            
            if (chk == "please wait.. & try again"):
                reg_ck=False
            else:
                    if form.is_valid():
                        form.save()
                        Total.objects.filter(id=1).update(containter='0')
                        reg_ck = True
    
    form = ProductsForm()

    return render(request, "registration.html", {'form':form,'creg_ck':reg_ck})

def qr_make(product_serial):
    qr = pyqrcode.create(product_serial)
    productQR = str(product_serial)+".png"
    qr.png(productQR, scale=6)

def load_calculation(space):
    w = 15
    l = 15
    h = 5
    weight = 0.5  #KG
    area = w * l * h

    space = 0
    
    return  space
    
def bin_load(load_space):
    grade_maping = robot_map.objects.get(pk=1).map
    maxspace = int(grade_maping[0]['1'][3])
    print(maxspace)
    bin="1"
    for grade in grade_maping[0]:
        
        
        if (int(grade_maping[0][grade][3]) > maxspace):

            maxspace = int(grade_maping[0][grade][3])
            if (int(load_space) <= maxspace):
                bin = grade
                print(bin)
            print(maxspace)
        
    loodv = int((grade_maping[0][bin][3])) - int(load_space)
    if loodv > 0:
        grade_maping[0][bin][3] =loodv
        robot_map.objects.filter(id=1).update(map=grade_maping)
        loodv=1
    else:
       loodv=0
    return [ bin, grade_maping[0][bin][0] , grade_maping[0][bin][1],loodv ]
    
def get_data(request):
    name = request.POST['name']
    ditails = request.POST['Details']
    Price = request.POST['Price']
    Quantity = request.POST['Quantity']
    Weight = request.POST['Weight']
    size_w = request.POST['s_w']
    size_h = request.POST['s_h']
    size_l = request.POST['s_l']
    mdday = request.POST['mdday']
    mdmonth = request.POST['mdmonth']
    mdyear = request.POST['mdyear']
    edday  = request.POST['edday']
    edmonth = request.POST['edmonth']
    edyear  = request.POST['edyear']
    Image = request.FILES['Image']
    

    # fs = FileSystemStorage()
    # uploaded_file_url = fs.url(myfile)
    # print(uploaded_file_url)
    load_space = int(size_w) * int(size_h) * int(size_l)
    bin_place = bin_load(load_space)
    if bin_place[3]>0:
        jesondata = {

                "name": name,
                "ditails": ditails,
                "Price": Price,
                "Quantity": Quantity,
                "Weight": Weight,
                "size_w": size_w,
                "size_h": size_h,
                "size_l": size_l, 
                "mdday": mdday, 
                "mdmonth": mdmonth, 
                "mdyear": mdyear,
                "edday": edday,
                "edmonth": edmonth,
                "edyear": edyear,

                "cloumn": bin_place[1],
                "Row": bin_place[2],
                "continar": bin_place[0],
                "loadspace": load_space,
                
                
        }
        
        json_dump = json.dumps(jesondata)
        json_object = json.loads(json_dump)

        #product_data = json.loads(alldata)
        reg_product = productdata.objects.create(product_data = json_object, Image = Image)
        reg_product.save()
        qr_make(reg_product.id)
        regs= 'Registration_Success!'
    else:
      regs= 'Registration_Not_Success!'

    return regs
    
def regf(request):
    reg_status = "Null"
    if request.method == "POST":
        reg_status = get_data(request)

    
    return render(request, "regf.html",{"regs":reg_status} )

def load(request):
    mainupdate()
    dests = productdata.objects.all()  #Allroducts.objects.all()

    return render(request, "load.html", {'totalp': Total.objects.get(pk=1)})

@api_view(['POST',])
def getitem(request):
    img=""
    if request.method == "POST":
            try:
                id = request.POST.get('id')
                print(id)
                img = productdata.objects.get(pk=int(id)).Image
                print(img)
            except:
                g = 0
                print("error")

    return HttpResponse({img})
    
def getitem1(request):
    name="none"
    if request.method == "POST":
            try:
                id = request.POST.get('id')
                name = productdata.objects.get(pk=int(id)).product_data["name"]
            except:
                g = 0
                
              
    return HttpResponse({name})
 