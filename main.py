from bottle import route, request, run, response, template, redirect, static_file
import baseLib

db = baseLib.dbLib()

decod = lambda x : x.encode("latin-1").decode("utf-8")

@route("/")
def index():
    return template("template.html", records=db.getNotDeleted(limit=(True, 0, 20)))

@route('/static/<filename>')
def server_static(filename):
    return static_file(filename, root='static/')


@route("/addRecord", method="POST")
def createRecord():
    name = decod(request.forms.get("name"))
    birthdate = decod(request.forms.get("birthdate"))
    distr = decod(request.forms.get("distr"))
    addresses = decod(request.forms.get("addresses"))
    phone = decod(request.forms.get("phone"))
    diagn = decod(request.forms.get("diagn"))
    db.addRecord(name, birthdate, distr, addresses, phone, diagn)
    redirect("/")
    
@route("/delRecord", method="POST")
def deliteRecord():
    recid = decod(request.forms.get("id"))
    db.deleteRecord(recid)
    redirect("/")
    
@route("/searchRecord")
def searchRecord():
    print(str(request.GET.get('id')))
    idr = decod(request.GET.get("id")) if request.GET.get('id') != "" else '-1'
    name = decod(request.GET.get("name"))  if request.GET.get('name') != None else ''
    birthdate = decod(request.GET.get("birthdate"))  if request.GET.get('birthdate') != None else ''
    distr = decod(request.GET.get("distr"))  if request.GET.get('distr') != None else ''
    addresses = decod(request.GET.get("addresses"))  if request.GET.get('addresses') != None else ''
    phone = decod(request.GET.get("phone"))  if request.GET.get('phone') != None else ''
    diagn = decod(request.GET.get("diagn"))  if request.GET.get('diagn') != None else ''
    
    return template(
        "template.html", 
        records=db.search(
            idr,
            name,
            birthdate,
            distr,
            addresses,
            phone,
            diagn,
        ),
    )
    

run(host="192.168.0.3", port="80")
