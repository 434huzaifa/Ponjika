from flask import Blueprint, render_template, request, url_for, redirect, jsonify,make_response,current_app
from .models import Lists,Items
from flask_login import current_user,login_required
from flask_uploads import UploadSet, IMAGES
import requests
from werkzeug.datastructures import  FileStorage
import io
import random
import os
from mongoengine.queryset.visitor import Q
 
views = Blueprint('views', __name__)

photos = UploadSet('images', IMAGES)

MAX_CATE_IMAGES=14

@views.route('/')
@login_required
def home():
    lists=Lists.objects(user=current_user)
    return render_template('home.html',lists=lists,photos=photos,user=current_user,home=True)


@views.route('/add_category/',methods=['GET','POST'])
@login_required
def add_category():
    if request.method=='POST':
        img_no=random.randint(1,MAX_CATE_IMAGES)
        image='/cate_images/'+str(img_no)+'.jpg'
        data=request.form

        
        lst=Lists.objects(Q(user=current_user)&Q(title=data['cate_name'])).first()
        if not lst:
            item=Items(title='s',link='https://www.ggogle.com',about='',item_type='',image='')
            lst=Lists(title=data['cate_name'],about=data['about'],user=current_user,image=image,items=[item])
            lst.save()
            response={'message':'valid Field','error':False}
        else:
            response={'message':'Field Exist','error':True}
        return make_response(response,200)
    return render_template('add_cate.html',photos=photos,user=current_user)


@views.route('/add_item/<string:cate_name>/',methods=['GET','POST'])
@login_required
def add_item(cate_name=False):
    if request.method=='POST':
        data=request.form
        image=request.files['image']
        if image.filename !='':
            image.filename=data['title']+'-' + \
                    cate_name+'.'+image.filename.split('.')[1]
            image=photos.save(image,folder=str(current_user.id)+'/'+cate_name)
            item = Items(title=data['title'], link=data['link'],
                             item_type=data['item_type'], about=data['about'], image=image)
        else:
            item = Items(title=data['title'], link=data['link'],
                             item_type=data['item_type'], about=data['about'])
        
        if cate_name != None:
            lists = Lists.objects(Q(user=current_user)&Q(title=cate_name)).update(push__items=item)
            # response={'message':'Accepted','error':False}
            # return make_response(response,200)
            return redirect('/item_lists/'+cate_name+'/')
    return render_template('new_item.html',photos=photos,user=current_user,cate_name=cate_name)


@views.route('/item_lists/<string:cate_name>/',methods=['GET','POST'])
@login_required
def item_lists(cate_name=None):
    if cate_name==None:
        cate=Lists.objects(user=current_user)
        lst=Lists.objects(user=current_user)
        items=list()
        cate=list()
        for i in lst:
            for j in i.items[1:]:
                items.append(j)
                cate.append(i.title)
    else:
        cate=Lists.objects(Q(user=current_user)&Q(title=cate_name)).first()
        items=Lists.objects(Q(user=current_user)&Q(title=cate_name)).first().items[1:]
    if request.method=='POST':
        keyword=request.form.get('keyword')
        keyword=keyword.strip().lower()
        temp=list()
        if keyword!='':
            for i in items:
                title=str(i['title'])
                title=title.strip().lower()
                if keyword in title:
                    i['image']=photos.url(i['image'])
                    temp.append(i)
        else:
            for i in items:
                i['image']=photos.url(i['image'])
                temp.append(i)
        if len(temp)==0:
            response={'items':'No Item','error':True}
        else:
            response={'items':temp,'error':False}
        return make_response(response,200)
    return render_template('item.html',photos=photos,user=current_user,items=items,cate_name=cate_name,cate=cate,item_list=True)


@views.route('/delete_item/<string:id>/<string:cate_name>/')
@login_required
def item_delete(id,cate_name):
    items=Lists.objects(Q(user=current_user)&Q(title=cate_name)).first().items[1:]
    for i in items:
        if str(i.id) == id:
            
            dir_name=os.path.dirname(photos.path(i.image))
            os.remove(photos.path(i.image))
            Lists.objects(Q(user=current_user)&Q(title=cate_name)).update_one(pull__items__id=id)
            if os.path.isdir(dir_name):
                if not os.listdir(dir_name):
                    os.removedirs(dir_name)
                else:    
                    print("Directory is not empty")
            else:
                print("Given directory doesn't exist")

    return redirect('/item_lists/'+cate_name+'/')

@views.route('/delete_cate/<string:id>/')
@login_required
def cate_delete(id):
    name=Lists.objects(id=id).first().title
    dir_name=current_app.config['UPLOADED_IMAGES_DEST']+'/'+str(current_user.id)+'/'+name  
    Lists.objects(id=id).first().delete()
    import shutil
    if os.path.isdir(dir_name):
        shutil.rmtree(dir_name)
    return redirect('/')

@views.route('/add_anime/<string:cate_name>/',methods=['GET','POST'])
@login_required
def add_anime(cate_name):
    j = ''
    code=''
    keyword=''
    gen="Award Winning,Action,Suspense,Horror,Avant Garde,Sports,Supernatural,Fantasy,Gourmet,Drama,Mystery,Comedy,Slice of Life,Adventure,Romance,Sci-Fi"
    if request.method == 'POST':
        keyword = request.form.get('keyword', '')
        page = request.form.get('page', 1)
        if keyword != '' and len(keyword)>=3:
            url = "https://anime-db.p.rapidapi.com/anime"

            querystring = {"page": page, "size": "20", "search": keyword,'genres':gen}

            headers = {
                "X-RapidAPI-Key": "27f05d3edcmsha0badda065a8ee0p1907a2jsnee57796b818d",
                "X-RapidAPI-Host": "anime-db.p.rapidapi.com"
            }

            response = requests.request(
                "GET", url, headers=headers, params=querystring)
            if response.ok:
                j=response.json()
                code=response.status_code
            if len(j['data'])==0:
                response={'data':j,'error':True}
            else:
                response={'data':j,'error':False}
            return make_response(response,200)
    return render_template('add_anime.html',photos=photos,user=current_user,cate_name=cate_name,api=True)

@views.route('/store_anime/',methods=['POST'])
@login_required
def store_anime():
    if request.method=='POST':
        data=request.form
        img_url=data['image']
        cate_name=data['cate']
        res=requests.get(img_url,allow_redirects=True)
        if res.ok:
            filename=data['title']+'-' +'New'+'.'+img_url.split('/')[-1].split('.')[1]
            f=FileStorage(io.BytesIO(res.content),filename=filename)
            if f.filename != '':
                f = photos.save(f, folder=str(current_user.id))
                item = Items(title=data['title'], link=data['link'],
                             item_type='Video', about=data['about'], image=f)
            else:
                item = Items(title=data['title'], link=data['link'],
                             item_type='Video', about=data['about'])
            Lists.objects(Q(user=current_user)&Q(title=cate_name)).update(push__items=item)
            response={'data':'DONE','error':False}
            return make_response(response,200)


@views.route('/all_items/')
@login_required
def all_item():
    lst=Lists.objects(user=current_user)
    items=list()
    cate=list()
    for i in lst:
        for j in i.items[1:]:
            items.append(j)
            cate.append(i.title)
    return render_template('all_item.html',photos=photos,user=current_user,items=items,cate=cate)


@views.route('/edit_cate/<string:id>/',methods=['GET','POST'])
@login_required
def edit_cate(id):
    lst=Lists.objects(id=id).first()
    if request.method=='POST':
        data=request.form
        Lists.objects(id=id).update(set__title=data['cate_name'])
        Lists.objects(id=id).update(set__about=data['about'])
        response={'message':'valid Field','error':False}
        return make_response(response,200)
    return render_template('edit_cate.html',lst=lst,photos=photos,user=current_user)

@views.route('/edit_item/<string:id>/<string:cate_name>/',methods=['GET','POST'])
@login_required
def edit_item(id,cate_name=False):
    items=Lists.objects(Q(user=current_user)&Q(title=cate_name)).first().items[1:]
    item=''
    index=0
    for i in items:
        index+=1
        if str(i.id)==id: 
            item=i
    if request.method=='POST':
        item=Lists.objects(Q(user=current_user)&Q(title=cate_name),items__id=id)
        data=request.form
        print("➡ data['item_type'] :", data['item_type'])
        image=request.files['image']
        if image.filename !='':
            image.filename=data['title']+'-' + \
                    cate_name+'.'+image.filename.split('.')[1]
            image=photos.save(image,folder=str(current_user.id)+'/'+cate_name)
            item.update(set__items__S__image=image)
        
        item.update(set__items__S__title=data['title'])
        item.update(set__items__S__about=data['about'])
        item.update(set__items__S__link=data['link'])
        item.update(set__items__S__item_type=data['item_type'])
        return redirect('/item_lists/'+cate_name+'/')
    return render_template('edit_item.html',photos=photos,user=current_user,cate_name=cate_name,item=item)

@views.route('/profile/')
@login_required
def profile():

    return render_template('profile.html',photos=photos,user=current_user)

@views.route('/delete_profile/')
@login_required
def delete_profile():
    dir_name=current_app.config['UPLOADED_IMAGES_DEST']+'/'+str(current_user.id)
    import shutil
    if os.path.isdir(dir_name):
        shutil.rmtree(dir_name)
    from .models import User
    User.objects(id=current_user.id).delete()
    return redirect('/logout/')

@views.route('/cate_search/',methods=['GET','POST'])
@login_required
def cate_search():
    cate=''
    if request.method=='POST':
        keyword=request.form.get('keyword')
        if keyword!='':
            cate=Lists.objects(title__icontains=keyword)
        else:
            cate=Lists.objects()
        if len(cate)!=0:
            temp=list()
            for i in cate:
                i['image']=photos.url(i['image'])
                temp.append(i)
            response={'cate':temp,'error':False}
        else:
            response={'cate':'NO DATA FOUNT','error':True}
    return make_response(response,200)


@views.route('/add_movie/<string:cate_name>/',methods=['GET','POST'])
@login_required
def add_movie(cate_name):
    if request.method=='POST':
        keyword=request.form.get('keyword')
        print(keyword)
        page=request.form.get('page',1)

        url = "https://api.themoviedb.org/3/search/movie?api_key=0a02ec5368de6a71ccc01d9d76b0c332&language=en-US&query="+keyword+"&page="+page+"&include_adult=false"
        
        response = requests.request("GET", url)
        response.raise_for_status()
        print(response.status_code)
        if response.ok:
           j=response.json()
        if len(j['results'])==0:
            response={'data':'No Data Found','error':True}
        else:
            response={'data':j,'error':False}
        return make_response(response,200)
    return render_template('add_movie.html',photos=photos,user=current_user,api=True,cate_name=cate_name)

@views.route('/add_tv_show/<string:cate_name>/',methods=['GET','POST'])
@login_required
def add_tv_show(cate_name):
    if request.method=='POST':
        keyword=request.form.get('keyword')
        print(keyword)
        page=request.form.get('page',1)

        url="https://api.themoviedb.org/3/search/tv?api_key=0a02ec5368de6a71ccc01d9d76b0c332&language=en-US&page="+page+"&query="+keyword+"&include_adult=false"
        response = requests.request("GET", url)
        response.raise_for_status()
        print(response.status_code)
        if response.ok:
           j=response.json()
        if len(j['results'])==0:
            response={'data':'No Data Found','error':True}
        else:
            response={'data':j,'error':False}
        return make_response(response,200)
    return render_template('add_tv_show.html',photos=photos,user=current_user,api=True,cate_name=cate_name)

@views.route('/add_manga/<string:cate_name>/',methods=['GET','POST'])
def add_manga(cate_name):
    print(cate_name)
    if request.method=='POST':
            keyword=request.form.get('keyword')
            page=request.form.get('page',1)
            from jikanpy import Jikan
            jikan=Jikan()
            search=jikan.search('manga',keyword,page=page)
            l=len(search['data'])
            delete_idx=[]
            for i in range(len(search['data'])):
                for j in search['data'][i]['genres']:
                    if j['mal_id'] in [28,26,47,9,49,12,50,58]:
                        delete_idx.append(i)
                        break
            print(delete_idx)
            c_ter=0
            for i in delete_idx:
                search['data'].pop(i-c_ter)
                c_ter+=1

            if search['pagination']['items']['total']==0:
                response={'data':'NO DATA','error':True}
            else:
                response={'data':search,'error':False}
            return make_response(response,200)
    return render_template('add_manga.html',photos=photos,user=current_user,api=True,cate_name=cate_name)