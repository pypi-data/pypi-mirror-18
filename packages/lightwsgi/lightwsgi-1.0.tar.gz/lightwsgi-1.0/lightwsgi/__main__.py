import os, sys, pwd, grp, urllib2, getpass, shutil

def recursive_chown(path, user, group):
    uid = pwd.getpwnam(user).pw_uid
    gid = grp.getgrnam(group).gr_gid

    for root, dirs, files in os.walk(path):
        for momo in dirs:
            os.chown(os.path.join(root, momo), uid, gid)
        for momo in files:
            os.chown(os.path.join(root, momo), uid, gid)

def recursive_chmod(path, mode):
    for root, dirs, files in os.walk(path):
        for reldir in dirs:
            os.chmod(os.path.join(root, reldir), mode)
        for relfile in files:
            os.chmod(os.path.join(root, relfile), mode)

def setup_project(projdir):
    try:
        os.mkdir(projdir)
    except OSError as e:
        if e.errno == 17:
            proceed = raw_input("Are you sure you want to proceed? If you do, your existing directory will \
be wiped. [y to proceed, any other key to cancel] ")
            if not proceed == "y":
                print("Cancelled.")
                return
            else:
                shutil.rmtree(projdir)
                os.mkdir(projdir)

    staticdir = os.path.join(projdir, "static")
    scriptsdir = os.path.join(projdir, "scripts")

    os.mkdir(staticdir)
    os.mkdir(scriptsdir)
    os.mkdir(scriptsdir + "/pagescripts")
    open(scriptsdir + "/pagescripts/__init__.py", "w").close()
    with open(scriptsdir + "/pagescripts/index.py", "w") as indexf:
        indexf.write(indexf_init)

    with open(scriptsdir + "/manager.wsgi", "w") as managerfile:
        managerfile.write(managerscript % os.path.join(os.getcwd(), scriptsdir))
    recursive_chmod(projdir, 0755)

    print("""
Done. Now, go to your Apache configuration and add these lines:

LoadModule wsgi_module libexec/apache2/mod_wsgi.so

AliasMatch ^/static/(.*)$ /path/to/project
WSGIScriptAlias / /path/to/project/scripts/manager.wsgi

<Directory /path/to/project>
    Allow all granted
</Directory>
""")

managerscript = """
import lightwsgi
import lightwsgi.cookie as lcookie
import cgi, sys, os, inspect

sys.path.append('%s')

def application(environ, start_response):
    status = '200 OK'

    if environ['PATH_INFO'][-1] == '/' and not len(environ['PATH_INFO']) == 1:
        request_path = environ['PATH_INFO'][:-1]
    else:
        request_path = environ['PATH_INFO']

    pathscripts = {
        '/': 'index',
    }

    page = output = redirect_location = None
    mimetype = 'text/html'
    response_headers = []

    post_env = environ.copy()
    qs = post_env['QUERY_STRING']
    post_env['QUERY_STRING'] = ''
    posts = lightwsgi.getHeaderDict(cgi.FieldStorage(environ=post_env,
            fp=post_env['wsgi.input'], keep_blank_values=True))
    gets = dict([(i.split('=')[0], i.split('=')[1]) if len(i.split('=')) > 1 else (i, '')
    for i in qs.split('&')])

    try:
        page = __import__('pagescripts.%%s' %% pathscripts[request_path],
               fromlist=[''])
        reload(page)
    except KeyError:
        status = '404 Not Found'
        output = ''
    else:
        pageoutput = page.page(environ, gets, posts)
        if len(pageoutput) == 3:
            otheropts = pageoutput[2]
            if 'redirect' in otheropts:
                response_headers.append(('Location', otheropts['redirect']))
                status = '303 See Other'
            if 'cookie' in otheropts:
                from Cookie import SimpleCookie
                cookieheader = SimpleCookie()
                for cookie in otheropts['cookie']:
                    cookieheader[cookie['name']] = cookie['value']
                    if 'expires' in cookie:
                        cookieheader[cookie['name']]['expires'] = lcookie.cookieExpiryFormat(cookie['expires'])

                    if 'httponly' in cookie and cookie['httponly'] == True:
                        cookieheader[cookie['name']]['httponly'] = True

                    if 'path' in cookie:
                        cookieheader[cookie['name']]['path'] = cookie['path']
                    else:
                        cookieheader[cookie['name']]['path'] = '/'

                    if 'domain' in cookie:
                        cookieheader[cookie['name']]['domain'] = cookie['domain']

                    if 'secure' in cookie:
                        cookieheader[cookie['name']]['secure'] = True
                for name in cookieheader:
                    response_headers.append(('Set-Cookie', cookieheader[name].OutputString()))
        output, mimetype = pageoutput[0:2]

    if not output is None:
        response_headers.append(('Content-Length', str(len(output))))
    if not mimetype is None:
        response_headers.append(('Content-type', mimetype))

    start_response(status, response_headers)

    return [output if not output is None else '']"""

indexf_init = """
import lightwsgi

def page(environ, gets, posts):
    return ("<h1>It works!</h1>", "text/html", {})
"""

if __name__ == "__main__":
    if len(sys.argv) >= 3 and sys.argv[1] == "makeapp":
        setup_project(sys.argv[2])
