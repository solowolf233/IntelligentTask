# -*- coding:utf-8 -*-
from . import product
from flask import url_for,redirect,render_template,request
from ..models import Product

@product.route('/product_detail',methods=['GET'])
def product_detail():
    productId=request.args.get('productId')
    productItem=Product.query.filter_by(productId=productId).first()
    dict={}
    dict['title']=productItem.title
    dict['key']=productItem.key_word
    typeDict = {1:u'Development',2:u'Designing',3:u'Tools',4:u'Unknown'}
    dict['type'] = typeDict[productItem.type]
    dict['desc']=productItem.describe

    return render_template('product/product_detail.html',dict=dict)


@product.route('/product',methods=['GET'])
def product():
    productList1=Product.query.filter_by(type=1).all()
    productList2 = Product.query.filter_by(type=2).all()
    productList3 = Product.query.filter_by(type=3).all()
    dict_one={}
    dict_two={}
    dict_three={}
    for i in range(len(productList1)):
        dict_one[str(i+1)]=productList1[i].productId
        dict_one['title'+str(i+1)]=productList1[i].title
    for i in range(len(productList2)):
        dict_two[str(i+1)]=productList2[i].productId
        dict_two['title'+str(i+1)]=productList2[i].title
    for i in range(len(productList3)):
        dict_three[str(i+1)]=productList3[i].productId
        dict_three['title'+str(i+1)]=productList3[i].title

    return render_template('product/product.html',dict_one=dict_one,dict_two=dict_two,dict_three=dict_three)