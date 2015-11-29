import BaseHTTPServer
import SocketServer
import threading
import time
import random
import urlparse
import cgi
import pprint
import re

import anagrams
import words

ROOT_PAGE = """<html><body onload="document.theform.q.focus();">
<form name=theform action="/search">
query: <input type=text name=q size=40 value=""> <input type=submit value=Go><br/>
<input type=radio name=kind value=anagram checked>anagram</input><br/>
<input type=radio name=kind value=match>regex match</input><br/>
<input type=radio name=kind value=search>regex search</input><br/>
</form>
"""

FOOTER = """
<hr>
<span class=next><a href=/>home</a></span>
<form name=theform action=/search>
q: <input type=text name=q size=40 value="%(q)s" <input type=submit value=Go>
<input type=hidden name=kind value="%(kind)s">
</form>

</body></html>
"""

class Handler(BaseHTTPServer.BaseHTTPRequestHandler):
  def HandleRoot(self, url):
    self.send_response(200)
    self.end_headers()
    self.wfile.write(ROOT_PAGE)

  def HandleSearch(self, url):
    d = cgi.parse_qs(url.query)
    q = d.get("q", [None])[0]
    kind = d.get("kind", ["anagram"])[0]
    if q is None:
      self.send_response(400)
      self.end_headers()
      self.wfile.write("missing query")
      return

    start = int(d.get("start", [0])[0])
    count = int(d.get("count", [50])[0])

    print "query is [%s]" % (q,)

    if kind == "anagram":
      result = anagrams.candidates(q)
    elif kind == "match":
      p = re.compile("^(?:" + q + ")$")
      result = [i for i in words.all if p.match(i)]
      result.sort()
    elif kind == "search":
      p = re.compile(q)
      result = []
      for i in words.all:
        m = p.search(i)
        if m:
          s, e = m.span()
          result.append((i, i[:s] + "<b>" + i[s:e] + "</b>" + i[e:]))
      result.sort()
      result = [i[1] for i in result]
    else:
      self.send_response(400)
      self.end_headers()
      self.wfile.write("unknown kind")
      return
      
    if start < 0: start = 0
    #if start > len(result) - count: start = len(result) - count
    
    self.send_response(200)
    self.end_headers()
    w = self.wfile.write

    self.WriteHeader()
    if result:
      if start > 0:
        w('<span class=prev><a href="/search?q=%s&kind=%s&start=%d&count=%d">prev</a></span>' % (q, kind, start-count, count))
      if start < len(result)-count:
        w('<span class=next><a href="/search?q=%s&kind=%s&start=%d&count=%d">next</a></span>' % (q, kind, start+count, count))
      w("<center>%d&ndash;%d of %d</center>" % (start+1, min(start+count, len(result)), len(result)))
      w("<pre>")
      words.print_compact_list(result[start:start+count], width=40, out=self.wfile)
      w("</pre>")
      print start, len(result), count
    else:
      w("no result")
    self.WriteFooter(q, kind)

  def WriteHeader(self):
    w = self.wfile.write
    w("<html><head>")
    w("<link rel=stylesheet type=text/css href=/css>")
    w('</head><body onload="document.theform.q.focus();">')

  def WriteFooter(self, q, kind):
    w = self.wfile.write
    w(FOOTER % {"q": cgi.escape(q, True), "kind": kind})
    
    
  def HandleCss(self, url):
    self.send_response(200)
    self.send_header("Content-Type", "text/css")
    self.end_headers()
    self.wfile.write("""
.prev { float: left }
.next { float: right }
pre b { color: red }
""")
    
  def HandleError(self, url):
    self.send_response(404)
    self.end_headers()
    self.wfile.write("404 not found")
  
  DISPATCH = {
    "/": HandleRoot,
    "/search": HandleSearch,
    "/css": HandleCss,
    None: HandleError,
    }

  def do_GET(self):
    o = urlparse.urlparse(self.path)
    handler = self.DISPATCH.get(o.path, self.DISPATCH[None])
    handler(self, o)

  
class PuzzServ(SocketServer.ThreadingMixIn,
           BaseHTTPServer.HTTPServer):
  def __init__(self, address):
    BaseHTTPServer.HTTPServer.__init__(self, address, Handler)

    
if __name__ == '__main__':
  httpd = PuzzServ(("", 9998))
  print "listening..."
  httpd.serve_forever()
