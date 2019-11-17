from flask import Flask,render_template,request
import json
import os
from sparql import *

app=Flask(__name__)
@app.route("/")
def hello():
    return render_template('home.html',title='Wiki-Music')
@app.route("/",methods=['POST'])
def get_value():
    s=request.form['search']
    S=request.form['song']
    if(S=="Artists"):
        p,b=con1(s)
        r,v = con2(s)
        if(b):
            p=[]
            p.append("no info")
            p.append("no info")
            p.append("no info")
        return render_template('home.html',title='Wiki-Music | Artist',search=s,records=r,des=p[0],hom=p[1],typ=p[2])
    
    elif(S=="Albums"):
        Albums=con3(s)
        A=[]
        m=0
        for i in Albums:
            t=[]
            if(m<=len((i[0])[0])):
                m=len((i[0])[0])
            t.append((i[0])[0])
            t.append(len(i))
            t.append((i[0])[2])
            A.append(t)
        for j in range(len(A)):
            if(len((A[j])[0])<m):
                for k in range(m-len((A[j])[0])):
                    (A[j])[0]=(A[j])[0]+"\t"
        return render_template('u.html',title='Wiki-Music | Album',search=s,art=A)
    elif(S=="song"):
        Art=con4(s)
        return render_template('u1.html',title='Wiki-Music | Song ',search=s,art=Art)

if __name__ == '__main__':
    app.run(debug=True)
