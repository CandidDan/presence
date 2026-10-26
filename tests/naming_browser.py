"""Cloud interaction gate for the recovered related-words tool."""
from pathlib import Path
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
from functools import partial
from threading import Thread
from playwright.sync_api import sync_playwright
class Quiet(SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(Path(__file__).resolve().parents[1])));Thread(target=server.serve_forever,daemon=True).start()
base=f'http://127.0.0.1:{server.server_port}/tools/naming/'
try:
 with sync_playwright() as p:
  browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
  page=browser.new_page(reduced_motion='reduce');errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  for w,h in [(1440,1000),(768,1024),(390,844),(320,740)]:
   page.set_viewport_size({'width':w,'height':h});page.goto(base,wait_until='networkidle')
   assert page.locator('.word').count()>0
   assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'), (w,page.evaluate('document.documentElement.scrollWidth'))
   page.locator('button[data-seed=work]').click();assert page.locator('#seed').input_value()=='work'
   page.get_by_role('button',name='Craft',exact=True).click();page.get_by_role('button',name='Save to shortlist',exact=True).click()
   page.locator('#notes').fill('Test association — temporary browser check')
   page.reload(wait_until='networkidle');page.locator('.saved-name').first.click();assert page.locator('#notes').input_value()=='Test association — temporary browser check'
   page.get_by_role('button',name='Remove from shortlist',exact=True).click()
   page.locator('button[data-seed=space]').click()
   page.locator('#custom-word').fill('Common ground');page.locator('#add-form button').click();assert page.locator('#candidate h2').inner_text()=='Common ground'
   page.get_by_role('button',name='Save to shortlist',exact=True).click()
   with page.expect_download() as result:page.locator('#export').click()
   data=Path(result.value.path()).read_bytes();assert b'Common ground' in data
   page.locator('#import').set_input_files({'name':'workspace.json','mimeType':'application/json','buffer':data})
   page.wait_for_function("document.getElementById('notice').textContent.includes('Imported')")
   assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
   page.screenshot(path=f'/tmp/naming-workbench-{w}.png',full_page=True)
   page.evaluate('localStorage.clear()')
   print('PASS:',w,'layout, built-in maps, shortlist, reload, notes, own association and real export/import',flush=True)
  page.goto(base+'?word=connection',wait_until='networkidle');page.wait_for_selector('.word');assert 'Datamuse' in page.locator('#map-source').inner_text()
  page.locator('.word').first.click();word=page.locator('#candidate h2').inner_text();page.get_by_role('button',name='Explore from here',exact=True).click();page.wait_for_selector('.word');assert page.locator('#map-title').inner_text().lower()==word.lower()
  assert not errors,errors
  print('PASS: live dictionary lookup and branch exploration; no JS errors',flush=True)
  browser.close()
finally:server.shutdown()
