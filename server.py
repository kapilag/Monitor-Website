from flask import Flask
from Model import FactoryObj
import jinja2
# from hello import getTemplate
app = Flask(__name__)

env = jinja2.Environment(loader=jinja2.FileSystemLoader('./templates'))
template = env.get_template('index.html')
@app.route('/')
def hello_world():
    ret
    print template.render(navigation=FactoryObj.obj_list)
    # d = hello.getTemplate()
    # print d
    return d

if __name__ == '__main__':
    app.run()
