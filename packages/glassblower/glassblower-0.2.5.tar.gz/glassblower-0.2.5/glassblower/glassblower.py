"""
el objetivo es hacer un programa que haga
todo el esqueleto de glassblower
"""
"""
1) crear diccionario
"""
import os
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("new")
parser.add_argument("project")
args = parser.parse_args()

#NAME = 'project'

glassblower_structure = {
	'app': {
		'__init__' : {
			'type': 'file',
			'name': '__init__.py',
			'from': {
				'config' : '*',
				'flask' : ['Flask'],
				'flask.ext.sqlalchemy' : ['SQLAlchemy'],
				'flask.ext.via' : ['Via']
			},
			'import': [],
			'content': [
				"app = Flask(__name__ )",
				"app.config.from_object('config.DevelopmentConfig')",
				"app.config['VIA_ROUTES_MODULE'] = 'config.routes'",
				"db = SQLAlchemy(app)",
				"via = Via()",
				"via.init_app(app, routes_name='urls')"
			],
			'main': False,
			'main_content': []	
		},
		'forms': ['__init__.py']
		,
		'models': ['__init__.py']
		,
		'static':[
			'fonts',
			'images',
			'js',
			{'css': ['reset.css',
					'style.css'
					]
			}
		],
		'templates':[
			{
					'type': 'file',
					'name': 'about.html',
					'from': {},
					'import': [],
					'function': [],
					'classes': [],
					'content': [
						"{% extends \"base.html\" %}",
						"{% block content %}",
						"<h1>GlassBlower Project</h1>",
						"<h2>Blas Martin Castro</h2>",
						"<h3>castro.blas.martin@gmail.com</h3>",
						"{% endblock %}"
					],
					'main': False,
					'main_content': []	
			},
			{
				'type': 'file',
				'name': 'base.html',
				'from': {},
				'import': [],
				'function': [],
				'classes': [],
				'content': [
					"<!DOCTYPE html>",
					"<html>",
					"<head>",
					"<meta charset='utf-8' />",
					"<meta name=\"viewport\" content=\"width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no\">",
					"<title>GlassBlower</title>",
					"<link rel=\"stylesheet\" href=\"{{ url_for('static', filename='css/reset.css') }}\">",
					"<link rel=\"stylesheet\" href=\"http://code.ionicframework.com/ionicons/2.0.1/css/ionicons.min.css\">",
					"<link rel=\"stylesheet\" href=\"https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css\">",
					"<script type=\"text/javascript\" src=\"https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js\"></script>",
					"<link rel=\"stylesheet\" href=\"{{ url_for('static', filename='css/style.css') }}\">",
					"</head>",
					"<body>",
					"<nav class=\"navbar navbar-default\">",
					"<div class=\"container-fluid\">",
					"<div class=\"navbar-header\">",
					"<a class=\"navbar-brand\" href=\"#\">GlassBlower</a>",
					"</div>",
					"<ul class=\"nav navbar-nav\">",
					"<li ><a href=\"/\">Home</a></li>",
					"<li><a href=\"/about\">About</a></li>",
					"</ul>",
					"</div></nav><div>{% block content %}{% endblock %}</div></body></html>"
				],
				'main': False,
				'main_content': []	
			},
			{
				'type': 'file',
				'name': 'index.html',
				'from': {},
				'import': [],
				'function': [],
				'classes': [],
				'content': [
					"{% extends \"base.html\" %}",
					"{% block content %}",
					"<div class='container'>",
					"<h1 class='text-center'>Welcome to GlassBlower</h1>",
					"<h2 class='text-center'>Powered by Flask</h2>",
					"</div>",
					"{% endblock %}"
				],
				'main': False,
				'main_content': []	
			}
		],
		'views': [{
					'type': 'file',
					'name': '__init__.py',
					'from': {
						"index" : "*",
						"about" : "*"
					},
					'import': [],
					'function': [],
					'classes': [],
					'content': [],
					'main': False,
					'main_content': []
				 },
				 {
				 	'type': 'file',
					'name': 'about.py',
					'from': {
						'flask.views': ['MethodView'],
						'flask': ['render_template'],
						'flask.ext.login': ['login_required']
					},
					'import': [],
					'classes':[
						{
							'name': 'About',
							'inheritance': ['MethodView'],
							'attr' : {
							},
							'function': [
								{
									'name':'get',
									'parameters':[

									],
									'content':["return render_template('about.html')"]
								},
								{
									'name':'post',
									'parameters':[

									],
									'content':[
										"pass"
									]
								},
								{
									'name':'put',
									'parameters':[

									],
									'content':[
										"pass"
									]
								},
								{
									'name':'delete',
									'parameters':[

									],
									'content':[
										"pass"
									]
								}
							]
						}
					],
					'content': [],
					'main': False,
					'main_content': []	
				 },
				 {
				 	'type': 'file',
					'name': 'index.py',
					'from': {
						'flask.views': ['MethodView'],
						'flask': ['render_template'],
						'flask.ext.login': ['login_required']
					},
					'import': [],
					'classes':[
						{
							'name': 'Index',
							'inheritance': ['MethodView'],
							'attr' : {
							},
							'function': [
								{
									'name':'get',
									'parameters':[
									],
									'content':[
										"return render_template('index.html')"
									]
								},
								{
									'name':'post',
									'parameters':[
									],
									'content':[
										"pass"
									]
								},
								{
									'name':'put',
									'parameters':[
									],
									'content':[
										"pass"
									]
								},
								{
									'name':'delete',
									'parameters':[
									],
									'content':[
										"pass"
									]
								}
							]
						}
					],
					'content': [],
					'main': False,
					'main_content': []	
				 }]
	},
	'config': [
			  {
				'type': 'file',
				'name': '__init__.py',
				'from': {
					"config" : "*"
				},
				'import': [],
				'function': [],
				'classes': [],
				'content': [],
				'main': False,
				'main_content': []
			  },
	          {
				'type': 'file',
				'name': 'config.py',
				'from': {},
				'import': ['os'],
				'classes':[
					{
						'name': 'BaseConfig',
						'inheritance': [],
						'attr' : {
							'DEBUG ': 'False',
							'SECRET_KEY' : '"always you can choose"',
							'SQLALCHEMY_DATABASE_URI' : '"sqlite:///" + os.getcwd() + "/yourdatabase.db"',
							'SQLALCHEMY_TRACK_MODIFICATIONS' : 'True'
						},
						'function': []
					},
					{
						'name': 'DevelopmentConfig',
						'inheritance': ['BaseConfig'],
						'attr' : {
							'DEBUG' : 'True',
						},
						'function': []
					},
					{
						'name': 'ProductionConfig',
						'inheritance': ['BaseConfig'],
						'attr' : {
							'DEBUG' : 'False',
						},
						'function': []
					}
				],
				'content': [],
				'main': False,
				'main_content': []	
			  },
	          {
	          	'type': 'file',
				'name': 'routes.blz',
				'from': {},
				'import': [],
				'function': [],
				'classes': [],
				'content': [
					'/,Index,index\n',
					'/about,About,about'
				],
				'main': False,
				'main_content': []	
	          },
	          {
				'type': 'file',
				'name': 'routes.py',
				'from': {
					'flask.ext.via.routers.default':['Pluggable as p'],
					'app.views':'*'
					},
				'import': [],
				'function': [],
				'classes': [],
				'content': [
					"urls = list()",
					"with open('config/routes.blz','r') as file:",
					"\tfor row in file:",
					"\t\tp_row = row.replace(" +  repr('\n') + ",'').replace(' ','').split(',')",
					"\t\texec(\"urls.append(p('%s', %s, '%s'))\" % (p_row[0], p_row[1], p_row[2]))"
				],
				'main': False,
				'main_content': []	
	          }
	 ],
	'test': [],
	'utilities':[],
	'others':[
		'.gitignore',
		'.gitattributes',
		'Procfile',
		{
			'type': 'file',
			'name': 'requirements.txt',
			'from': {},
			'import': [],
			'function': [],
			'classes': [],
			'content': [
				'Flask==0.10.1',
				'Flask-Admin==1.4.2',
				'Flask-HTTPAuth==3.1.2',
				'Flask-Login==0.3.2',
				'Flask-Mail==0.9.1',
				'Flask-Migrate==1.8.0',
				'Flask-RESTful==0.3.5',
				'Flask-SQLAlchemy==2.1',
				'Flask-Script==2.0.5',
				'Flask-Via==2015.1.1',
				'Flask-WTF==0.12',
				'Jinja2==2.8',
				'Mako==1.0.4',
				'MarkupSafe==0.23',
				'PyMySQL==0.7.5',
				'SQLAlchemy==1.0.14',
				'WTForms==2.1',
				'Werkzeug==0.9.4',
				'alembic==0.8.6',
				'aniso8601==1.1.0',
				'argparse==1.2.1',
				'blinker==1.4',
				'click==6.6',
				'gunicorn==19.6.0',
				'itsdangerous==0.24',
				'passlib==1.6.5',
				'python-dateutil==2.5.3',
				'python-editor==1.0.1',
				'pytz==2016.4',
				'six==1.10.0',
				'wsgiref==0.1.2'
			],
			'main': False,
			'main_content': []
		},
		'vendor.yml',
		{
			'type': 'file',
			'name': 'manage.py',
			'from': {
					'flask.ext.script': ['Manager', 'Server']
					,
					'flask.ext.migrate': ['Migrate', 'MigrateCommand']
					,
					'app': ['app', 'db']
					},
			'import': [],
			'function': [],
			'classes': [],
			'content': [
				'migrate = Migrate(app, db)',
				'manager = Manager(app)',
				'server = Server(host="0.0.0.0", port=9000)',
				'manager.add_command("db", MigrateCommand)',
				'manager.add_command("runserver", server)'
			],
			'main': True,
			'main_content': ['manager.run()']	
		},
		{
			'type': 'file',
			'name': 'glassblower.py',
			'from': {},
			'import': ['os', 'argparse'],
			'function': [],
			'classes': [],
			'content': [
				'parser = argparse.ArgumentParser()',
				'parser.add_argument("blow")',
				'parser.add_argument("option")',
				'parser.add_argument("--newFile")',
				'args = parser.parse_args()',
				'currentPath = os.getcwd()',
				"\ndef make_template():",
				"\thtmlDir = False",
				"\thtmlDir = os.path.join(currentPath, 'app', 'templates', args.newFile.lower() + '.html')",
				"\twith open(htmlDir,'w') as af:",
				"\t\taf.write('{% extends \"base.html\" %}' + " + repr('\n') +")",
				"\t\taf.write(" + repr('\n') +")",
				"\t\taf.write('{% block content %}' + " + repr('\n') +")",
				"\t\taf.write('<h1 class=\"text-center\">%s</h1>%s'  % (args.newFile.upper(), " + repr('\n') +"))",
				"\t\taf.write(" + repr('\n') +")",
				"\t\taf.write('{% endblock %}' +" + repr('\n') +")",
				"\treturn htmlDir\n",
				"\ndef make_view(api=False):",
				"\tfileDir = os.path.join(currentPath, 'app', 'views', args.newFile.lower() + '.py')",
				"\twith open(fileDir,'w') as af:",
				"\t\taf.write('from flask.views import MethodView' +" + repr('\n') +")",
				"\t\taf.write('from flask import render_template' +" + repr('\n') +")",
				"\t\taf.write(" + repr('\n') +")",
				"\t\taf.write('class %s(MethodView):%s' % (args.newFile.capitalize(), " + repr('\n') +"))",
				"\t\taf.write(" + repr('\n') +")",
				"\t\taf.write('\tdef get(self):' +" + repr('\n') +")",
				"\t\tif api:",
				"\t\t\taf.write('\t\treturn \"%s\"%s'  % (args.newFile.lower(), " + repr('\n') +"))",
				"\t\telse:",
				"\t\t\taf.write('\t\treturn render_template(\"%s.html\")%s' % (args.newFile.lower(), " + repr('\n') +"))",
				"\t\tmethod_list = ['post', 'put', 'delete']",
				"\t\tfor method in method_list:",
				"\t\t\taf.write(" + repr('\n') +")",
				"\t\t\taf.write('\tdef %s(self):%s' % (method, " + repr('\n') +"))",
				"\t\t\taf.write('\t\tpass' +" + repr('\n') +")",
				"\tinitDir = os.path.join(currentPath, 'app', 'views', '__init__.py')",
				"\twith open(initDir,'a') as af:",
				"\t\taf.write('%sfrom %s import * %s' % (" + repr('\n') + ",args.newFile.lower(), " + repr('\n') +"))",
				"\thtmlDir = False",
				"\tif not api:",
				"\t\thtmlDir = make_template()",
				"\troutesDir = os.path.join(currentPath, 'config', 'routes.blz')",
				"\twith open(routesDir,'a') as af:",
				"\t\taf.write(\"%s/%s,%s,%s\" % (" + repr('\n') +",args.newFile.lower(), args.newFile.capitalize(), args.newFile.lower()))",
				"\tprint fileDir",
				"\tprint initDir",
				"\tif htmlDir:",
				"\t\tprint htmlDir",
				"\tprint routesDir\n",
				"\ndef make_model():",
				"\tfileDir = os.path.join(currentPath, 'app', 'models', args.newFile.lower() + '.py')",
				"\twith open(fileDir,'w') as af:",
				"\t\taf.write('from manage import app, db' +" + repr('\n') +")",
				"\t\taf.write('from sqlalchemy import ForeignKey' +" + repr('\n') +")",
				"\t\taf.write('from sqlalchemy.orm import relationship' +" + repr('\n') +")",
				"\t\taf.write(" + repr('\n') +")",
				"\t\taf.write('class %s(db.Model):%s' % (args.newFile.capitalize(), " + repr('\n') +"))",
				"\t\taf.write(" + repr('\n') +")",
				"\t\taf.write('\t__tablename__ = \"%s\"%s' % (args.newFile.lower(), " + repr('\n') +") )",
				"\t\taf.write('\tid = db.Column(db.Integer, primary_key=True)')",
				"\tinitDir = os.path.join(currentPath, 'app', 'models', '__init__.py')",
				"\twith open(initDir,'a') as af:",
				"\t\taf.write('%sfrom %s import *%s' % ( " + repr('\n') +",args.newFile.lower(), " + repr('\n') +"))",
				"\tprint fileDir",
				"\tprint initDir\n",
				'print("Updated Directories")',
				'if args.blow == "blow" and args.option == "view":',
    			'\tmake_view()',
				'elif args.blow == "blow" and args.option == "model":',
    			'\tmake_model()',
				'elif args.blow == "blow" and args.option == "api":',
    			'\tmake_view(api=True)',
    			'\tmake_model()',
				'elif args.blow == "blow" and args.option == "scaffold":',
    			'\tmake_view()',
    			'\tmake_model()',
				'elif args.blow == "blow" and args.option == "login":',
    			'\tmake_login()'
			],
			'main': False,
			'main_content': []
		},
		{
			'type': 'file',
			'name': 'wsgi.py',
			'from': {
				'manage': ['app']
			},
			'import': [],
			'function': [],
			'classes': [],
			'content': [

			],
			'main': True,
			'main_content': [
				'app.run()'
			]
		}
	]

}

def make_string_parameters(parameters):
	value = ''
	if parameters:
		string_parameters = ",%s" % ','.join(parameters)
	else:
		string_parameters = ''
	return string_parameters

def make_project(NAME):
	os.mkdir(os.path.join(os.getcwd(), NAME))
	for k,v in glassblower_structure.items():
		if k != 'others':
			new_dir = os.path.join(os.getcwd(), NAME, k)
			os.mkdir(new_dir)
			if type(v) != dict:
				for subdir_row in v:
					new_dir = os.path.join(os.getcwd(), NAME, k)
					if type(subdir_row) == str:
						new_dir = os.path.join(new_dir, subdir_row)
						with open(new_dir,'w') as nf:
							nf.close()
					else:
						new_dir = os.path.join(new_dir, subdir_row['name'])
						with open(new_dir,'w') as nf:
							for from_key, from_value in subdir_row['from'].items():
								nf.write("from %s import %s\n" % (from_key, ','.join(from_value)))
							for row_import in subdir_row['import']:
								nf.write("import %s\n" % row_import) 
							for row_class in subdir_row['classes']:
								nf.write("\n\nclass %s(%s):\n" % (row_class['name'], ','.join(row_class['inheritance'])))
								for row_class_attr, row_class_attr_value in row_class['attr'].items():
									nf.write("\t%s = %s\n" % (row_class_attr, row_class_attr_value))
								for row_class_func in row_class['function']:
									nf.write("\n\tdef %s(self%s):\n" % (row_class_func['name'], make_string_parameters(row_class_func['parameters'])))
									nf.write("\t\t%s\n" % '\n'.join(row_class_func['content']))
							if subdir_row['name'] == 'routes.blz':
								nf.write("%s" % ''.join(subdir_row['content']))
							else:
								nf.write("%s\n" % '\n'.join(subdir_row['content']))
							if subdir_row['main']:
								nf.write("if __name__ == \"__main__\":\n")
								nf.write("\t%s" % '\n'.join(subdir_row['main_content']))
							nf.close()
			else:
				#dentro de app
				for k1, v1 in v.items():
					new_dir = os.path.join(os.getcwd(), NAME, k, k1)
					if type(v1) == list:
						#carpetas de app
						os.mkdir(new_dir)
						for row in v1:
							if type(row) == str:
								if k1 == 'static':
									os.mkdir(os.path.join(os.getcwd(), NAME, k, k1, row))
								else:
									with open(os.path.join(os.getcwd(), NAME, k, k1, row),'w') as nf:
										nf.close()
							else:
								if k1 == 'static' and 'css' in row:
									os.mkdir(os.path.join(os.getcwd(), NAME, k, k1, 'css'))
									for style in row['css']:
										with open(os.path.join(os.getcwd(), NAME, k, k1, 'css', style),'w') as nf:
											nf.close()	
								else:
									with open(os.path.join(os.getcwd(), NAME, k, k1, row['name']),'w') as nf:
										for from_key, from_value in row['from'].items():
											nf.write("from %s import %s\n" % (from_key, ','.join(from_value)))
										for row_import in row['import']:
											nf.write("import %s\n" % row_import) 
										for row_class in row['classes']:
											nf.write("\n\nclass %s(%s):\n" % (row_class['name'], ','.join(row_class['inheritance'])))
											for row_class_attr, row_class_attr_value in row_class['attr'].items():
												nf.write("\t%s = %s\n" % (row_class_attr, row_class_attr_value))
											for row_class_func in row_class['function']:
												nf.write("\n\tdef %s(self%s):\n" % (row_class_func['name'], make_string_parameters(row_class_func['parameters'])))
												nf.write("\t\t%s\n" % '\n'.join(row_class_func['content']))
										nf.write("%s\n" % '\n'.join(row['content']))
										if row['main']:
											nf.write("if __name__ == \"__main__\":\n")
											nf.write("\t%s" % '\n'.join(row['main_content']))
										nf.close()
					else:
						# __init__.py
						with open(os.path.join(os.getcwd(), NAME, k, v1['name']),'w') as nf:
							for from_key, from_value in v1['from'].items():
								nf.write("from %s import %s\n" % (from_key, ','.join(from_value)))
							for row_import in v1['import']:
								nf.write("import %s\n" % row_import) 
							nf.write("%s\n" % '\n'.join(v1['content']))
							if v1['main']:
								nf.write("if __name__ == \"__main__\":\n")
								nf.write("\t%s" % '\n'.join(v1['main_content']))
							nf.close()
		else:
			for other in v:
				if type(other) == str:
					new_dir = os.path.join(os.getcwd(), NAME, other)
					with open(new_dir,'w') as nf:
						nf.close()
				else:
					new_dir = os.path.join(os.getcwd(), NAME, other['name'])
					with open(new_dir,'w') as nf:
						for from_key, from_value in other['from'].items():
							nf.write("from %s import %s\n" % (from_key, ','.join(from_value)))
						for row_import in other['import']:
							nf.write("import %s\n" % row_import) 
						nf.write("%s\n" % '\n'.join(other['content']))
						if other['main']:
							nf.write("if __name__ == \"__main__\":\n")
							nf.write("\t%s" % '\n'.join(other['main_content']))
						nf.close()
	

def main():
    # parse arguments using optparse or argparse or what have you
    if args.new == 'new':
    	make_project(args.project)
    	print('project created')
    	print('1) cd %s' % args.project)
    	print('2) virtualenv venv')
    	print('3) source venv/bin/activate')
    	print('4) pip install -r requirements.txt')
    	print('5) python wsgi.py')
    else:
    	print('Incorrect parameters use: new appname')

if __name__ == '__main__':
    import sys
    main()