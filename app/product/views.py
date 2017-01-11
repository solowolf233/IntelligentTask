# -*- coding:utf-8 -*-
from . import product
from flask import url_for,redirect,render_template


@product.route('/product',methods=['GET'])
def product():
    return render_template('product/product.html')