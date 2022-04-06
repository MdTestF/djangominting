from asyncio.windows_events import NULL
from logging import exception
from turtle import st
from .serializers import RegisterSerializer,ImageSerializer,PinataUploadSerializer,RegisterNorSerializer,RegisterBoSerializer,RoleSerializer1,RoleSerializer,ActionSerializer,RoleActionSerializer
from rest_framework import generics
from base.models import User,Image,PinataUpload,Role,RoleUser,Action,RoleAction
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny

import os
import subprocess



from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

import jwt
from django.conf import settings

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['is_verified'] = user.is_verified
        return token

class MyTokenObtainPairView(TokenObtainPairView):
     serializer_class = MyTokenObtainPairSerializer

@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/api/token',
        '/api/token/refresh',
        '/api/register/',
    ]
    return Response(routes)

@api_view(['GET'])
def allImage(request,pk):
    images =  Image.objects.all()
    # user = User.objects.get(id=pk)
    # print(user.acTitle)
    imageUrl=[]
    for image in images:
        if(str(image.user_id)==pk):
          imageUrl.append({'id':image.id,'photo':str(image.photo),'url':image.url,'status':image.status,'Qc Status':image.is_qcPassed,'Comment':image.is_readyForNft})
    serializer = ImageSerializer(images, many=True)
    #return Response(serializer.data)
    return Response(imageUrl)


@api_view(['GET'])
def allUploadedImage(request):
    images =  Image.objects.all()
    imageUrl=[]
    for image in images:
        user=User.objects.get(id=str(image.user_id))
        st=str(image.created)
        imageUrl.append({'id':image.id,'photo':[str(image.photo),image.url],'status': image.status+"\n"+st,'user':[{'name':user.acTitle,'user_id':image.user_id}],'QcStatus':image.is_qcPassed,'Comment':image.is_readyForNft})
    serializer = ImageSerializer(images, many=True)
    #return Response(serializer.data)
    return Response(imageUrl)

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

class VerifyEmail(generics.GenericAPIView):
    def get(self,request):
        token=request.GET.get('token')
        try:
            payload=jwt.decode(token,settings.SECRET_KEY,algorithms=["HS256"])
            # print(payload['user_id'])
            user= User.objects.get(id= payload['user_id'])
            # print(user)
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({'email':'Sucessfully Activate'})
        except jwt.ExpiredSignatureError as e:
            return Response({'error':'Activation link exp.'})
        except jwt.exceptions.DecodeError as e:
            return Response({'error':'Invalid token.'})

@api_view(['POST'])
def imageUpload(request): 
    id = request.data['id']    
    image=Image.objects.create(user_id=id,photo=request.data['photo'])
    image.url=str('http://127.0.0.1:8000/media/')+str(image.photo)
    image.save()
    serializer = ImageSerializer(image)
    return HttpResponse({'message': 'Photo up'}, status=200)

@api_view(['POST'])
def imageStatusChange(request):
    data=(request.data)
    image=Image.objects.get(id=data['id'])
    image.is_qcPassed=data['value']
    image.save()
    # return Response(serializer.data)
    return Response("Status Change Successfully")

@api_view(['POST'])
def saveComment(request):
    data=(request.data)
    image=Image.objects.get(id=data['id'])
    image.comment=data['value']
    image.save()
    return Response("Comment Save")

@api_view(['POST'])
def saveContractInfo(request):
    data=(request.data)
    image=Image.objects.get(id=data['id'])
    image.collectionName=data['fromValues']['nameOfCol']
    image.collectionSym=data['fromValues']['nameOfSym']
    image.save()
    return Response('Contact Info Save Successfully')

@api_view(['POST'])
def indivudualAllImages(request,pk):
    images =  Image.objects.all()
    imageUrl=[]
    for image in images:
        if(str(image.user_id)==pk):
          user=User.objects.get(id=str(image.user_id))
          imageUrl.append({'id':image.id,'photo':[str(image.photo),image.url],'user':[{'name':user.acTitle}],'status':image.status,'QcStatus':image.is_qcPassed,'Comment':image.comment,'Wallet Address':image.userWalletAddress,'Contact Address':image.contractAddress,'CID':image.imageCID,'pinataStatus':image.pinataUpload,'openSeaUpload':image.openSeaUpload,'minted':image.minted,'price':image.price+str('ETH'),'Sell Order':image.sellOrder,'Soled':image.soled})
        
    serializer = ImageSerializer(images, many=True)
    return Response(imageUrl)


@api_view(['POST'])
def setEventInfo(request):
    data=(request.data)
    #print(data[0]['contarctID'])
    # print(len(request.data))
    print(data)
    image=Image.objects.get(contractAddress=data[0]['contarctID'])
    #print(image)

    for dic in data:
        print(dic)
        for d in dic:
            val=dic[d].split("_")[0]
            if(val=='Soled'):
                image.soled=dic[d]
            elif(val=='Minted'):  
                image.minted=dic[d]
            elif(val=='Sell Order'): 
                image.sellOrder=dic[d]
            elif(val=='Sell Order Cencelled'):
                image.sellOrder=dic[d]
        image.save()  
    return Response('Contact Info Save Successfully')

@api_view(['GET'])
def getSellOrderContract(request):
    images =  Image.objects.all()
    imageUrl=[]
    for image in images:
        if(image.sellOrder.split("_")[0]=='Sell Order'):
            print(image.sellOrder)
            imageUrl.append(image.contractAddress)
    return Response(imageUrl)


@api_view(['GET'])
def orderPrice(request):
    image=Image.objects.get(id=1)
    return Response( image.price)

@api_view(['POST'])
def saveOrderPrice(request):
    print(request.data['contactAddress'])
    image=Image.objects.get(contractAddress=request.data['contactAddress'])
    image.price=request.data['price']
    image.save()
    return Response(image.price)

@api_view(['GET'])
def getContract(request):
    image=Image.objects.get(id=1)
    return Response(image.contractAddress)  

@api_view(['GET'])
def getAllContract(request):
    images=Image.objects.all()
    contArr=[]
    for image in images:
        if(image.contractAddress!=None):
            print(image.contractAddress)
            contArr.append(image.contractAddress)

    return Response(contArr)  

# @api_view(['GET'])
# def createContract(request):
#     os.chdir(r'D:\Second Part With Contract Gen\secondPart')
#     sub = subprocess.Popen("npx hardhat run scripts/deploy.js --network rinkeby", shell=True, stdout=subprocess.PIPE,cwd=os.getcwd())
#     subprocess_return = sub.stdout.read()
#     print(subprocess_return)
#     return Response(subprocess_return)


@api_view(['POST'])
def upPinataImg(request):
    
    os.chdir(r'D:\Version1\Authentication\backend')

    upPinimgs = PinataUpload.objects.all()

    for up in upPinimgs:
        up.delete()

    upPinimg = PinataUpload.objects.create(
        upImage=request.data
    )
    
    serializer = PinataUploadSerializer(upPinimg)

    sub = subprocess.Popen("node copyimage.js", shell=True, stdout=subprocess.PIPE,cwd=os.getcwd())
    subprocess_return = sub.stdout.read()
    print(subprocess_return)

    sub = subprocess.Popen("node renameImage.js", shell=True, stdout=subprocess.PIPE,cwd=os.getcwd())
    subprocess_return = sub.stdout.read()
    print(subprocess_return)

    sub = subprocess.Popen("node index.js", shell=True, stdout=subprocess.PIPE,cwd=os.getcwd())
    subprocess_return = sub.stdout.read()
    print(subprocess_return)

    sub = subprocess.Popen("node generate.js", shell=True, stdout=subprocess.PIPE,cwd=os.getcwd())
    subprocess_return = sub.stdout.read()
    print(subprocess_return)

    sub = subprocess.Popen("node update.js", shell=True, stdout=subprocess.PIPE,cwd=os.getcwd())
    subprocess_return = sub.stdout.read()
    print(subprocess_return)

    sub = subprocess.Popen("node upload.js", shell=True, stdout=subprocess.PIPE,cwd=os.getcwd())
    subprocess_return = sub.stdout.read()
    print(subprocess_return)

    return Response(serializer.data)

@api_view(['GET'])
def getClickUp(request):
    image=PinataUpload.objects.first()
    return Response(image.upImage) 

@api_view(['POST'])
def saveCID(request):
    print(request.data['img'])
    image=Image.objects.get(photo=request.data['img'])
    image.imageCID=request.data['CID']
    image.save()
    return Response('Contract Save Successfully')

@api_view(['POST'])
def getCID(request):
    print(request.data['img'])
    image=Image.objects.get(photo=request.data['img'])
    print('The is from',image.imageCID) 
    return Response(image.imageCID)

@api_view(['POST'])
def getjsonCID(request):
    print(request.data['img'])
    image=Image.objects.get(photo=request.data['img'])
    info={'cid':image.jsonCID,'collectName':image.collectionName,'symName':image.collectionSym}
    return Response(info)


@api_view(['POST'])
def saveJsonCID(request):
    print(request.data['img'])
    image=Image.objects.get(photo=request.data['img'])
    image.jsonCID=request.data['jsonCid']
    image.pinataUpload="Uploded"
    image.save()
    return Response('JsonCid Save Successfully')


@api_view(['POST'])
def generateNFT(request):
    os.chdir(r'D:\Version1\secondPart')
    sub = subprocess.Popen("npx hardhat run scripts/deploy.js --network rinkeby", shell=True, stdout=subprocess.PIPE,cwd=os.getcwd())
    subprocess_return = sub.stdout.read()
    print(subprocess_return)
    return Response(subprocess_return)


@api_view(['POST'])
def saveContract(request):
    print(request.data['img'])
    image=Image.objects.get(photo=request.data['img'])
    image.contractAddress=request.data['contract'] 
    image.userWalletAddress=request.data['waladdress']
    image.openSeaUpload='Uploaded'
    image.save()
    return Response('Contract Save Successfully')


######################################################

class RegisterUserNor(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny,]
    serializer_class = RegisterNorSerializer

@permission_classes([IsAuthenticated])
class RegisterUserBo(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny,]
    serializer_class = RegisterBoSerializer


@api_view(['GET'])
#@permission_classes([IsAuthenticated])
def getRoles(request):
    roles = Role.objects.all()
    serializer=RoleSerializer1(roles,many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def setUserRole(request):
    roles=request.data['roles']
    print(roles)
    for role in roles:
        result=Role.objects.get(role_name=role)
        print(result.id)
        result1=User.objects.get(email=request.data['email'])
        print(result.id)
        userRole = RoleUser.objects.create(
            user_id=result1.id,
            role_id=result.id
        )
        userRole.save()
    return Response('Save SucessFully')

#######################################################

@api_view(['GET'])
def GetSingleOrAllAction(request,action_name=None):
    if(action_name):
        result=Action.objects.get(action_name=action_name)
        serializer=ActionSerializer(result)
        return Response(serializer.data)
        #return Response({"status": "success", "data": serializer.data}, status=200)

    result = Action.objects.all()
    serializer = ActionSerializer(result, many=True)
    return Response(serializer.data)
    #return Response({"status": "success", "data": serializer.data}, status=200)



@api_view(['GET'])
def RoleAllOrSingle(request,role_name):
    items = Role.objects.all()
    roleUrl=[]
   
    for item in items:
        if(str(item.role_name)==role_name):
          roleUrl.append({
              'id':item.id,              
              'role_name':item.role_name
              })
        
    serializer = RoleSerializer(items, many=True)
    #return Response(serializer.data)
    return Response(serializer.data)


@api_view(['POST'])
def RoleActionSave(request): 
    # try:
        if(request.data['role_name']!=''):

            role = Role.objects.create(
                role_name=request.data['role_name'],
            )        
            role.save()        
            actionids=request.data['actions']        
            for actionid in actionids:
                action=Action.objects.get(id=actionid) 
                roleaction = RoleAction.objects.create(
                    role=role, 
                    action=action 
                )        
                roleaction.save()            
            return Response({'roleaction':'Data Saved Sucessfully'})

        else:
            return Response({'roleaction':'You need to write RoleName'})
    # except:        
    #     return Response({'error':'Data not Saved'},status=400)


@api_view(['POST'])
def RoleActionEdit(request): 
    #try:
        role_id=request.data['role']
        actionids=request.data['actions']
        RoleAction.objects.filter(role_id=role_id).delete()
        for actionid in actionids:
            role=Role.objects.get(id=role_id)
            action=Action.objects.get(id=actionid)               
            roleAction = RoleAction.objects.create(
                action=action,
                role=role
            )
            roleAction.save()
        return Response({'roleaction':'Data Updated Sucessfully'})   


@api_view(['GET'])
def RoleWiseActionAllOrSingle(request,id):      
    items = RoleAction.objects.all();
    roleAction=[]
    for item in items:
        if(str(item.role_id)==id):
            roleAction.append({
              'id':item.id, 
              'action_id':item.action_id,            
              'role_id':item.role_id,
              
              })              
            serializer = RoleActionSerializer(roleAction, many=True)
    serializer = RoleActionSerializer(items, many=True)
    return Response(roleAction)




    ###########################################################



@api_view(['POST'])
def imageUpload1(request): 
    print(request.data)
    id = request.data['id']  
    #isLocal= request.POST.get('islocal')
    imageSellType=request.POST.get('selltype')
    isGenerateVariation=request.POST.get('isgeneratevariation')
    productTitle = request.POST.get('imgtitle') 
    price= request.POST.get('price')
    sale_price=request.POST.get('saleprice')
    description=request.POST.get('description')
    image=Image.objects.create(
        product_title=productTitle,
        user_id=id,
        photo=request.data['photo'],
        islocal=True,
        imageselltype=imageSellType,
        isgeneratevariation=isGenerateVariation,        
        price=price,
        sale_price=sale_price,
        description=description
    )
    image.url=str('http://127.0.0.1:8000/media/')+str(image.photo)    
    image.save()
    return HttpResponse({'message': 'Photo up'}, status=200)


@api_view(['GET'])
def allImage1(request,pk):
    images =  Image.objects.all()
    imageUrl=[]
   
    for image in images:
        if(str(image.user_id)==pk):
          imageUrl.append({
              'id':image.id,
              'product_title':image.product_title,
              'price':image.price,
              'sale_price':image.sale_price,
              'photo':str(image.photo),
              'url':image.url,
              'status':image.status,
              'islocal':image.islocal,
              'imageselltype':image.imageselltype,
              'isgeneratevariation':image.isgeneratevariation,              
              'short_description':image.short_description,
              'description':image.description,

              })
        
    serializer = ImageSerializer(images, many=True)
    #return Response(serializer.data)
    return Response(imageUrl)





@api_view(['GET'])
def getBoUser(request):
    boUser = User.objects.all()
    userBo = []
    for bo in boUser:
        if(bo.is_boUser==1):
            userBo.append(bo.email)
    return Response(userBo)

@api_view(['GET'])
def getSingleUserRole(request,email):
    print(email)
    result=User.objects.get(email=email)
    roleUser = RoleUser.objects.all()
    userRole = []
    for ru in roleUser:
        if(ru.user_id==result.id):
            role = Role.objects.get(id=ru.role_id)
            userRole.append(role.role_name)
    print(userRole)
    return Response(userRole)
   