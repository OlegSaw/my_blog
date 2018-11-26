lue', 'yellow', 'magenta']
colors = []
name = []
names2 = defaultdict(dict)
params = [1]

@app.route('/')
def hello_world():
     #name = request.args['name']
     name = "oleg"
     return render_template('hello.html', name = name)


@app.route('/user', methods=['GET', 'POST'])
def user():
    global users
    if request.method == 'GET':
        return render_template('useres.html', users=users)
    if request.method == 'POST':
        name = request.args['name']
        users.append(name)
        return "Success: 200\n"

@app.route('/boxes', methods =['GET', 'POST'])
def boxes():
     global boxesColor
     global colors
     global name
     global names2
     if request.method == 'GET':
          print(names2)
          return render_template('boxes.html', names2=names2)
     if request.method == 'POST':
          color = request.args['color']
          name = request.args['name']
          if color not in boxesColor:
               return "Wrong color\n"
          print(names2.keys())
          if name not in names2.keys() and color not in names2.values():
               box(name, color)
               #names2[name]['color'] = color
               return "Success:200\n"
          else:
               return "Box or Name is alredy\n"

@app.route('/boxes/<name_box>', methods =['GET', 'POST'])
def link_box(name_box):
     global boxesColor
     global colors
     global name
     global param
     global names2
     if request.method == 'GET':
          print(names2[name_box]['param'])
          return render_template('name_box.html', name_box = name_box, color = names2[name_box]['color'], param = params)
     if request.method == 'POST':
          #color = request.args['color']
          name = request.form['name']
          #box(name, color)
          params.append(name)
          print(params)
          
               
def box(name, color):
     names2[name] = dict()
     names2[name]['color'] = color
     names2[name]['param'] = dict()
