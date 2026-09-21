"""Zero-dependency RootCause AI backend using Python's standard library."""
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
import os, json, sqlite3, hashlib, secrets, datetime, mimetypes

BASE=os.path.dirname(os.path.dirname(os.path.abspath(__file__))); FRONT=os.path.join(BASE,'frontend'); DB=os.path.join(BASE,'backend','rootcause.db')
SESSIONS={}
DEMO={'system_status':'OPERATIONAL','kpis':{'total_pipelines':7,'healthy':5,'active_failures':1,'root_causes':12,'avg_resolution':'8.4m'},'root_cause':{'type':'SCHEMA DRIFT','confidence':96,'severity':'HIGH','field':'customer_id','expected':'INTEGER','actual':'STRING','impact':{'pipelines':7,'dashboards':2,'ml_models':1},'recommendation':'Restore the expected column type or update the downstream schema.'},'pipelines':[{'name':'customer_360_pipeline','status':'FAILED','last_run':'10:42 AM','duration':'4m 18s','records':'1.24M','health':18},{'name':'orders_daily','status':'HEALTHY','last_run':'10:39 AM','duration':'2m 11s','records':'842K','health':98},{'name':'revenue_model','status':'HEALTHY','last_run':'10:31 AM','duration':'3m 04s','records':'218K','health':96},{'name':'product_analytics','status':'WARNING','last_run':'10:28 AM','duration':'5m 09s','records':'1.02M','health':72},{'name':'customer_events','status':'HEALTHY','last_run':'10:24 AM','duration':'1m 44s','records':'3.81M','health':99}], 'root_causes':[{'name':'Schema Drift','value':62},{'name':'Data Quality','value':18},{'name':'Pipeline Failure','value':12},{'name':'Connection Failure','value':8}], 'timeline':[12,18,9,25,14,31,20,16,29,22,35,27], 'quality':{'schema_consistency':96,'duplicate_rows':0,'negative_amounts':0,'invalid_records':2}, 'incidents':[{'id':'INC-1042','pipeline':'customer_360_pipeline','root_cause':'Schema Drift','severity':'HIGH','confidence':'96%','detected':'10:42 AM','status':'OPEN'},{'id':'INC-1040','pipeline':'product_analytics','root_cause':'Null Spike','severity':'MEDIUM','confidence':'89%','detected':'10:28 AM','status':'MONITORING'},{'id':'INC-1038','pipeline':'orders_daily','root_cause':'Late Source Data','severity':'LOW','confidence':'91%','detected':'09:51 AM','status':'RESOLVED'},{'id':'INC-1031','pipeline':'revenue_model','root_cause':'Null Spike','severity':'LOW','confidence':'88%','detected':'09:12 AM','status':'RESOLVED'}]}
SIGNALS=[('Schema signal','customer_id changed from INTEGER to STRING.','Strongest direct signal at the source boundary.'),('Log signal','TypeError detected in the transform stage.','Corroborates the schema mismatch.'),('DQ signal','Type validation breached after the source update.','Supports the same failure chain.'),('Dependency signal','7 downstream pipelines consume the affected table.','Defines the blast radius.'),('Historical signal','A similar schema change produced the same pattern.','Increases confidence in the diagnosis.')]

def init_db():
 os.makedirs(os.path.dirname(DB),exist_ok=True); c=sqlite3.connect(DB); c.execute('CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT,email TEXT UNIQUE,password_hash TEXT,salt TEXT,created_at TEXT)'); c.commit(); c.close()
def hashpw(p,s=None):
 s=s or secrets.token_hex(16); return hashlib.pbkdf2_hmac('sha256',p.encode(),s.encode(),120000).hex(),s
def json_body(r):
 try:return json.loads(r.rfile.read(int(r.headers.get('Content-Length','0')) or 0) or '{}')
 except:return {}
def send(r,code,data,headers=None):
 raw=data if isinstance(data,bytes) else json.dumps(data).encode(); r.send_response(code); r.send_header('Content-Type', 'application/json' if not isinstance(data,bytes) else 'application/octet-stream'); r.send_header('Content-Length',str(len(raw))); (headers or {}).items()
 for k,v in (headers or {}).items():r.send_header(k,v)
 r.end_headers();r.wfile.write(raw)
class Handler(BaseHTTPRequestHandler):
 def log_message(self,*a):pass
 def user(self):
  sid=self.headers.get('Cookie','').replace('rc_session=','').split(';')[0]; return SESSIONS.get(sid)
 def do_GET(self):
  p=urlparse(self.path).path
  if p=='/api/health':return send(self,200,{'status':'ok','service':'RootCause AI API','version':'1.0.0'})
  if p=='/api/dashboard':
   d=json.loads(json.dumps(DEMO));d['signals']=[{'name':a,'detail':b,'why':c} for a,b,c in SIGNALS];return send(self,200,d)
  if p=='/api/me':return send(self,200,{'user':self.user()})
  path='/index.html' if p=='/' else ('/dashboard.html' if p=='/dashboard' else p)
  fp=os.path.normpath(os.path.join(FRONT,path.lstrip('/')))
  if not fp.startswith(FRONT) or not os.path.isfile(fp):return send(self,404,{'error':'Not found'})
  raw=open(fp,'rb').read();self.send_response(200);self.send_header('Content-Type',mimetypes.guess_type(fp)[0] or 'text/plain');self.send_header('Content-Length',str(len(raw)));self.end_headers();self.wfile.write(raw)
 def do_POST(self):
  p=urlparse(self.path).path; d=json_body(self)
  if p=='/api/auth/signup':
   name=d.get('name','').strip();email=d.get('email','').strip().lower();pw=d.get('password','')
   if not name or not email or len(pw)<6:return send(self,400,{'error':'Name, email and a 6+ character password are required.'})
   h,s=hashpw(pw)
   try:
    c=sqlite3.connect(DB);c.execute('INSERT INTO users(name,email,password_hash,salt,created_at) VALUES(?,?,?,?,?)',(name,email,h,s,datetime.datetime.utcnow().isoformat()));c.commit();c.close()
   except sqlite3.IntegrityError:return send(self,409,{'error':'An account with this email already exists.'})
   u={'name':name,'email':email};sid=secrets.token_urlsafe(24);SESSIONS[sid]=u;return send(self,200,{'ok':True,'user':u},{'Set-Cookie':f'rc_session={sid}; Path=/; HttpOnly; SameSite=Lax'})
  if p=='/api/auth/login':
   email=d.get('email','').strip().lower();pw=d.get('password','');c=sqlite3.connect(DB);c.row_factory=sqlite3.Row;u=c.execute('SELECT * FROM users WHERE email=?',(email,)).fetchone();c.close()
   if not u:return send(self,401,{'error':'Invalid email or password.'})
   h,_=hashpw(pw,u['salt'])
   if not secrets.compare_digest(h,u['password_hash']):return send(self,401,{'error':'Invalid email or password.'})
   user={'name':u['name'],'email':u['email']};sid=secrets.token_urlsafe(24);SESSIONS[sid]=user;return send(self,200,{'ok':True,'user':user},{'Set-Cookie':f'rc_session={sid}; Path=/; HttpOnly; SameSite=Lax'})
  if p=='/api/auth/logout':return send(self,200,{'ok':True},{'Set-Cookie':'rc_session=; Max-Age=0; Path=/; HttpOnly'})
  if p=='/api/analyze':return send(self,200,{'ok':True,'message':'AI analysis complete — Schema Drift confirmed at 96%.','result':DEMO['root_cause']})
  if p=='/api/remediate':return send(self,200,{'ok':True,'message':'Remediation recorded. Incident marked resolved.','action':'schema_validation_rerun'})
  return send(self,404,{'error':'Not found'})
def main():
 init_db();server=ThreadingHTTPServer(('127.0.0.1',5055),Handler);print('RootCause AI running at http://127.0.0.1:5055');server.serve_forever()
if __name__=='__main__':main()
