"""Explicit crawlable HTML redirects for the former website hostname."""
from pathlib import Path, PurePosixPath
from urllib.parse import urlsplit
from html import escape
import argparse,json,re
ROOT=Path(__file__).resolve().parents[1]
def destination_file(route):
    if not re.fullmatch(r'/[A-Za-z0-9_./-]*',route) or '..' in PurePosixPath(route).parts or route.startswith('//'):
        raise ValueError('Unsafe legacy path')
    if route.startswith('/notebooks/') or not (route.endswith('/') or route.endswith('.html')):
        raise ValueError('Only website HTML paths belong in this redirect map')
    return route.lstrip('/') + ('index.html' if route.endswith('/') else '')
def render(target):
    u=urlsplit(target)
    if u.scheme!='https' or u.netloc!='nadas.ro' or u.query or u.fragment or not re.fullmatch(r'/[A-Za-z0-9_./-]*',u.path) or '..' in PurePosixPath(u.path).parts:
        raise ValueError('Redirect must use an explicit nadas.ro destination')
    text=escape(target,quote=True)
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Moved to nadas.ro</title>
<link rel="canonical" href="{text}">
<script>window.location.replace({json.dumps(target)} + window.location.search + window.location.hash);</script>
<meta http-equiv="refresh" content="0;url={text}">
</head>
<body><h1>This page has moved</h1><p>Continue to <a href="{text}">{text}</a>.</p></body>
</html>
'''
def build(check=False):
    routes=json.loads((ROOT/'redirect-map.json').read_text())
    if routes.get('/')!='https://nadas.ro/':raise ValueError('Homepage mapping is required')
    for route,target in routes.items():
        path=ROOT/destination_file(route);markup=render(target)
        if check:
            if not path.is_file() or path.read_text()!=markup:raise ValueError('Stale redirect: '+route)
        else:
            path.parent.mkdir(parents=True,exist_ok=True);path.write_text(markup)
    print(f'{len(routes)} explicit HTML redirects validated' if check else f'{len(routes)} explicit HTML redirects generated')
if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--check',action='store_true');build(parser.parse_args().check)
